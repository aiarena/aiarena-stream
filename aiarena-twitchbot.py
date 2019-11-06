import os

from twitchio.ext import commands

from config import irc_token, client_id
# api token can be passed as test if not needed.
# Channels is the initial channels to join, this could be a list, tuple or callable
from util import queue_file


def queue_match_replay(match_id):
    f = open(queue_file, "a+")
    f.write(str(match_id) + "\n")
    f.close()


def get_queue():
    f = open(queue_file, "r")
    queue = f.read()
    f.close()
    return queue


bot = commands.Bot(
    irc_token=irc_token,
    client_id=client_id,
    nick='aiarenastream',
    prefix='!',
    initial_channels=['#aiarenastream']
)


# Register an event with the bot
@bot.event
async def event_ready():
    print(f'Ready | {bot.nick}')


@bot.event
async def event_message(message):
    print(message.content)

    # If you override event_message you will need to handle_commands for commands to work.
    await bot.handle_commands(message)


# Register a command with the bot
@bot.command(name='next', aliases=['n'])
async def next_command(ctx):
    if ctx.author.is_mod:
        await ctx.send(f'Okay {ctx.author.name} - I will restart Sc2! - Please wait')
        os.system("taskkill /f /im SC2_x64.exe")
        os.system("taskkill /f /im ExampleObserver.exe")


@bot.command(name='queue', aliases=['q'])
async def queue_command(ctx):
    if ctx.author.is_mod:
        match_id = None

        try:
            if ctx.content[:7] == '!queue ':
                match_id = int(ctx.content[7:])  # test for a valid integer
            elif ctx.content[:3] == '!q ':
                match_id = int(ctx.content[3:])  # test for a valid integer
            else:  # empty command
                queue = get_queue()
                await ctx.send(f'Current queue:\n' + queue)
                return

            # account for negative numbers
            if match_id < 1:
                await ctx.send(f'Sorry {ctx.author.name}, please supply a valid match id.')
                return

        except ValueError:
            await ctx.send(f'Sorry {ctx.author.name}, please supply a valid match id.')

        if match_id is not None:
            queue_match_replay(match_id)
            await ctx.send(f'Match ID {match_id} queued')


bot.run()
