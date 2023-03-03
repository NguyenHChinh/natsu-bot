# myanimelist.py
# This file serves to host an anime search function
# Usage: aki search [Anime Name]
# Example: aki search Attack on Titan
# Output: https://myanimelist.net/anime/16498/Shingeki_no_Kyojin

import discord
import requests
from discord.ext import commands
from bs4 import BeautifulSoup


class myanimelist(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def search(self, ctx, *args):
        print('search function executed')

        site = 'myanimelist.net'
        query = ''
        for index, word in enumerate(args):
            query = query + word
            if index < (len(args) - 1):
                query = query + '+'

        url = f"https://www.google.com/search?q={query}+site:{site}"
        print(url)
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
        results = soup.find_all("div", class_="g")

        if results:
            for result in results:
                link = result.find("a")["href"]
                if site in link:
                    await ctx.send(f'<{link}>')
                    break
            else:
                print(f"No results found on {site}")
        else:
            print("No results found")


async def setup(bot):
    await bot.add_cog(myanimelist(bot))
