import discord
from discord.ext import commands

# Adjustable variables
print_buttons = False

class karuta_valentines(commands.Cog):
    @commands.Cog.listener()
    async def on_message(self, message):
        if ("aki " in message.content): 
            await commands.bot.process_commands(message)

        if (message.author.id != 646937666251915264):
            return

        if ('dropping' not in message.content):
            return

        channel = discord.utils.get(
            message.guild.channels, name="karuta-fiends")  # our channel

        flowers = ['🌻', '🌹', '🌼', '🌷']
        role_ids = [1073733358334513152, 1073733260573671506,
                    1073733365129297960, 1073733365867483196]

        for button in message.components:
            emojis = []
            for child in button.children:
                emoji = child.emoji.name
                emojis.append(emoji)
                if emoji in flowers:
                    print(f'FLOWER: {emoji}')
                    flower_index = flowers.index(emoji)
                    await message.channel.send(f'Hey! A <@&{role_ids[flower_index]}> dropped!')
            if (print_buttons):
                print(f'Card drop detected! Buttons: {emojis}')
            else:
                print(f'Print_buttons is off')

async def setup(bot):
    await bot.add_cog(karuta_valentines(bot))