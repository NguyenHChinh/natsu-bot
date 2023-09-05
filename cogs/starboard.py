# starboard.py

import discord
import aiohttp
import io
from discord.ext import commands

STAR_EMOJI = "⭐"
KARUTA_BOT_ID = 646937666251915264
STARBOARD_CHANNEL_ID = 1034310939635372132

class starboard(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        print(reaction.emoji)
        print(reaction.message)

        # check emoji
        if str(reaction.emoji) == STAR_EMOJI:
            message = reaction.message

            # check if the message is from karuta bot
            if message.author.id != KARUTA_BOT_ID:
                return

            # get the URL of the image
            image_url = message.attachments[0].url

            # get the original content of the message
            original_content = message.content

            # create the embed
            embed_description = f"{original_content}\n\n[**Jump to original message!**]({message.jump_url})"
            embed = discord.Embed(description=embed_description, color=0x3498db)
            embed.set_footer(text=f"Starred by {user.name}")

            # fetch the image using aiohttp
            async with aiohttp.ClientSession() as session:
                async with session.get(image_url) as resp:
                    image_data = await resp.read()

            # create a file object for the image
            image_data_io = io.BytesIO(image_data)
            image_file = discord.File(image_data_io, filename="starboard_image.webp")

            # send the image as an attachment and the embed to the starboard channel
            starboard_channel = self.bot.get_channel(STARBOARD_CHANNEL_ID)
            await starboard_channel.send(file=image_file, embed=embed)

async def setup(bot):
    await bot.add_cog(starboard(bot))
