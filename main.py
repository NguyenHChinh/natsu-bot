import json
import requests
import discord
import re
from discord.ext import commands
from discord import ui, Embed, app_commands

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
    basic_oreha_fusion_material = data[0]
    fish = data[1]
    natural_pearl = data[2]
    oreha_solar_carp = data[3]
    superior_oreha_fusion_material = data[4]
    base_basic = 205
    base_superior = 250

    basic_crafting = {'materials':[oreha_solar_carp, natural_pearl, fish],
                      'amount':[10, 40, 80],
                      'raw':base_basic}

    superior_crafting = {'materials':[oreha_solar_carp, natural_pearl, fish],
                    'oreha_solar_carp':10,
                    'natural_pearl':40,
                    'fish':80,
                    'raw':base_superior}

    #await ctx.send("Processed!\nCost Reduction: " + reduction[0] + "\nTime Reduction: " + reduction[1])

    embed = Embed(title="Lost Ark Fusion Material Crafting", description="")
    embed.color = 0x3498db
    # Add fields to the embed
    average_prices = ""
    average_prices += "Oreha Solar Carp (x10) - " + str(round(oreha_solar_carp['avgPrice'])) + 'g\n'
    average_prices += "Natural Pearl (x10) - " + str(round(natural_pearl['avgPrice'])) + 'g\n'
    average_prices += "Fish (x100) - " + str(round(fish['avgPrice'])) + 'g\n'
    average_prices += "Basic Oreha Fusion Material (x1): - " + str(round(basic_oreha_fusion_material['avgPrice'])) + 'g\n'
    average_prices += "Superior Oreha Fusion Material (x1) - " + str(round(superior_oreha_fusion_material['avgPrice'])) + 'g\n'

    embed.add_field(name="**Prices Used in Calculation**", value=average_prices, inline=False)

    def singleUnit(item):
        return round(item['avgPrice']) / item['amount']

    def calculateCost(recipe):
        temp_sum = 0
        for i in range(len(recipe['materials'])):
            temp_sum += singleUnit(recipe['materials'][i]) * recipe['amount'][i]

        temp_sum += recipe['raw']
        return temp_sum

    crafting_operation = ""
    crafting_operation += "10 Oreha Solar Carp - " + str(singleUnit(oreha_solar_carp) * 10) + 'g\n'
    crafting_operation += "40 Natural Pearl - " + str(singleUnit(natural_pearl) * 40) + 'g\n'
    crafting_operation += "80 Fish - " + str(singleUnit(fish) * 80) + 'g\n'
    crafting_operation += "Base Crafting Cost - " + str(base_basic) + 'g\n'
    crafting_operation += '\nSum: ' + str(calculateCost(basic_crafting)) + 'g\n'

    embed.add_field(name="**Crafting Costs**", value=crafting_operation, inline=False)

    # embed.add_field(name="Oreha Solar Carp", value=round(oreha_solar_carp['avgPrice']), inline=False)
    # embed.add_field(name="Natural Pearl", value=round(natural_pearl['avgPrice']), inline=False)
    # embed.add_field(name="Fish", value=round(fish['avgPrice']), inline=False)
    # embed.add_field(name="Basic Oreha Fusion Material", value=round(basic_oreha_fusion_material['avgPrice']), inline=False)
    # embed.add_field(name="Superior Oreha Fusion Material", value=round(superior_oreha_fusion_material['avgPrice']), inline=False)

    # await ctx.send("Oreha Solar Carp" + str(oreha_solar_carp))
    # await ctx.send("Natural Pearl: " + str(natural_pearl))
    # await ctx.send("Fish: " + str(fish))
    # await ctx.send("Basic Oreha Fusion Material: " + str(basic_oreha_fusion_material))
    # await ctx.send("Superior Oreha Fusion Material: " + str(superior_oreha_fusion_material))



    # Send the embed to a channel
    await ctx.send(embed=embed)


bot.run(config["token"])
