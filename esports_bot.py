import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
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

    @commands.command(name='start_t')
    async def start_t(self, ctx, brackets=None):
        if brackets == None:
            await ctx.send("Usage Format: (Discord Name)#(numbers)|+")
        else:
            if re.match("^([a-zA-z]+#[0-9][0-9][0-9][0-9]/)+([a-zA-z]+#[0-9][0-9][0-9][0-9])$", brackets):
                global players
                players = brackets.split("/") # stores players in a list
                global matches
                matches = zip(players[::2], players[1::2]) # pairs up players and stores pairs in a tuple
                global nextround
                nextround = [None] * (len(players)//2) # how many matches there will be next round
                await ctx.send("Tournament Started")
            else:
                await ctx.send("Usage Format: (Discord Name)#(numbers)|+")

    @commands.command(name='win')
    async def win(self, ctx, name=None):
            if matches == ():
                await ctx.send("There's no tournament")
            else:
                if name in players:
                    nextround.append(name) # this has issues when players complete their matches out of order of the bracket
                    await ctx.send("Congrats {}, wait for your next match".format(name))
                else:
                    await ctx.send("You're not in the tournament")
            if None not in nextround:
                global ready
                ready = True
                await ctx.send("Next round is ready")
            elif len(nextround) == 1:
                await ctx.send("We have a winner")

    @commands.command(name='nextround_start')
    async def nextround_start(self, ctx):
        if ready == True:
            global matches
            matches = zip(nextround[::2], nextround[1::2])
            for match in matches:
                await ctx.send("@{player1} and @{player2}".format(player1 = match[0], player2
                 = match[1]))
        else:
            await ctx.send("Next round is not ready yet")




bot.add_cog(Commands())     # Adding the commands to the bot
bot.run(TOKEN)              # This runs the bot



