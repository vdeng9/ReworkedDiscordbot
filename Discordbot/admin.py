import discord
import sys
from discord.ext import commands
import discord.utils
import os
import re
import asyncio

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
        image_types = ["png", "jpeg", "gif", "jpg", "mp4", "mov"]
        channel = ctx.channel
        def check(m):
            return m.author == ctx.author
        
        await ctx.send("are you sure? yes or no")
        try:
            res = await self.bot.wait_for('message', timeout=20.0, check=check)
        except asyncio.TimeoutError:
            await ctx.send("no response")
        else:
            if res.content.lower() == "yes": 
                if os.path.exists(os.path.join(sys.path[0], "downloaded")):
                    await ctx.send("downloading...")
                    async for message in channel.history():
                        for attachment in message.attachments:
                            if any(attachment.filename.lower().endswith(image) for image in image_types):
                                await attachment.save(os.path.join(sys.path[0], f"downloaded\{attachment.filename}"))
                    await ctx.send("done!")
                else:
                    os.makedirs(os.path.join(sys.path[0], "downloaded"))
                    await ctx.send("download folder location was missing, try again")
            elif res.content.lower() == "no":
                await ctx.send("ok...")
            else:
                await ctx.send("something happened idk try again <:worryshrug1:1097614392360698002><:worryshrug2:1097614441937371186>")

    @commands.is_owner()
    @commands.command(name="delmsg")
    async def delmsg(self, ctx, limit:int):
        '''Deletes messages'''
        #yayreplies = re.compile(r"^(?:y(?:es)?|1)$") cant use regex for some reason :(
        #nayreplies = re.compile(r"^(?:n(?:o)?|1)$")
        res = "" 
        
        def check(m):
            return m.author == ctx.author
        
        await ctx.send("are you sure? yes or no")
        try:
            res = await self.bot.wait_for('message', timeout=20.0, check=check)
        except asyncio.TimeoutError:
            await ctx.send("no response")
        else:
            if res.content.lower() == "yes":
                await ctx.send("dont send messages while deleting is in process or dont idc tbh <:worryshrug1:1097614392360698002><:worryshrug2:1097614441937371186> this is very slow tho wait for confirmation \"deleted x message(s)\" message <:PepelaughW:674427223574446092>")
                await asyncio.sleep(5)
                deleted = await ctx.channel.purge(limit=limit+4, bulk=True)
                await ctx.send(f"deleted {len(deleted)-4} message(s)")
            elif res.content.lower() == "no":
                await ctx.send("ok...")
            else:
                await ctx.send("something happened idk try again <:PepelaughW:674427223574446092>")

    @commands.is_owner()
    @commands.command(name="spam")
    async def spammsg(self, ctx, limit:int):
        '''Opposite of delete'''
        counter = 0
        while counter < limit:
            counter = counter+1
            await ctx.send(counter)
            