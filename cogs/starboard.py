# starboard.py

import discord
import aiohttp
import io
from discord.ext import commands
from db_manager import DatabaseManager
from mysql.connector import Error
from datetime import datetime

STAR_EMOJI = "⭐"
KARUTA_BOT_ID = 646937666251915264

class starboard(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db_manager = DatabaseManager()

    # Insert or update channel ID for starboard channel in database
    #   Usage: a.setstar <channel id>
    @commands.command()
    async def setstar(self, ctx):
        member = ctx.author
        if not member.guild_permissions.administrator:
            return

        current_guild = ctx.guild.id
        current_channel = ctx.message.channel.id
        try:
            query = """
            INSERT INTO server_channels (server_id, channel_id)
            VALUES (%s, %s)
            ON DUPLICATE KEY UPDATE
            channel_id = VALUES(channel_id)
            """
            self.db_manager.execute_query(query, (current_guild, current_channel))
            await ctx.send("Set current channel for Starboard drops!\nReact to any Karuta drop with ⭐ to post it here!")
        except Error as e:
            await ctx.send("An error occurred.. please contact Discord user \"vietaki\"")
            print(e)

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        # check emoji
        if str(reaction.emoji) == STAR_EMOJI:
            message = reaction.message
            current_guild = message.guild.id

            # check if the message is from karuta bot
            if message.author.id != KARUTA_BOT_ID:
                return

            # get the starboard channel ID from database
            query = "SELECT channel_id FROM server_channels WHERE server_id = %s"
            result = self.db_manager.fetch_query(query, (current_guild,))
            if result:
                STARBOARD_CHANNEL_ID = result['channel_id']

            # get the URL of the image
            image_url = message.attachments[0].url

            # get the original content of the message
            original_content = message.content

            # create the embed
            embed_description = f"{original_content}\n\n[**Jump to original message!**]({message.jump_url})"
            embed = discord.Embed(description=embed_description, color=0x3498db, timestamp=datetime.utcnow())
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
