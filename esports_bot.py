import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
import re


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='!')  # Bot commands designated by !
bot.remove_command("help")              # Removes the default help command.



class Commands(commands.Cog):    # Class storing all the commands of the bot
    @commands.command(name='hello')
    async def hello(self, ctx):
        name = ctx.author.name
        await ctx.send("Hello {}!".format(name))

    @commands.command(name='start-t')
    async def start(self, ctx, brackets=None): # brackets in the form
        if brackets == None:
            await ctx.send("Usage Format: Discord Name#(numbers)|+")
        else:
            if re.match("^([a-zA-z]+#[0-9][0-9][0-9][0-9]/)+([a-zA-z]+#[0-9][0-9][0-9][0-9])$", brackets):
                players = brackets.split("/")
                matches = zip(players[::2], players[1::2])


            else:
                await ctx.send("Usage Format: Discord Name#(numbers)|+")



bot.add_cog(Commands())     # Adding the commands to the bot
bot.run(TOKEN)              # This runs the bot



