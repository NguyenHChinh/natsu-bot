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
bot = commands.Bot(command_prefix='', intents=intents)


@bot.command()
async def ping(ctx):
    await ctx.send("pong")


@bot.command()
async def pricecheck(ctx, *args):
    # Start by checking if # of parameters is correct
    argument_check = 1
    if (argument_check):
        if len(args) < 1:
            await ctx.send("Please check your arguments! Reason: Invalid Number of Arguments\n" +
                           "```!pricecheck [cost reduction] [time_reduction (optional)]```")
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
    # CALCULATE PROFIT AND MAXIMUM PROFIT
    # CLEAN UP EMBED

    parameters = {
        'items': 'oreha-solar-carp-2,natural-pearl-1,fish-0,basic-oreha-fusion-material-2,superior-oreha-fusion-material-4'
    }
    payload = {}
    headers = {}

    response = requests.request(
        "GET", url, headers=headers, data=payload, params=parameters)
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

    basic_crafting = {'materials': [oreha_solar_carp, natural_pearl, fish],
                      'amount': [10, 40, 80],
                      'raw': base_basic}

    superior_crafting = {'materials': [oreha_solar_carp, natural_pearl, fish],
                         'amount': [16, 64, 128],
                         'raw': base_superior}

    embed = Embed(title="Lost Ark Fusion Material Crafting", description="")
    embed.color = 0x3498db
    embed.set_thumbnail(
        url="")
    # Add fields to the embed
    average_prices = "```\n"
    average_prices += "Oreha Solar Carp (x10) - " + \
        str(round(oreha_solar_carp['avgPrice'])) + 'g\n'
    average_prices += "Natural Pearl (x10) - " + \
        str(round(natural_pearl['avgPrice'])) + 'g\n'
    average_prices += "Fish (x100) - " + str(round(fish['avgPrice'])) + 'g\n'
    average_prices += "Basic Oreha Fusion Material (x1): - " + str(
        round(basic_oreha_fusion_material['avgPrice'])) + 'g\n'
    average_prices += "Superior Oreha Fusion Material (x1) - " + str(
        round(superior_oreha_fusion_material['avgPrice'])) + 'g```\n\n'

    embed.add_field(name=" ", value=" ", inline=False)

    embed.add_field(name="**Prices Used in Calculation**",
                    value=average_prices, inline=False)

    def singleUnit(item):
        return round(item['avgPrice']) / item['amount']

    def calculateCost(recipe):
        temp_sum = 0
        for i in range(len(recipe['materials'])):
            temp_sum += singleUnit(recipe['materials']
                                   [i]) * recipe['amount'][i]

        temp_sum += round(recipe['raw'] * (1 - (float(args[0])/100)))
        return temp_sum

    crafting_operation_basic = "```\n"
    crafting_operation_basic += "10 Oreha Solar Carp - " + \
        str(singleUnit(oreha_solar_carp) * 10) + 'g\n'
    crafting_operation_basic += "40 Natural Pearl - " + \
        str(singleUnit(natural_pearl) * 40) + 'g\n'
    crafting_operation_basic += "80 Fish - " + \
        str(round((singleUnit(fish) * 80), 2)) + 'g\n'
    crafting_operation_basic += "Raw Gold - " + \
        str(round(base_basic *
            (100-(float(args[0])))/100)) + 'g (' + args[0] + '% reduction)\n'
    crafting_operation_basic += '\nSum (Total/Per Unit): ' + str(calculateCost(
        basic_crafting)) + 'g/' + str(round((calculateCost(basic_crafting) / 30), 2)) + 'g```\n'

    craft_superior = "```\n"
    craft_superior += "16 Oreha Solar Carp - " + \
        str(singleUnit(oreha_solar_carp) * 16) + 'g\n'
    craft_superior += "64 Natural Pearl - " + \
        str(singleUnit(natural_pearl) * 64) + 'g\n'
    craft_superior += "128 Fish - " + \
        str(round((singleUnit(fish) * 128), 2)) + 'g\n'
    craft_superior += "Raw Gold - " + str(round(base_superior *
                                                (100-(float(args[0])))/100)) + 'g (' + args[0] + '% reduction)\n'
    craft_superior += '\nSum (Total/Per Unit): ' + str(calculateCost(
        superior_crafting)) + 'g/' + str(round((calculateCost(superior_crafting) / 20), 2)) + 'g```\n'

    embed.add_field(name="**Crafting Costs for Basic Oreha Fusion Material**",
                    value=crafting_operation_basic, inline=False)

    embed.add_field(name="**Crafting Costs for Superior Oreha Fusion Material**",
                    value=craft_superior, inline=False)

    # Send the embed to a channel
    await ctx.send(embed=embed)


@ bot.command()
async def fuck(ctx, *args):
    if (len(args) > 1):
        if (args[0] == "you" or args[0] == "u"):
            messagexd = re.sub(r'[^(a-zA-Z)]', '', str(args[1]))
            await ctx.send("yeah fuck you " + messagexd)

bot.run(config["token"])
