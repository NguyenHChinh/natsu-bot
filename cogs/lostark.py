# oreha.py
# This file serves to host the "oreha" command
# Usage: aki oreha [cost reduction] [time reduction]
#        where cost and time reduction can be expressed as a float

import discord
import requests
import re
import math
from discord import ui, Embed, app_commands
from discord.ext import commands


class oreha(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def calculate_prices(self, ctx, reduction, data):
        show_average = 1
        show_basic = 1
        show_superior = 1

        basic_oreha_fusion_material = data[0]
        fish = data[1]
        natural_pearl = data[2]
        oreha_solar_carp = data[3]
        superior_oreha_fusion_material = data[4]
        base_basic = 205
        base_superior = 250

        basic_crafting = {'materials': [oreha_solar_carp, natural_pearl, fish],
                          'amount': [10, 40, 80],
                          'raw': base_basic,
                          'data': basic_oreha_fusion_material,
                          'output': 30,
                          'time': 45}

        superior_crafting = {'materials': [oreha_solar_carp, natural_pearl, fish],
                             'amount': [16, 64, 128],
                             'raw': base_superior,
                             'data': superior_oreha_fusion_material,
                             'output': 20,
                             'time': 60}
        
        def tax(recipe):
            tax = math.ceil(recipe['data']['avgPrice'] / 20)
            return tax

        def singleUnit(item):
            return round(item['avgPrice']) / item['amount']

        def calculateCost(recipe):
            temp_sum = 0
            for i in range(len(recipe['materials'])):
                temp_sum += singleUnit(recipe['materials']
                                       [i]) * recipe['amount'][i]

            temp_sum += round(recipe['raw'] * (1 - (float(reduction[0])/100)))
            return round(temp_sum, 2)

        def calculateProfit(recipe):
            # Return array of batch profit and unit profit
            profit = []

            # Calculate batch
            batch = (round(recipe['data']['avgPrice']) -
                     tax(recipe)) * recipe['output']
            batch -= calculateCost(recipe)
            profit.append(round(batch, 2))

            # Calculate unit
            unit = round(recipe['data']['avgPrice']) - tax(recipe)
            unit -= calculateCost(recipe) / recipe['output']
            profit.append(round(unit, 2))

            return profit

        def calculatePotential(recipe):
            time_to_cost = recipe['time'] * (1 - (reduction[1] / 100))
            batches_per_week = (10080 / time_to_cost) * 3
            potential = batches_per_week * calculateProfit(recipe)[0]
            return round(potential, 2)

        # TO DO - FINISH THIS, REMOVE OTHER THINGS
        def createMessage(recipe):
            msg = f'''```
            {recipe['amount'][0]} Oreha Solar Carp - {(singleUnit(oreha_solar_carp) * recipe['amount'][0])}
            ```'''

        embed = Embed(title="Lost Ark Fusion Material Crafting",
                      description="")
        embed.color = 0x3498db
        embed.set_thumbnail(
            url="https://cdn.discordapp.com/emojis/967248060407250954.webp?size=240&quality=lossless")

        if (show_average):
            average_prices = ''
            average_prices += '```'
            average_prices += f"Oreha Solar Carp (x10) - {round(oreha_solar_carp['avgPrice'])}g\n"
            average_prices += f"Natural Pearl (x10) - {round(natural_pearl['avgPrice'])}g\n"
            average_prices += f"Fish (x100) - {round(fish['avgPrice'])}g\n"
            average_prices += f"Basic Oreha Fusion Material (x1) - {round(basic_oreha_fusion_material['avgPrice'])}g\n"
            average_prices += f"Superior Oreha Fusion Material (x1) - {round(superior_oreha_fusion_material['avgPrice'])}g\n"
            average_prices += '```'
            embed.add_field(name="**Prices Used in Calculation**",
                            value=average_prices, inline=False)

        if (show_basic):
            craft_basic = "```\n"
            craft_basic += "10 Oreha Solar Carp - " + \
                str(singleUnit(oreha_solar_carp) * 10) + 'g\n'
            craft_basic += "40 Natural Pearl - " + \
                str(singleUnit(natural_pearl) * 40) + 'g\n'
            craft_basic += "80 Fish - " + \
                str(round((singleUnit(fish) * 80), 2)) + 'g\n'
            craft_basic += "Raw Gold - " + str(round(base_basic *
                                                     (100-(reduction[0]))/100)) + 'g (' + str(reduction[0]) + '% reduction)\n'
            craft_basic += '\nSum Cost (Batch/Unit): ' + str(calculateCost(
                basic_crafting)) + 'g/' + str(round((calculateCost(basic_crafting) / 30), 2)) + 'g\n'
            craft_basic += "Profit (Batch/Unit): " + \
                str(calculateProfit(basic_crafting)[0]) + "g/"
            craft_basic += str(calculateProfit(basic_crafting)[1]) + 'g\n'
            craft_basic += "\nPotential Profit Per Week: " + \
                str(calculatePotential(basic_crafting)) + 'g```'

            embed.add_field(name="**Basic Oreha Fusion Material Calculation**",
                            value=craft_basic, inline=False)

        if (show_superior):
            craft_superior = "```\n"
            craft_superior += "16 Oreha Solar Carp - " + \
                str(singleUnit(oreha_solar_carp) * 16) + 'g\n'
            craft_superior += "64 Natural Pearl - " + \
                str(singleUnit(natural_pearl) * 64) + 'g\n'
            craft_superior += "128 Fish - " + \
                str(round((singleUnit(fish) * 128), 2)) + 'g\n'
            craft_superior += "Raw Gold - " + str(round(base_superior *
                                                        (100-(reduction[0]))/100)) + 'g (' + str(reduction[0]) + '% reduction)\n'
            craft_superior += '\nSum Cost (Batch/Unit): ' + str(calculateCost(
                superior_crafting)) + 'g/' + str(round((calculateCost(superior_crafting) / 20), 2)) + 'g\n'
            craft_superior += "Profit (Batch/Unit): " + \
                str(calculateProfit(superior_crafting)[0]) + "g/"
            craft_superior += str(calculateProfit(superior_crafting)
                                  [1]) + 'g\n'
            craft_superior += "\nPotential Profit Per Week: " + \
                str(calculatePotential(superior_crafting)) + 'g```'
            embed.set_footer(
                text="NOTE: Potential profit does NOT include great sucesses!")

            embed.add_field(name="**Superior Oreha Fusion Material Calculation**",
                            value=craft_superior, inline=False)

        # Send the embed to the channel
        await ctx.send(embed=embed)
        print("Successfully executed price check!")

    @commands.command()
    async def oreha(self, ctx, *args):
        # Make sure channel is correct
        if (ctx.channel.id != 1073043279664386208):
            message = ctx.message
            await message.delete()
            return

        # Argument Checks for Any # Of Parameters
        reduction = []
        if len(args) == 0:
            reduction.append(0)
            reduction.append(0)
        elif (len(args) < 3):
            # Creates reduction variable and verifies validity of each argument
            # Reduction varaible format will be [cost_reduction, time_reduction
            for i in args:
                # Processing argument to only number value (remove %)
                i = re.sub(r'[^(0-9) + .]', '', i)
                if float(i) < 0 or float(i) > 100:  # Invalid Response
                    await ctx.send("```Please check your arguments!\nReason: Invalid Arguments, Must Be [0-100)```")
                    return
                else:  # Valid Response
                    reduction.append(float(i))

            if len(reduction) == 1:  # No specified time reduction
                reduction.append(0)
            else:  # There IS a specified time reduction
                if (reduction[1] == 100):
                    await ctx.send('```Please check your arguments!\nReason: Time reduction cannot be 100%')
                    return

        else:
            await ctx.send("```Please check your arguments! Reason: Invalid Arguments\n\n" +
                           "Correct Command Usage: pricecheck [cost reduction] [time reduction]```")
            return

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

        print(f'Data: {data}')
        print(f'Reduction: {reduction}')
        await self.calculate_prices(ctx, reduction, data)

    # TO-DO: Once I have the time, remove this function completely
    #        oreha command will have buttons that you can click and edit the
    #        prices manually and it will automatically edit the original message.
    @commands.command()
    async def manual(self, ctx, *args):
        if len(args) != 7:
            await ctx.send("Invalid Input. This command is VERY experimental so please do it this way:\n" +
                           "`aki manual [basic oreha] [fish] [natural pearl] [oreha solar carp] [superior oreha] [cost reduction] [time reduction]`")
            return
        
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

        # for i in range(5):
        #     data[i]['avgPrice'] = args[i]

        reduction = [float(args[5]), float(args[6])]
        print(f'Data: {data}')
        print(f'Reduction: {reduction}')

        await self.calculate_prices(ctx, reduction, data)

async def setup(bot):
    await bot.add_cog(oreha(bot))
