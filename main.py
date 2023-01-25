import json
import requests
import discord
import re
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
    # ADD/PROCESS COST OF "Oreha Solar Carp"
    # ADD/PROCESS COST OF "Natural Pearl"
    # ADD/PROCESS COST OF "Fish"
    # ADD/PROCESS COST OF "Basic Oreha Fusion Material"
    # ADD/PROCESS COST OF "Superior Oreha Fusion Material"
    # ADD/PROCESS COST OF BASE CRAFTING AND REDUCTION
    # CALCULATE PROFIT AND MAXIMUM PROFIT

    parameters= {
        'items':'basic-oreha-fusion-material-2,fish-0'
        }
    payload={}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload, params=parameters)
    data = response.json()
    #await ctx.send(data)
    await ctx.send("Processed!\nCost Reduction: " + reduction[0] + "\nTime Reduction: " + reduction[1])

bot.run(config["token"])
