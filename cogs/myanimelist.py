# myanimelist.py
# This file serves to host an anime search function
# Usage: aki search [Anime Name]
# Example: aki search Attack on Titan
# Output: https://myanimelist.net/anime/16498/Shingeki_no_Kyojin

import discord
from discord.ext import commands


class myanimelist(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def search(self, ctx):
        # TO-DO
        print('TO DO')


async def setup(bot):
    await bot.add_cog(myanimelist(bot))
