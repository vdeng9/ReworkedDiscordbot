import discord
from discord.ext import commands


class musicplugin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="musictest")
    async def test(self, ctx):
        await ctx.send("Hello from music.py")