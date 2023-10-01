# coinflip.py
# Just a barebones coinflip command

import discord
from discord.ext import commands
import random

class CoinFlip(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def coinflip(self, ctx):
        result = random.choice(['Heads', 'Tails'])
        await ctx.send(result)

async def setup(bot):
    await bot.add_cog(CoinFlip(bot))
