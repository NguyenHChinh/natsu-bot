# storedata.py

from discord.ext import commands
from db_manager import DatabaseManager

class storedata(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db_manager = DatabaseManager()

    @commands.command()
    async def mal(self, ctx, user_string: str):
        user_id = ctx.author.id
        query = "INSERT INTO user_data (user_id, user_string) VALUES (%s, %s)"
        self.db_manager.execute_query(query, (user_id, user_string))
        await ctx.send(f"Set MyAnimeList Username \"{user_string}\" for {ctx.author.mention}")

    @commands.command()
    async def checkmal(self, ctx):
        user_id = ctx.author.id
        query = "SELECT user_string FROM user_data WHERE user_id = %s"
        result = self.db_manager.fetch_query(query, (user_id,))
        if result:
            await ctx.send(f"Stored MyAnimeList Username is \"{result['user_string']}\"")
        else:
            await ctx.send("No string found for your user ID.")

async def setup(bot):
    await bot.add_cog(storedata(bot))
