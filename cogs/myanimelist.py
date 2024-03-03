# myanimelist.py
# This file serves to host an anime search function
# Usage: aki search [Anime Name]
# Example: aki search Attack on Titan
# Output: https://myanimelist.net/anime/16498/Shingeki_no_Kyojin

import httpx
import discord
import json
from discord.ext import commands

# Load the client.json file
with open('./config.json') as f:
    config = json.load(f)

class MyAnimeList(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.base_url = "https://api.myanimelist.net/v2"
        # Replace 'Your_Client_ID_here' with your actual MyAnimeList Client ID
        self.headers = {"X-MAL-CLIENT-ID": config['myanimelist_token']}

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

async def setup(bot):
    await bot.add_cog(MyAnimeList(bot))
