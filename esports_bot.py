import os
import string
import discord
import json
from discord.ext import commands
from dotenv import load_dotenv
from datetime import datetime, timedelta

GAMES = ['Guilty Gear Strive', 'Street Fighter V', 'Tekken 7', 'Dragon Ball FighterZ', 'King of Fighers XV']

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

class Lobby:   # Class to store lobby information
    def __init__(self, lobby_code, creator_name):
        self.lobby_code = lobby_code
        self.lobby_time = datetime.now()  # Track when lobby was created
        self.creator = creator_name

class User:
    def __init__(self, user, ):
        self.user = user
        self.aliases = set()
        self.games = set()

users_have_changed = False # stores if users have been updated (to update json file)
current_lobbies = set() # Store currently hosted lobbies, added by commands
all_users = set() # Stores all users and also saves it to a file that we can load from

bot = commands.Bot(command_prefix='!')  # Bot commands designated by !
bot.remove_command("help")              # Removes the default help command.

f=open('data.json')
all_users = json.loads(f) # load values for json()
f.close()

class Commands(commands.Cog):    # Class storing all the commands of the bot
    @commands.command(name='hello')
    async def hello(self, ctx):
        name = ctx.author.name
        await ctx.send("Hello {}!".format(name))

    @commands.command(name='ggstlobby')   # Display all current lobbies, or make a new one if given an arg
    async def ggstlobby(self, ctx, lobby_code=None):
        if lobby_code == None:    # No args, just checking queue
            embed = discord.Embed(title='Current Lobbies')
            lobby_messages = []
            current_time = datetime.now()
            for lobby in current_lobbies:
                if ((current_time - lobby.lobby_time).total_seconds()/3600) > 24: # If lobby has been here for 24h, remove
                    current_lobbies.remove(lobby)
                else:
                    lobby_messages.append('**{}** created {}:{} {}/{} by {}'.format(lobby.lobby_code, lobby.lobby_time.hour, lobby.lobby_time.minute, lobby.lobby_time.month, lobby.lobby_time.day, lobby.creator))
            
            if current_lobbies == set():
                lobby_messages.append('No lobbies right now D:')

            embed_val = '\n'.join(lobby_messages)
            embed.add_field(name='Guilty Gear Strive:', value=embed_val, inline=False)
            await ctx.send(embed=embed)
        
        else:   # Arg, adding to queue
            new_lobby = Lobby(lobby_code, ctx.author.name)
            current_lobbies.add(new_lobby)
            await ctx.send('Lobby Added!')

    async def setup_new_user(self, ctx):
        print('wip lol')

    @commands.command(name='tempsave')
    async def save_users(self, ctx):
        f=open('data.json', 'w')
        f.write(json.dump(all_users))
        f.close()

bot.add_cog(Commands())     # Adding the commands to the bot
bot.run(TOKEN)              # This runs the bot