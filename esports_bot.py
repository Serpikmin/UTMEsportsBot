from cmath import e
import os
import string
import discord
from discord.ext import commands
from dotenv import load_dotenv
from datetime import datetime, timedelta
from fetchtest import search_charatcer

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

class Lobby:   # Class to store lobby information
    def __init__(self, lobby_code, creator_name):
        self.lobby_code = lobby_code
        self.lobby_time = datetime.now()  # Track when lobby was created
        self.creator = creator_name

    def get_code(self) -> string:
        return self.lobby_code

current_lobbies = set() # Store currently hosted lobbies, added by commands

bot = commands.Bot(command_prefix='!')  # Bot commands designated by !
bot.remove_command("help")              # Removes the default help command.


class Commands(commands.Cog):    # Class storing all the commands of the bot
    @commands.command(name='ping')
    async def ping(self, ctx):
        await ctx.send("pong")

    @commands.command(name='dustloop')
    async def dustloop(self, ctx, char=None, move=None):
        if char is None or move is None:
            await ctx.send("Invalid format")
        else:
            try:
                await ctx.send(embed=search_charatcer(char, move))
            except Exception as e:
                await ctx.send('Error: Move not found!')

    @commands.command(name='ggstlobby')   # Display all current lobbies, or make a new one if given an arg
    async def ggstlobby(self, ctx, lobby_code=None):
        if lobby_code is None:    # No args, just checking queue
            embed = discord.Embed(title='Current Lobbies')
            lobby_messages = []
            current_time = datetime.now()
            for lobby in current_lobbies:
                if ((current_time - lobby.lobby_time).total_seconds()/3600) > 24: # If lobby has been here for 24h, remove
                    current_lobbies.remove(lobby)
                else:
                    lobby_messages.append('**{}** created by {} at {}:{} on {}/{}'.format(lobby.lobby_code, lobby.creator, lobby.lobby_time.hour, lobby.lobby_time.minute, lobby.lobby_time.month, lobby.lobby_time.day))

            if current_lobbies == set():
                lobby_messages.append('No lobbies right now :(')

            embed_val = '\n'.join(lobby_messages)
            embed.add_field(name='Guilty Gear Strive:', value=embed_val, inline=False)
            await ctx.send(embed=embed)

        else:   # Arg, adding to queue
            new_lobby = Lobby(lobby_code, ctx.author.name)
            current_lobbies.add(new_lobby)
            await ctx.send('Lobby Added!')

    @commands.command(name='help')
    async def help(self, ctx):
        await ctx.send("```COMMANDS:\nhelp: display this message\n\nggstlobby: lists all currently registered lobbies, or registers a new one.  To see all lobbies type this without arguments, and to add a lobby use \"!ggstlobby <lobbyname>\"\n\ndustloop: displays a characters frame data for a specific move, taken from dustloop. Example: \"!dustloop nago 632146h\".\nSome names and inputs have aliases```")

    

bot.add_cog(Commands())     # Adding the commands to the bot
bot.run(TOKEN)              # This runs the bot