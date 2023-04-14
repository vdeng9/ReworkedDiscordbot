import discord
import sys
from discord.ext import commands, tasks
import discord.utils
import os, sys

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
        '''Shuts down the bot'''
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
        '''Gets authentication link for joining servers'''
        f = open(os.path.join(sys.path[0], "authlink.txt"), "r")
        clientid = f.read()
        link = discord.utils.oauth_url(clientid)
        await ctx.send(link)

    @commands.is_owner()
    @commands.command(name='dlimg')
    async def dlimg(self, ctx):
        '''Downloads images from a channel'''
        image_types = ["png", "jpeg", "gif", "jpg"]
        channel = ctx.channel
        async for message in channel.history():
            for attachment in message.attachments:
                if any(attachment.filename.lower().endswith(image) for image in image_types):
                    await attachment.save(os.path.join(sys.path[0], f"downloaded\{attachment.filename}"))
        await ctx.send("done!")
