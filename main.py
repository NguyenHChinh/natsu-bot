import json
import requests
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

@bot.command()
async def pricecheck(ctx):
    url = "https://www.lostarkmarket.online/api/export-market-live/North America East"

    parameters= {'items':'basic-oreha-fusion-material-2'}
    payload={}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload, params=parameters)
    data = response.json()
    basic_oreha = data[0]

    await ctx.send("Price of Oreha: " + str(round(basic_oreha["avgPrice"])))

bot.run(config["token"])
