import requests
import json
import urllib.request, urllib.error
import os
import glob
import time

requests.adapters.DEFAULT_RETRIES = 500000000

script_path = os.path.dirname(os.path.abspath(__file__))
temp_path = (script_path + '\\temp\\')
statefile = ("state.txt")

if not os.path.exists(temp_path):
    os.makedirs(temp_path)

token = 'token'

already_visited = []


def startbattle():
    # delete temp files
    # tempfilelist = glob.glob(os.path.join(temp_path, "*.*"))
    # for tempfile in tempfilelist:
    #    os.remove(tempfile)

    # get results from API
    r = requests.get('https://ai-arena.net/api/results/?ordering=-created', headers={'Authorization': "Token " + token})
    r.text
    data = json.loads(r.text)

    # results are ordered by match id from lowest to highest.
    # we always want to show the game with the highest id that
    # has not been shown already.
    # If there is no new games, reset.
    found_new_game = False
    for battle in reversed(data['results']):
        if battle['id'] not in already_visited:
            already_visited.append(battle['id'])
            found_new_game = True;
            break
    if not found_new_game:
        already_visited.clear()
        return

    # define a few vars for easier handling
    battleid = battle['id']
    winner = battle['winner']
    replayfile = str(battle['replay_file'])
    if replayfile == "None":
        return

    # We dont want to show Tie Games
    if battle['game_steps'] >= 60480:
        return

    print(str(battle['bot1_name'] + " vs " + str(battle['bot2_name'])))

    if os.path.isfile(statefile):
        os.remove(statefile)
    f = open(statefile, "a+")
    f.write("Game: " + str(battleid) + "\n")
    f.close()

    replaysave = temp_path + str(battleid) + ".Sc2Replay"

    # download replay
    try:
        urllib.request.urlretrieve(replayfile, replaysave)
    except urllib.error.URLError as e:
        return

    # print replay data to CLI
    print("Round " + str(battleid))
    print("----------\n")
    print("Winner: " + str(winner))

    # rename bots
    # if 'bot1_name' in battle:
    #    print("BotReplayRename.exe \"" + replaysave + "\"" + " foo5679 " + battle['bot1_name'] + " foo5680 " + battle['bot2_name'])
    #    os.system("BotReplayRename.exe \"" + replaysave + "\"" + " foo5679 " + battle['bot1_name'] + " foo5680 " + battle['bot2_name'])

    # run Observer
    os.system("ExampleObserver.exe --Path \"" + replaysave + "\"")
    # os.system("ExampleObserver.exe --Path \"" + replaysave + "\" --data_version B89B5D6FA7CBF6452E721311BFBC6CB2")


# Main Loop
while True:
    # os.system('cls')
    try:
        startbattle()
    except Exception as e:
        print(e)
        print("Something failed! Trying again in 10 seconds...")
        time.sleep(10)
