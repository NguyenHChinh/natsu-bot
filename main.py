import json
import requests
import discord
import re
from discord.ext import commands
from discord import ui, Embed

with open('config.json') as f:
    config = json.load(f)


intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)


@bot.command()
async def ping(ctx):
    await ctx.send("pong")

@bot.command()
async def pricecheck(ctx, *args):
    # Start by checking if # of parameters is correct
    if len(args) != 2:
        await ctx.send("Please check your arguments! Reason: Invalid Number of Arguments\n" + 
            "```!pricecheck [cost reduction] [time_reduction]```")
        return
    else:
        # Creates reduction variable and verifies validity of each argument
        # Reduction varaible format will be [cost_reduction, time_reduction]
        reduction = []
        for i in args:
            i = re.sub(r'[^(0-9) + .]', '', i)
            if float(i) < 0 or float(i) > 100:
                await ctx.send("Please check your arguments! Reason: Invalid Arguments, Must Be Between 0-100" + 
                    "```!pricecheck [cost reduction] [time_reduction]```")
                return
            else:
                reduction.append(i)

    # Using lostarkmarket.online api to receive information on each items 
    url = "https://www.lostarkmarket.online/api/export-market-live/North America East"

    # TO-DO:
    # ADD/PROCESS COST OF BASE CRAFTING AND REDUCTION
    # ADD/PROCESS COST OF "Superior Oreha Fusion Material"
    # CALCULATE PROFIT AND MAXIMUM PROFIT

    parameters= {
        'items':'oreha-solar-carp-2,natural-pearl-1,fish-0,basic-oreha-fusion-material-2,superior-oreha-fusion-material-4'
        }
    payload={}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload, params=parameters)
    data = response.json()
    # data will be passed back with these values:
    # data[0] = Basic Oreha Fusion Material
    # data[1] = Fish
    # data[2] = Natural Pearl
    # data[3] = Oreha Solar Carp
    # data[4] = Superior Oreha Fusion Material
    #await ctx.send("Processed!\nCost Reduction: " + reduction[0] + "\nTime Reduction: " + reduction[1])

    embed = Embed(title="Lost Ark Fusion Material Crafting", description="")

    # Add fields to the embed
    embed.add_field(name="Oreha Solar Carp", value=data[3]['avgPrice'], inline=True)
    embed.add_field(name="Natural Pearl", value=data[2]['avgPrice'], inline=True)
    embed.add_field(name="Fish", value=data[1]['avgPrice'], inline=True)

    for i in data:
        print(i['id'])

    # Send the embed to a channel
    await ctx.send(embed=embed)


bot.run(config["token"])
