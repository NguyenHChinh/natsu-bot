import json
import discord
import os
import asyncio
from discord.ext import commands

with open('config.json') as f:
    config = json.load(f)

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix='a!', intents=intents)


async def startup():
    for file_name in os.listdir('./cogs'):
        if file_name.endswith('.py'):
            await bot.load_extension(f'cogs.{file_name[:-3]}')
            print(f'Loaded cog.{file_name[:-3]}')


async def main():
    await startup()
    await bot.start(config["discord_token"])

@bot.command()
async def load(ctx, extension):
    try:
        await bot.load_extension(f'cogs.{extension}')
        print(f'Loaded {extension}')
    except Exception as e:
        print(f'Error loading {extension}: {e}')

@bot.command()
async def unload(ctx, extension):
    try:
        await bot.unload_extension(f'cogs.{extension}')
        print(f'Unloaded {extension}')
    except Exception as e:
        print(f'Error unloading {extension}: {e}')

@bot.command()
async def reload(ctx, extension):
    try:
        await bot.unload_extension(f'cogs.{extension}')
        await bot.load_extension(f'cogs.{extension}')
        print(f'Reloaded {extension}')
    except Exception as e:
        print(f'Error reloading {extension}: {e}')

@bot.command()
async def loadall(ctx):
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            try:
                await bot.load_extension(f'cogs.{filename[:-3]}')
                print(f'Loaded {filename[:-3]}')
            except Exception as e:
                print(f'Error loading {filename[:-3]}: {e}')

@bot.command()
async def reloadall(ctx):
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            try:
                await bot.unload_extension(f'cogs.{filename[:-3]}')
                await bot.load_extension(f'cogs.{filename[:-3]}')
                print(f'Reloaded {filename[:-3]}')
            except Exception as e:
                print(f'Error reloading {filename[:-3]}: {e}')


@bot.event
async def on_ready():
    print(f'{bot.user} is now online and ready to go!')

asyncio.run(main())
