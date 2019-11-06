from twitchio.ext import commands
import os
from config import irc_token, client_id

# api token can be passed as test if not needed.
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

bot.run()
