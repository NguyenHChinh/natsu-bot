import discord
from discord.ext import commands

class essential(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'Successfully loaded all cogs! {self.bot.user} is now online!')

    @commands.command()
    async def ping(self, ctx):
        # Basic ping command
        await ctx.send("Pong")

    @commands.command()
    async def test(self, ctx):
        # Checks to see if user who called this is me (Aki#1005)
        if (ctx.author.id != 202872300968607745):
            return

        await ctx.send("Test!")

async def setup(bot):
    await bot.add_cog(essential(bot))