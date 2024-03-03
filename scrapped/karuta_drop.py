# karuta_drop.py
# This file serves to analyze dropped cards from Karuta bot
# Usage: Just have appropriate roles labeled and bot running

import discord
import requests
import time
import json
import os
import asyncio
import platform
from discord.ext import commands
from PIL import Image

if (platform.system() == 'Windows'):
    path_to_tesseract = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    pytesseract.tesseract_cmd = path_to_tesseract

json_file = "counts.json"

if os.path.exists(json_file):
    with open(json_file, "r") as f:
        counts = json.load(f)
else:
    counts = {}

class karuta_drop(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if ("aki " in message.content):
            await commands.bot.process_commands(message)

        if (message.author.id != 646937666251915264):
            return

        target_channel = 1111547887839608842  # whisper in Aki's Academy
        if message.channel.id == target_channel:
            original_message = await message.channel.fetch_message(message.reference.message_id)
            original_username = original_message.author

            user_id = str(original_username.id)

            counts[user_id] = counts.get(user_id, 0) + 1

            # save the counts back to the json file
            with open(json_file, "w") as f:
                json.dump(counts, f)
            
            print(f'{original_username} just used a Karuta command in #whisper LMFAO')
            my_reply = await original_message.reply(f'Hey, {original_message.author.name}. You\'re in the wrong channel :) In fact, you\'ve done this {counts[user_id]} times')
            await asyncio.sleep(3)
            await message.delete()
            await original_message.delete()
            await my_reply.delete()
            return

        if ('dropping' not in message.content):
            return

        channel = discord.utils.get(
            message.guild.channels, name="karuta-fiends")  # our channel

        output_dir = os.path.join(os.getcwd(), 'cogs', 'temp')
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        karuta_drop_path = os.path.join(output_dir, 'karuta_drop.jpg')
        img_data = requests.get(message.attachments[0].url).content
        with open(karuta_drop_path, 'wb') as handler:
            handler.write(img_data)

        time.sleep(2)

        pytesseract.tesseract_cmd = path_to_tesseract
        img = Image.open(karuta_drop_path)

        cards = []
        top = 67
        bottom = 105
        card1 = img.crop((50, top, 230, bottom))
        cards.append(pytesseract.image_to_string(card1))
        card1.convert('RGB').save(os.path.join(output_dir, 'card1.jpg'))

        card2 = img.crop((320, top, 505, bottom))
        cards.append(pytesseract.image_to_string(card2))
        card2.convert('RGB').save(os.path.join(output_dir, 'card2.jpg'))

        card3 = img.crop((600, top, 780, bottom))
        cards.append(pytesseract.image_to_string(card3))
        card3.convert('RGB').save(os.path.join(output_dir, 'card3.jpg'))

        if (img.width > 840):
            card4 = img.crop((870, top, 1050, bottom))
            cards.append(pytesseract.image_to_string(card4))
            card4.convert('RGB').save(os.path.join(output_dir, 'card4.jpg'))

        print_message = ''
        for i in cards:
            print_message += i
        # await message.channel.send(print_message)
        print(print_message)


async def setup(bot):
    await bot.add_cog(karuta_drop(bot))
