# delete_msgs.py:
# This file serves to delete messages in bulk

# Importing required libraries
import discord
import json
from discord.ext import commands

# Load the client.json file
with open('./config.json') as f:
    config = json.load(f)

confirm_emoji = "✅"
print_updates = False

class delete_msgs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def delete(self, ctx, number: int):
        # Ensure that the user is admin
        if ctx.author.id != config['discord_admin_id']:
            return await ctx.send("You do not have permission to use this command.")

        # Check the number of messages to delete
        if number <= 0:
            return await ctx.send("The number of messages to delete should be greater than zero.")

        # Fetch messages
        try:
            if (print_updates):
                print("About to fetch messages...")
            messages = [msg async for msg in ctx.channel.history(limit=number+1)]
            if (print_updates):
                print(f"Number of messages fetched: {len(messages)}")
        except Exception as e:
            if (print_updates):
                print(f"An error occurred while fetching messages: {e}")
            return await ctx.send(f"An error occurred: {e}")

        cutoff_msg_content = messages[-1].content if messages else None

        # If there is no "cutoff" message, inform the user
        if not cutoff_msg_content:
            return await ctx.send("Couldn't find a cutoff message. Maybe the channel has less history than you specified?")

        # Send a confirmation message and add the emoji
        confirm_msg = await ctx.send(f"`{cutoff_msg_content}` and messages after will be deleted. React with {confirm_emoji} to confirm.")
        await confirm_msg.add_reaction(confirm_emoji)

        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) == confirm_emoji

        try:
            reaction, user = await self.bot.wait_for('reaction_add', timeout=60.0, check=check)
        except TimeoutError:
            await ctx.send('Delete operation timed out.')
        else:
            # Delete messages (plus two: one for the command and one for the confirmation message)
            deleted = await ctx.channel.purge(limit=number + 2)
            msg = await ctx.send(f"Deleted {len(deleted) - 2} messages.")
            await msg.delete(delay=5)

async def setup(bot):
    await bot.add_cog(delete_msgs(bot))
