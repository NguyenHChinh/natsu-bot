import discord
from discord.ext import commands

# Adjustable variables
print_buttons = False
target = ['🌻', '🌹', '🌼', '🌷']
sunflower_role = 1073733358334513152
rose_role = 1073733260573671506
blossom_role = 1073733365129297960
tulip_role = 1073733365867483196
role_ids = [sunflower_role, rose_role, blossom_role, tulip_role]


class karuta_valentines(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

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

        for button in message.components:
            emojis = []
            for child in button.children:
                emoji = child.emoji.name
                emojis.append(emoji)
                if emoji in target:
                    print(f'FLOWER: {emoji}')
                    flower_index = target.index(emoji)
                    await message.channel.send(f'Hey! A <@&{role_ids[flower_index]}> dropped!')
            if (print_buttons):
                print(f'Card drop detected! Buttons: {emojis}')


async def setup(bot):
    await bot.add_cog(karuta_valentines(bot))
