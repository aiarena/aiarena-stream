import traceback

import requests
import json
import urllib.request, urllib.error
import os
import glob
import time
import config

from gtts import gTTS
import playsound

from util import queue_pop_next_match, statefile

requests.adapters.DEFAULT_RETRIES = 500000000

script_path = os.path.dirname(os.path.abspath(__file__))
temp_path = (script_path + '\\temp\\')

if not os.path.exists(temp_path):
    os.makedirs(temp_path)

already_visited = []

def retrieve_match_data(match_id):
    r = requests.get(f'https://aiarena.net/api/matches/{match_id}', headers={'Authorization': "Token " + config.token})
    data = json.loads(r.text)
    return data


def retrieve_map_data(map_id):
    r = requests.get(f'https://aiarena.net/api/maps/{map_id}', headers={'Authorization': "Token " + config.token})
    data = json.loads(r.text)
    return data


def download_map(match_id):
    match_data = retrieve_match_data(match_id)
    map_data = retrieve_map_data(match_data["map"])

    map_save_location = os.path.join(config.sc2_maps_folder, f"{map_data['name']}.Sc2Map")

    try:
        urllib.request.urlretrieve(map_data["file"], map_save_location)
    except urllib.error.URLError as e:
        print(e)
        return False

    return True


def startbattle():
    # delete temp files
    tempfilelist = glob.glob(os.path.join(temp_path, "*.*"))
    for tempfile in tempfilelist:
       os.remove(tempfile)

    queued_match_id = queue_pop_next_match()
    if queued_match_id is not None:
        print(f"Playing queued match id: {queued_match_id}")
        r = requests.get(f'https://aiarena.net/api/results/?match={queued_match_id}', headers={'Authorization': "Token " + config.token})
        data = json.loads(r.text)
        battle = data['results'][0]
        already_visited.append(battle['match'])
    else:
        print("No matches queued. Searching for a recent replay.")
        # get replay from API
        r = requests.get('https://aiarena.net/api/stream/next-replay/', headers={'Authorization': "Token " + config.token})
        data = json.loads(r.text)

        # If there is no new games, reset.
        found_new_game = False
        for battle in reversed(data['results']):
            if battle['match'] not in already_visited:
                already_visited.append(battle['match'])
                found_new_game = True
                break
        if not found_new_game:
            already_visited.clear()
            print("All matches viewed - resetting.")
            return

    # define a few vars for easier handling
    match = battle['match']
    replayfile = str(battle['replay_file'])
    if replayfile == "None":
        print("Replay file was None!")
        return

    print(str(battle['bot1_name'] + " vs " + str(battle['bot2_name'])))

    f = open(statefile, "w")
    f.write("Match: https://aiarena.net/matches/" + str(match) + "/\n")
    f.close()

    if not download_map(match):
        print("Map download failed.")
        return

    replaysave = temp_path + str(match) + ".Sc2Replay"

    # download replay
    try:
        urllib.request.urlretrieve(replayfile, replaysave)
    except urllib.error.URLError as e:
        print(e)
        return

    # print replay data to CLI
    print("Match " + str(match))
    print("----------\n")

    # remove chat
    removechatcmd = "ReplayChatRemove.exe \"" + replaysave + "\""
    print("Running command:\n" + removechatcmd)
    os.system(removechatcmd)

    # run Observer
    cmd = "ExampleObserver.exe -p \"" + replaysave + "\""
    if hasattr(config, 'sc2_executable') and config.sc2_executable is not None:
        cmd += f" -e \"{config.sc2_executable}\""
    if hasattr(config, 'sc2_data_version') and config.sc2_data_version is not None:
        cmd += f" -d \"{config.sc2_data_version}\""
    print("Running command:\n" + cmd)
    os.system(cmd)
    # os.system("ExampleObserver.exe --Path \"" + replaysave + "\" --data_version B89B5D6FA7CBF6452E721311BFBC6CB2")

    # Text to speech match announcement
    tts = gTTS(str(battle['bot1_name']) + " versus " + str(battle['bot2_name']), lang='en')
    tts_file_name = os.path.join(os.path.abspath(os.getcwd()), 'current_game.mp3')
    tts.save(tts_file_name)
    playsound.playsound(tts_file_name)
    os.remove(tts_file_name)


# Main Loop
while True:
    # os.system('cls')
    try:
        startbattle()
    except Exception as e:
        traceback.print_exc()
        print("Something failed! Trying again in 10 seconds...")
        time.sleep(10)
