# karuta_wrongchannel.py
# This file used to analyze dropped cards from Karuta bot
# Now, it just deletes messages and counts how many times someone drops outside of specific channel
# Usage: Just have appropriate roles labeled and bot running

import discord
import requests
import time
import json
import os
import asyncio
import platform
from discord.ext import commands

json_file = "counts.json"

if os.path.exists(json_file):
    with open(json_file, "r") as f:
        counts = json.load(f)
else:
    counts = {}

class karuta_wrongchannel(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if ("aki " in message.content):
            await commands.bot.process_commands(message)

        if (message.author.id != 646937666251915264):
            return

        target_channels = {
            970386541811753040,  # whisper in Aki's Academy
            1111547887839608842,   # general in Aki's Academy
            1195904130317820016,     # random-dump
            1053519286720790558,     # content
            1198743071597285479,     # palworld-enjoyers
            1188035997523521546,     # nerd-shit
            1176396440629694534,     # lethal-clips
            1176262666424164502     # lethal-modded
        }
        if message.channel.id in target_channels:
            original_message = await message.channel.fetch_message(message.reference.message_id)
            original_username = original_message.author

            user_id = str(original_username.id)

            counts[user_id] = counts.get(user_id, 0) + 1

            # save the counts back to the json file
            with open(json_file, "w") as f:
                json.dump(counts, f)
            
            print(f'{original_username} just used a Karuta command in the wrong channel LMFAO')
            my_reply = await original_message.reply(f'Hey, {original_message.author.name}. You\'re in the wrong channel :) In fact, you\'ve done this {counts[user_id]} times')
            await asyncio.sleep(3)
            await message.delete()
            await original_message.delete()
            await my_reply.delete()
            return

        if ('dropping' not in message.content):
            return


async def setup(bot):
    await bot.add_cog(karuta_wrongchannel(bot))
