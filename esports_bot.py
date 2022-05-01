import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
import copy
import re


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='!')  # Bot commands designated by !
bot.remove_command("help")              # Removes the default help command.

players = []
matches = ()
nextround = []
totalgames = 0;
ready = False;

class Commands(commands.Cog):    # Class storing all the commands of the bot
    @commands.command(name='hello')
    async def hello(self, ctx):
        name = ctx.author.name
        await ctx.send("Hello {}!".format(name))

    @commands.command(name='ping')
    async def ping(self, ctx, id):
        myid = '<@{}>'.format(id)
        await ctx.send(' %s is the best' % myid)

    @commands.command(name='start_t')
    async def start_t(self, ctx, brackets=None):
        if brackets == None:
            await ctx.send("Usage Format: (Discord Name)#(numbers)|+")
        else:
            if re.match("^([a-zA-z]+#[0-9][0-9][0-9][0-9]/)+([a-zA-z]+#[0-9][0-9][0-9][0-9])$", brackets):
                global players
                players = brackets.split("/") # stores players in a list
                global nextround
                nextround = [None] * (len(players)//2)
                # how many matches there will be next round
                global matches
                matches = zip(players[::2], players[1::2])
                # pairs up players and stores pairs in a tuple
                await ctx.send("Tournament Started")
            else:
                await ctx.send("Usage Format: (Discord Name)#(numbers)|+")

    @commands.command(name='win')
    async def win(self, ctx, name=None, groupNumber=None):
            groupnumber = int(groupNumber)
            if matches == ():
                await ctx.send("There's no tournament")
            else:
                if name in players:
                    nextround[groupnumber - 1] = name
                    if len(nextround) == 1 and None not in nextround:
                        await ctx.send("We have a winner")
                    else:
                        await ctx.send("Congrats {}, wait for your next match".format(name))
                    if None not in nextround and len(nextround) != 1:
                        global ready
                        ready = True
                        await ctx.send("Next round is ready")
                else:
                    await ctx.send("You're not in the tournament")

    @commands.command(name='nextround_start')
    async def nextround_start(self, ctx):
        global ready
        global players
        global matches
        global nextround
        if ready == True:
            matches = zip(nextround[::2], nextround[1::2])
            for match in matches:
                await ctx.send("{player1} and {player2}, Group {group}".format(player1 = match[0], player2
                 = match[1], group = 1))
            ready = False
            players = copy.deepcopy(nextround)
            nextround.clear()
            nextround = [None] * (len(players)//2)
        else:
            await ctx.send("Next round is not ready yet")

"""
!start_t a#1111/b#2222/c#3333/d#4444
!win a#1111 1
!win d#4444 2
!nextround_start
!win a#1111 1
"""

bot.add_cog(Commands())     # Adding the commands to the bot
bot.run(TOKEN)              # This runs the bot



