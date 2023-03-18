import os
import json
import openai
import discord
from discord.ext import commands

with open('config.json') as f:
    config = json.load(f)

openai.api_key = config["openai_token"]

class ai_commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def generate_response(self, ctx, prompt: str, engine: str):
        response = openai.Completion.create(
            engine=engine,
            prompt=prompt,
            max_tokens=300,
            n=1,
            stop=None,
            temperature=0.7,
        )
        response_text = response.choices[0].text.strip()
        if len(response_text) > 2000:
            response_text = response_text[:1997] + "..."
        await ctx.send(response_text)

    @commands.command()
    async def gpt4(self, ctx, *, prompt: str):
        await self.generate_response(ctx, prompt, "text-davinci-002")

    @commands.command()
    async def gpt3(self, ctx, *, prompt: str):
        await self.generate_response(ctx, prompt, "davinci")


async def setup(bot):
    await bot.add_cog(ai_commands(bot))