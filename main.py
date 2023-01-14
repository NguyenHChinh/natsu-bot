import json

import discord
from discord.ext import commands

with open('config.json') as f:
    config = json.load(f)

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)


@bot.command()
async def ping(ctx):
    await ctx.send("pong")

bot.run(config["token"])
