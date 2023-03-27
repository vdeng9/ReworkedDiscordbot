import discord
import os
import sys
from discord.ext import commands, tasks
import discord.utils
import time

class adminplugin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.is_owner()
    @commands.command(name='test')
    async def hello(self, ctx):
        await ctx.send("hello! from admin.py")
        await self.bot.change_presence(activity=discord.Game(name="Testing"), status="idle")

    @commands.is_owner()
    @commands.command(name='shutdown')
    async def shutdown(self, ctx):
        await ctx.send("shutting down...")
        sys.exit("shutting down")

    #discord.py discord server says this is not ideal just manual restart
    #@commands.command(name='restart')
    #async def restart(self, ctx):
    #    await ctx.send("restarting please wait...")
    #    os.execv(sys.executable, sys.executable + sys.argv)
    
    @commands.is_owner()
    @commands.command(name='link')
    async def authlink(self, ctx):
        f = open(r'C:\Users\Victor\Desktop\Projects\Discordbot\authlink.txt', 'r')
        clientid = f.read()
        link = discord.utils.oauth_url(clientid)
        await ctx.send(link)

    