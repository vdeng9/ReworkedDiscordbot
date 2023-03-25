import discord
import os
import sys
import asyncio
from discord.ext import commands
import random

vtubers = [["Omaru Polka", "https://www.youtube.com/@OmaruPolka"], ["Ceres Fauna", "https://www.youtube.com/@CeresFauna"], ["Nanashi Mumei", "https://www.youtube.com/@NanashiMumei"], ["Usada Pekora", "https://www.youtube.com/@UsadaPekora"], ["Sakamata Chloe", "https://www.youtube.com/@SakamataChloe"],
           ["Laplus Darknesss", "https://www.youtube.com/@LaplusDarknesss"], ["Hakui Koyori", "https://www.youtube.com/@HakuiKoyori"], ["Yukihana Lamy", "https://www.youtube.com/@YukihanaLamy"], ["Momosuzu Nene", "https://www.youtube.com/@MomosuzuNene"], ["Shishiro Botan", "https://www.youtube.com/@ShishiroBotan"],
           ["Kazama Iroha", "https://www.youtube.com/@KazamaIroha"], ["Gawr Gura", "https://www.youtube.com/@GawrGura"], ["Watson Amelia", "https://www.youtube.com/@WatsonAmelia"], ["Minato Aqua", "https://www.youtube.com/@MinatoAqua"], ["Shirakami Fubuki", "https://www.youtube.com/@ShirakamiFubuki"]]

class basicplugin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.is_owner()
    @commands.command(name='basictest')
    async def test(self, ctx):
        await ctx.send("hello! from basic.py")

    @commands.command()
    async def add(self, ctx, *args):
        totalsum = 0
        #print(type(totalsum))
        for num in args:
            #print(type(num))
            convertedStrToFloat = float(num)
            totalsum += convertedStrToFloat
        #print(type(totalsum))
        await ctx.send(totalsum)

    @commands.command()
    async def mul(self, ctx, *args):
        totalproduct = 1
        for num in args:
            convertedStrToFloat = float(num)
            totalproduct *= convertedStrToFloat
        await ctx.send(totalproduct)

    @commands.command()
    async def exp(self, ctx, base:float, exponent:float):
        solution = base ** exponent
        await ctx.send(solution)

    @commands.command()
    async def watch(self, ctx):
        vtuber, vtuberurl = random.choice(vtubers)
        await ctx.send("vtuber: " + vtuber)
        await ctx.send("vtuber url: " + vtuberurl)
        await self.bot.change_presence(activity=discord.Activity(name=vtuber, type=discord.ActivityType.watching, url=vtuberurl), status="dnd")

    @commands.command(name="clearstatus")
    async def clearstat(self, ctx):
        await self.bot.change_presence(activity=None, status=None)