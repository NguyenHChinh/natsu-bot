# karuta_drop.py
# This file serves to analyze dropped cards from Karuta bot
# Usage: Just have appropriate roles labeled and bot running

import discord
import requests
from discord.ext import commands

class karuta_drop(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if ("aki " in message.content):
            await commands.bot.process_commands(message)

        if (message.author.id != 646937666251915264):
            return

        if ('dropping' not in message.content):
            return

        channel = discord.utils.get(
            message.guild.channels, name="karuta-fiends")  # our channel

        print(channel)
        print(message.attachments[0].url)
        img_data = requests.get(message.attachments[0].url).content
        with open('karuta_drop.jpg', 'wb') as handler:
            handler.write(img_data)

async def setup(bot):
    await bot.add_cog(karuta_drop(bot))
