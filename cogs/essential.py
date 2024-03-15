# essential.py
# This file serves to host very basic commands for testing of bot as well as a template for new cogs

# Importing required libraries
import discord
import json
from discord.ext import commands

# Load the client.json file
with open('./config.json') as f:
    config = json.load(f)

class essential(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx):
        # Basic ping command
        await ctx.send("Pong")

    @commands.command()
    async def amiadmin(self, ctx):
        # Checks to see if user who called 
        if (ctx.author.id != config['discord_admin_id']):
            return

        await ctx.send("Yes, you are set as admin.")


async def setup(bot):
    await bot.add_cog(essential(bot))
