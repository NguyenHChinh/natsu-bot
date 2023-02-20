import json
import discord
import os
import asyncio
from discord.ext import commands

with open('config.json') as f:
    config = json.load(f)

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='aki ', intents=intents)

async def load():
    for file_name in os.listdir('./cogs'):
        if file_name.endswith('.py'):
            await bot.load_extension(f'cogs.{file_name[:-3]}')
            print(f'Loaded cog.{file_name[:-3]}')

async def main():
    await load()
    await bot.start(config["token"])

# bot.run(config["token"])
asyncio.run(main())