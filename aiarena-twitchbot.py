import os

from twitchio.ext import commands
from pynput.keyboard import Key, Controller
import time
from config import irc_token, client_id
from util import queue_match_replay, get_queue, is_match_id, statefile


class Bot(commands.Bot):
    def __init__(self):
        # Initialise our Bot with our access token, prefix and a list of channels to join on boot...
        # prefix can be a callable, which returns a list of strings or a string...
        # initial_channels can also be a callable which returns a list of strings...
        super().__init__(
            token=irc_token,
            client_id=client_id,
            nick='aiarenastream',
            prefix='!',
            initial_channels=['#aiarenastream']
        )

    # Register an event with the bot
    async def event_ready(self):
        print(f'Ready | {self.nick}')

    async def event_message(self, message):
        # Messages with echo set to True are messages sent by the bot...
        # For now we just want to ignore them...
        if message.echo:
            return

        # Print the contents of our message to console...
        print(message.content)

        # Since we have commands and are overriding the default `event_message`
        # We must let the bot know we want to handle and invoke our commands...
        await self.handle_commands(message)

    # Register a command with the bot

    # Display a help command in chat
    @commands.command(name='help', aliases=['h', 'commands'])
    async def help_command(self, ctx: commands.Context):
        help_message = """!help - Display this message
        Aliases: h, commands
    
        !link - Request the current match's website link to be pasted into chat.
        Aliases: l
    
        !next - Request to move on to the next game
        Aliases: n
    
        !queue {GAME ID}[, MORE IDs, ...]- Queue a game from AIArena to the queue using its game ID.
        Aliases: q
    
        !restart - Restart the OBS stream.
        Aliases: r
        """
        await ctx.send(f'Here you go {ctx.author.name}\n\n{help_message}')

    @commands.command(name='restart', aliases=['r'])
    async def restart_stream_command(self, ctx: commands.Context):
        # if ctx.author.is_mod:
        await ctx.send(f'Okay {ctx.author.name} - I will restart the stream! - Please wait')
        keyboard = Controller()
        keyboard.press(Key.ctrl)
        keyboard.press(']')
        keyboard.release(']')

        keyboard.release(Key.ctrl)
        time.sleep(1)
        keyboard.press(Key.ctrl)
        keyboard.press('[')
        keyboard.release('[')
        keyboard.release(Key.ctrl)

    @commands.command(name='next', aliases=['n'])
    async def next_command(self, ctx: commands.Context):
        # if ctx.author.is_mod:
        await ctx.send(f'Okay {ctx.author.name} - I will restart Sc2! - Please wait')
        os.system("taskkill /f /im SC2_x64.exe")
        os.system("taskkill /f /im ExampleObserver.exe")

    @commands.command(name='queue', aliases=['q'])
    async def queue_match_command(self, ctx: commands.Context):
        # if ctx.author.is_mod:
        content = ctx.message.content
        if content[:7] == '!queue ':
            match_id = content[7:]
        elif content[:3] == '!q ':
            match_id = content[3:]
        else:  # empty command
            queue = get_queue()
            await ctx.send(f'Current queue:\n' + queue)
            return

        if is_match_id(match_id):
            queue_match_replay(int(match_id))
            await ctx.send(f'Match ID {match_id} queued')
        else:
            await ctx.send(f'Sorry {ctx.author.name}, please supply a valid match id.')

    @commands.command(name='link', aliases=['l'])
    async def queue_command(self, ctx: commands.Context):
        """Loads the statefile content, which contains a link to the current match."""
        with open(statefile, 'r') as file:
            data = file.read()
            await ctx.send(data)


bot = Bot()
bot.run()
