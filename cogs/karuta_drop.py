# karuta_drop.py
# This file serves to analyze dropped cards from Karuta bot
# Usage: Just have appropriate roles labeled and bot running

import discord
import requests
import time
from discord.ext import commands
from PIL import Image
from pytesseract import pytesseract

path_to_tesseract = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


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

        img_data = requests.get(message.attachments[0].url).content
        with open('karuta_drop.jpg', 'wb') as handler:
            handler.write(img_data)

        time.sleep(2)

        pytesseract.tesseract_cmd = path_to_tesseract
        img = Image.open('karuta_drop.jpg')

        cards = []

        card1 = img.crop((50, 67, 230, 105))
        cards.append(pytesseract.image_to_string(card1))

        card2 = img.crop((320, 67, 505, 105))
        cards.append(pytesseract.image_to_string(card2))

        card3 = img.crop((600, 67, 780, 105))
        cards.append(pytesseract.image_to_string(card3))
        if (img.width > 840):
            card4 = img.crop((870, 67, 1050, 105))
            cards.append(pytesseract.image_to_string(card4))

        print_message = ''
        for i in cards:
            # await message.channel.send(i)
            print_message += i
        await message.channel.send(print_message)
        print(print_message)


async def setup(bot):
    await bot.add_cog(karuta_drop(bot))
