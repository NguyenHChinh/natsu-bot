# myanimelist.py
# This file serves to host features relating to MyAnimeList

import discord
import httpx
import json
from discord.ext import commands
from db_manager import DatabaseManager
from mysql.connector import Error
from discord import ui, Embed, app_commands

# Load the client.json file
with open('./config.json') as f:
    config = json.load(f)

class myanimelist(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.base_url = "https://api.myanimelist.net/v2"
        self.headers = {"X-MAL-CLIENT-ID": config['myanimelist_token']}
        self.db_manager = DatabaseManager()


    # Search Feature
    #   Usage: a.search [Anime Name]
    #   Example: a.search Attack on Titan
    #   Output: https://myanimelist.net/anime/16498/Shingeki_no_Kyojin
    @commands.command()
    async def search(self, ctx, *, query):
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.base_url}/anime", params={"q": query, "limit": 1}, headers=self.headers)
            if response.status_code == 200:
                data = response.json()
                if data.get("data"):
                    anime = data["data"][0]["node"]
                    await ctx.send(f"<https://myanimelist.net/anime/{anime['id']}/{anime['title'].replace(' ', '_')}>")
                else:
                    await ctx.send("No results found.")
            else:
                await ctx.send("Failed to fetch data from MyAnimeList.")


    # Insert or update entry in MyAnimeList user table in database
    #   Usage: a.setmal <username>
    #   Example: a.setmal "Bobby"
    #   Output: Set MyAnimeList Username "Bobby" for @Bobby
    @commands.command()
    async def setmal(self, ctx, user_string: str):
        user_id = ctx.author.id
        try:
            query = """
            INSERT INTO user_data (user_id, user_string) 
            VALUES (%s, %s) 
            ON DUPLICATE KEY UPDATE 
            user_string = VALUES(user_string)
            """
            self.db_manager.execute_query(query, (user_id, user_string))
            await ctx.send(f"Set MyAnimeList Username \"{user_string}\" for {ctx.author.mention}")
        except Error as e:
            await ctx.send("An error occurred while setting your username.")
            print(e)


    # Retrieve value from MyAnimeList user table in database
    #   Usage: a.getmal
    #   Example: a.getmal
    #   Output: Set MyAnimeList Username is "Bobby"
    #   Error Output: No MyAnimeList Username stored. Set with a.setmal <name>
    @commands.command()
    async def getmal(self, ctx):
        user_id = ctx.author.id
        query = "SELECT user_string FROM user_data WHERE user_id = %s"
        result = self.db_manager.fetch_query(query, (user_id,))
        if result:
            await ctx.send(f"Set MyAnimeList Username is \"{result['user_string']}\"")
        else:
            await ctx.send("No MyAnimeList Username stored. Set with a.setmal <name>")


    # Pull MyAnimeList User List -- WIP
    #   Usage: a.mylist
    #   Example: a.mylist
    # TODO: Since embed can't store the whole message, implement buttons to flip through "pages"
    @commands.command()
    async def mylist(self, ctx):
        user_id = ctx.author.id
        query = "SELECT user_string FROM user_data WHERE user_id = %s"
        result = self.db_manager.fetch_query(query, (user_id,))
        user_string = result['user_string']

        if not user_string:
            await ctx.send("You have not set a MyAnimeList username. Use the command to set your username first.")
            return

        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.base_url}/users/{user_string}/animelist", params={"fields": "list_status", "limit": 25}, headers=self.headers)
            if response.status_code == 200:
                data = response.json()
                if data.get("data"):
                    embed = discord.Embed(title=f"{user_string}'s Anime List", description="Here are the titles:", color=discord.Color.blue())
                    for anime in data['data']:
                        anime_title = anime['node']['title']
                        anime_score = anime['list_status']['score']

                        embed.add_field(name=anime_title, value=anime_score, inline=False)  # Using "•" as a placeholder value

                    await ctx.send(embed=embed)
                else:
                    await ctx.send(f"{user_string}'s anime list could not be found or is empty.")
            else:
                await ctx.send("Failed to fetch the anime list from MyAnimeList.")

    @commands.command()
    async def animelist(self, ctx, user: discord.User):
        user_id = user.id
        query = "SELECT user_string FROM user_data WHERE user_id = %s"
        result = self.db_manager.fetch_query(query, (user_id,))
        user_string = result['user_string']

        if not user_string:
            await ctx.send("That user has not set a MyAnimeList username. They can set their username by doing `setmal <name>`.")
            return

        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.base_url}/users/{user_string}/animelist", params={"fields": "list_status", "limit": 25}, headers=self.headers)
            if response.status_code == 200:
                data = response.json()
                if data.get("data"):
                    embed = discord.Embed(title=f"{user_string}'s Anime List", description="Here are the titles:", color=discord.Color.blue())
                    for anime in data['data']:
                        anime_title = anime['node']['title']
                        anime_score = anime['list_status']['score']

                        embed.add_field(name=anime_title, value=anime_score, inline=False)  # Using "•" as a placeholder value

                    await ctx.send(embed=embed)
                else:
                    await ctx.send(f"{user_string}'s anime list could not be found or is empty.")
            else:
                await ctx.send("Failed to fetch the anime list from MyAnimeList.")


async def setup(bot):
    await bot.add_cog(myanimelist(bot))
