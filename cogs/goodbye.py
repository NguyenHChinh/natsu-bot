# goodbye.py
# This file serves to host very basic commands for personal testing of bot

import discord
from discord.ext import commands

server_map = {
    # guildid1: channelid1,      # Server 1
    # guildid2: guild channel2,  # Server 2
    
    # and so on.
}

class Goodbye(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        # get channel ID for server from which member is leaving
        guild_id = member.guild.id

        # fetch channel object using guild id
        channel_id = server_map.get(guild_id)

        if channel_id:
            # fetch channel object using channel id
            channel = self.bot.get_channel(channel_id)
            
            if channel:
                # send goodbye message in the specified channel
                await channel.send(f"`{member.display_name}` just left the server")

async def setup(bot):
    await bot.add_cog(Goodbye(bot))