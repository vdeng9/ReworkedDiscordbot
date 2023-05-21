import discord
import sys
from discord.ext import commands
import discord.utils
import os
import string
import asyncio
import sqlite3
import random

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
        f = open(os.path.join(sys.path[0], "textfiles\\authlink.txt"), "r")
        clientid = f.read()
        link = discord.utils.oauth_url(clientid)
        await ctx.send(link)

    @commands.is_owner()
    @commands.command(name='dlimg')
    async def dlimg(self, ctx, randomize: int = None):
        '''Downloads images from a channel'''
        image_types = ["png", "jpeg", "gif", "jpg", "mp4", "mov"]
        channel = ctx.channel
        incrementalname = 0
        def check(m):
            return m.author == ctx.author
        
        def genrngname(length):
            characters = string.ascii_letters + string.digits
            return "".join(random.choice(characters) for _ in range(length))
        
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
                                if randomize is None:
                                    await attachment.save(os.path.join(sys.path[0], f"downloaded\{attachment.filename}"))
                                elif randomize == 99:
                                    await attachment.save(os.path.join(sys.path[0], f"downloaded\{incrementalname}.{attachment.filename.split('.')[-1]}"))
                                    incrementalname += 1
                                else:
                                    rngfilename = genrngname(randomize)
                                    await attachment.save(os.path.join(sys.path[0], f"downloaded\{rngfilename}.{attachment.filename.split('.')[-1]}"))
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

    @commands.is_owner()
    @commands.command(name='a')
    async def say(self, ctx, channel:int, *messages):
        targetChannel = self.bot.get_channel(channel)
        output = ""
        for message in messages:
            output += message + " "
        await targetChannel.send(output)

    @commands.is_owner()
    @commands.command(name='mksqldb')
    async def makesqldatabase(self, ctx, dbname: str):
        '''Creates empty sql database'''
        def check(m):
            return m.author == ctx.author
        
        await ctx.send("are you sure? yes or no")
        try:
            res = await self.bot.wait_for('message', timeout=20.0, check=check)
        except asyncio.TimeoutError:
            await ctx.send("no response")
        else:
            #TODO CONSIDER ADDING DUPE CHECK TO PREVENT OVERWRITING DB 
            if res.content.lower() == "yes": 
                if os.path.exists(os.path.join(sys.path[0], "databases")):
                    conn = sqlite3.connect(os.path.join(sys.path[0], f"databases\\{dbname}.db"))
                    conn.commit()
                    conn.close()
                    await ctx.send(f"Database: {dbname}, created.")
                else:
                    os.makedirs(os.path.join(sys.path[0], "databases"))
                    await ctx.send("database folder location was missing, try again")
            elif res.content.lower() == "no":
                await ctx.send("ok...")
            else:
                await ctx.send("something happened idk try again <:worryshrug1:1097614392360698002><:worryshrug2:1097614441937371186>")

    @commands.is_owner()
    @commands.command(name="sqldbloc")
    async def sqldblocator(self, ctx, dbname: str):
        '''Locates a database'''
        testing_channel = self.bot.get_channel(1088649684358266892)
        if os.path.exists(os.path.join(sys.path[0], f"databases\\{dbname}.db")):
            conn = sqlite3.connect(os.path.join(sys.path[0], f"databases\\{dbname}.db"))
            fileloc = conn.execute("PRAGMA database_list;").fetchall()[0][2]
            await testing_channel.send(fileloc)
        else:
            await testing_channel.send("database missing")
        conn.close()

    @commands.is_owner()
    @commands.command(name='delsqldb')
    async def deletesqldatabase(self, ctx, dbname: str):
        '''Deletes sql database'''
        def check(m):
            return m.author == ctx.author
        
        await ctx.send("are you sure? yes or no")
        try:
            res = await self.bot.wait_for('message', timeout=20.0, check=check)
        except asyncio.TimeoutError:
            await ctx.send("no response")
        else:
            if res.content.lower() == "yes": 
                if os.path.exists(os.path.join(sys.path[0], f"databases\\{dbname}.db")):
                    os.remove(os.path.join(sys.path[0], f"databases\\{dbname}.db"))
                    await ctx.send(f"{dbname}, removed")
                else:
                    await ctx.send("Database doesn't exist")
            elif res.content.lower() == "no":
                await ctx.send("ok...")
            else:
                await ctx.send("something happened idk try again <:worryshrug1:1097614392360698002><:worryshrug2:1097614441937371186>")

    @commands.is_owner()
    @commands.command(name="mkreviewtable")
    async def makesqltable(self, ctx, dbname:str):
        '''Create review table in database'''
        if os.path.exists(os.path.join(sys.path[0], f"databases\\{dbname}.db")):
            conn = sqlite3.connect(os.path.join(sys.path[0], f"databases\\{dbname}.db"))
            cursor = conn.cursor()
            mktablequery = '''CREATE TABLE botreview (review TEXT, score INTEGER)'''
            insertquery = '''INSERT INTO botreview VALUES (?,?)'''
            insertdata = [("good", 0), ("bad", 0)]
            cursor.execute(mktablequery)
            cursor.executemany(insertquery, insertdata)
            conn.commit()
            conn.close()
            await ctx.send("done")
        else:
            await ctx.send("missing Database")

    @commands.is_owner()
    @commands.command(name="rigged")
    async def riggedgoodbot(self, ctx):
        '''Rigs bot review scores'''
        if os.path.exists(os.path.join(sys.path[0], f"databases\\review.db")):
            conn = sqlite3.connect(os.path.join(sys.path[0], f"databases\\review.db"))
            cursor = conn.cursor()
            cursor.execute('''SELECT * FROM botreview''')
            numbad = cursor.fetchall()
            updatequery = f'''UPDATE botreview SET score = score + {numbad[1][1]} WHERE review = "good"'''
            cursor.execute(updatequery)
            conn.commit()
            conn.close()
            await ctx.send("https://media.discordapp.net/attachments/722594694898647102/1045179474649554944/ezgif-5-a797348fe1.gif")
        else:
            await ctx.send("Missing Database")

    