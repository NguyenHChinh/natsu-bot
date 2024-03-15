# storedata.py

from discord.ext import commands
from db_manager import DatabaseManager
from mysql.connector import Error  # Make sure to import Error

class storedata(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db_manager = DatabaseManager()

    @commands.command()
    async def mal(self, ctx, user_string: str):
        user_id = ctx.author.id
        try:
            query = """
            INSERT INTO user_data (user_id, user_string) 
            VALUES (%s, %s) 
            ON DUPLICATE KEY UPDATE 
            user_string = VALUES(user_string)
            """
            self.db_manager.execute_query(query, (user_id, user_string))
            await ctx.send(f"Stored \"{user_string}\" for {ctx.author.mention}")
        except Error as e:
            await ctx.send("An error occurred while storing your data.")
            print(e)


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
