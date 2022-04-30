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

class Commands(commands.Cog):    # Class storing all the commands of the bot
    @commands.command(name='hello')
    async def hello(self, ctx):
        name = ctx.author.name
        await ctx.send("Hello {}!".format(name))

    @commands.command(name='start-t')
    async def start(self, ctx, brackets=None):
        if brackets == None:
            await ctx.send("Usage Format: Discord Name#(numbers)|+")
        else:
            if re.match("^([a-zA-z]+#[0-9][0-9][0-9][0-9]/)+([a-zA-z]+#[0-9][0-9][0-9][0-9])$", brackets):
                global players
                players = brackets.split("/")
                global matches
                matches = zip(players[::2], players[1::2])
                global nextround
                nextround = [None] * (len(players)/2)
                await ctx.send("Tournament Started")
            else:
                await ctx.send("Usage Format: Discord Name#(numbers)|+")

    @commands.command(name='win')
    async def start(self, ctx, name=None):
            if matches == ():
                await ctx.send("There's no tournament")
            else:
                if players.index(name):
                    nextround.append(name)
                    await ctx.send("Congrats {}, wait for your next match".format(name))
                else:
                    await ctx.send("You're not in the tournament")
            if None not in nextround:
                await ctx.send("Next round is ready")




bot.add_cog(Commands())     # Adding the commands to the bot
bot.run(TOKEN)              # This runs the bot



