import os

from twitchio.ext import commands

from config import irc_token, client_id
from util import queue_match_replay, get_queue, is_match_id

# Channels is the initial channels to join, this could be a list, tuple or callable
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
        if ctx.content[:7] == '!queue ':
            match_id = ctx.content[7:]
        elif ctx.content[:3] == '!q ':
            match_id = ctx.content[3:]
        else:  # empty command
            queue = get_queue()
            await ctx.send(f'Current queue:\n' + queue)
            return

        if is_match_id(match_id):
            queue_match_replay(int(match_id))
            await ctx.send(f'Match ID {match_id} queued')
        else:
            await ctx.send(f'Sorry {ctx.author.name}, please supply a valid match id.')


bot.run()
