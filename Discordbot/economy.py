import discord
import sys
from discord.ext import commands
import discord.utils
import os
import asyncio
import requests
import sqlite3
import random
import datetime
from threading import Thread
from time import sleep

def checkReg(discID: int):
    if os.path.exists(os.path.join(sys.path[0], f"databases\\econ.db")):
        x = 0
        conn = sqlite3.connect(os.path.join(sys.path[0], f"databases\\econ.db"))
        cursor = conn.cursor()
        cursor.execute('''SELECT id FROM economy''')
        results = cursor.fetchall()
        for x in range(len(results)):
            if discID == results[x][0]: 
                return True
        return False

def startrefresher():
    while True:
        midnightrefresh()
        sleep(60)
        
def midnightrefresh():
    # normalize daily to reset at midnight est for all users
    midnight = (datetime.datetime.now() - datetime.datetime.now().replace(hour=0, minute=0, second=0)).total_seconds()
    return midnight

Thread(target=startrefresher).start() 

class economyplugin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.is_owner()
    @commands.command(name='economytest')
    async def hello(self, ctx):
        await ctx.send("hello! from economy.py")

    @commands.command(name='register')
    async def registation(self, ctx):
        '''Registers user to the Shademare12 economy system'''
        discID = ctx.message.author.id # discord IDs are unique as of rn 5/30/23
        #print(f"register was called by {discID}")
        if os.path.exists(os.path.join(sys.path[0], f"databases\\econ.db")):
            x = 0
            registeredcheck = False 
            conn = sqlite3.connect(os.path.join(sys.path[0], f"databases\\econ.db"))
            cursor = conn.cursor()
            cursor.execute('''SELECT id FROM economy''')
            results = cursor.fetchall()
            while x < len(results): # TODO replace with checkReg() at some point
                if discID == results[x][0]:
                    await ctx.send("you are already registered")
                    registeredcheck = True
                    break
                x = x + 1
            if registeredcheck == False:
                cursor.executemany('INSERT INTO economy VALUES (?,?)', [(discID, 50)])
                conn.commit()
                await ctx.send("you are now registered here is 50 pekos to start off with <:PekoSmug:797748881642356756>")
            #cursor.execute('''SELECT id FROM economy''')
            #results = cursor.fetchall()
            #print("results:" + str(results))
            conn.close()
        else:
            await ctx.send("Missing database")


    midnight = midnightrefresh()
    @commands.cooldown(1, 24*60*60 - midnight, commands.BucketType.user)
    @commands.command(name='daily')
    async def daily(self, ctx):
        '''Daily pekos'''
        discID = ctx.message.author.id
        x = 0
        discUser = await self.bot.fetch_user(discID)
        #print(discUser)
        #print(discID)
        if os.path.exists(os.path.join(sys.path[0], f"databases\\econ.db")):
            conn = sqlite3.connect(os.path.join(sys.path[0], f"databases\\econ.db"))
            cursor = conn.cursor()
            cursor.execute('''SELECT id FROM economy''')
            results = cursor.fetchall()
            #print(len(results))
            for x in range(len(results)):
                if discID == results[x][0]: 
                    cursor.execute(f'''UPDATE economy SET pekos = pekos + 50 WHERE id = {discID}''')
                    conn.commit()
                    conn.close()
                    pekosembed = discord.Embed(title="Daily", description="<:PekoSmug:797748881642356756>", color=0x80FFFF)
                    pekosembed.add_field(name="pekos",value="+50")
                    pekosembed.set_author(name=str(discUser))
                    await ctx.send(embed=pekosembed)
                    break
                elif x >= len(results)-1:
                    await ctx.send("You might not be registered")
                    ctx.command.reset_cooldown(ctx)
            #print(x)
        else:
            await ctx.send("Missing database")

    @commands.cooldown(1,3,commands.BucketType.user)
    @commands.command(name='pekos')
    async def checkpekos(self, ctx, member: discord.User = None):
        '''Checks how much pekos you have or someone else has
        !pekos | !pekos [member]'''
        if member is None:
            discID = ctx.message.author.id
            if not checkReg(discID=discID):
                await ctx.send("You might not be registered")
                return
        else:
            discID = member.id
            if not checkReg(discID=discID):
                await ctx.send("They might not be registered")
                return
        discUser = await self.bot.fetch_user(discID)
        if os.path.exists(os.path.join(sys.path[0], f"databases\\econ.db")):
            conn = sqlite3.connect(os.path.join(sys.path[0], f"databases\\econ.db"))
            cursor = conn.cursor()
            cursor.execute(f'''SELECT pekos FROM economy WHERE id = {discID}''')
            result = cursor.fetchall()
            pekosembed = discord.Embed(title="Check", description="<:PekoSmug:797748881642356756>", color=0x80FFFF)
            pekosembed.add_field(name="pekos", value=result[0][0])
            pekosembed.set_author(name=str(discUser))
            await ctx.send(embed=pekosembed)
        else:
            await ctx.send("Missing database")

    rngcd = random.randint(10,20) 
    @commands.cooldown(1, rngcd, commands.BucketType.user)
    @commands.command(name='gamba')
    async def gamba(self, ctx, amount: int):
        '''Gamble your pekos
        !gamba [amount]'''
        discID = ctx.message.author.id
        if not checkReg(discID=discID):
            await ctx.send("You might not be registered")
            return
        def check(m):
            return m.author == ctx.author
        multiplierOptions = ["2x", "3x", "5x"]
        outcomes = ["win", "lose"]
        twoxweights = [.5, .5]
        threexweights = [.3, .7]
        fivexweights = [.1, .9]
        if os.path.exists(os.path.join(sys.path[0], f"databases\\econ.db")):
            conn = sqlite3.connect(os.path.join(sys.path[0], f"databases\\econ.db"))
            cursor = conn.cursor()
            cursor.execute(f'''SELECT * FROM economy WHERE id = {discID}''')
            results = cursor.fetchall()
            if amount > results[0][1]:
                await ctx.send("You do not have enough pekos!!!")
                return
            if amount < 1:
                await ctx.send("You can't gamble 0 or negative pekos!!!")
                return
            await ctx.send(f"What multiplier? {multiplierOptions}")
            try:
                res = await self.bot.wait_for('message', timeout=10.0, check=check)
            except asyncio.TimeoutError:
                await ctx.send("no response")
            else:
                #print(res.content)
                #print(type(res.content))
                if res.content.lower() == multiplierOptions[0]:
                    gambaresult = random.choices(outcomes, twoxweights)
                    #print(gambaresult[0])
                    if gambaresult[0] == "win":
                        cursor.execute(f'''UPDATE economy SET pekos = pekos + {amount} WHERE id = {discID}''')
                        conn.commit()
                        conn.close()
                        await ctx.send(f"You won {2*amount}!!!")
                    else:
                        cursor.execute(f'''UPDATE economy SET pekos = pekos - {amount} WHERE id = {discID}''')
                        conn.commit()
                        conn.close()
                        await ctx.send(f"You lost {amount}!!!")
                elif res.content.lower() == multiplierOptions[1]:
                    gambaresult = random.choices(outcomes, threexweights)
                    #print(gambaresult[0])
                    if gambaresult[0] == "win":
                        cursor.execute(f'''UPDATE economy SET pekos = pekos + {2*amount} WHERE id = {discID}''')
                        conn.commit()
                        conn.close()
                        await ctx.send(f"You won {3*amount}!!!")
                    else:
                        cursor.execute(f'''UPDATE economy SET pekos = pekos - {amount} WHERE id = {discID}''')
                        conn.commit()
                        conn.close()
                        await ctx.send(f"You lost {amount}!!!")
                elif res.content.lower() == multiplierOptions[2]:
                    gambaresult = random.choices(outcomes, fivexweights)
                    #print(gambaresult[0])
                    if gambaresult[0] == "win":
                        cursor.execute(f'''UPDATE economy SET pekos = pekos + {4*amount} WHERE id = {discID}''')
                        conn.commit()
                        conn.close()
                        await ctx.send(f"You won {5*amount}!!!")
                    else:
                        cursor.execute(f'''UPDATE economy SET pekos = pekos - {amount} WHERE id = {discID}''')
                        conn.commit()
                        conn.close()
                        await ctx.send(f"You lost {amount}!!!")
                else:
                    await ctx.send("Not a valid option")
            conn.close() # I dont actually know if this close is needed but its here incase it is
        else:
            await ctx.send("Missing database")

    @commands.command(name="lb", aliases=["leaderboard"])
    async def leaderboard(self, ctx):
        '''Leaderboard'''
        x = 0
        if os.path.exists(os.path.join(sys.path[0], f"databases\\econ.db")):
            conn = sqlite3.connect(os.path.join(sys.path[0], f"databases\\econ.db"))
            cursor = conn.cursor()
            cursor.execute('''SELECT * FROM economy ORDER BY pekos DESC''')
            results = cursor.fetchall()
            resultembed = discord.Embed(title="Leaderboard")
            while x < len(results):
                rank = x + 1
                resultembed.add_field(name=f"#{rank} {str(await self.bot.fetch_user(results[x][0]))}", value=f"{results[x][1]} pekos", inline=True)
                x += 1
            await ctx.send(embed=resultembed)

    @commands.command(name="give")
    async def givepekos(self, ctx, receiver: discord.User, amount: int):
        '''Gives pekos to someone
        !give [receiver] [amount]'''
        discID = ctx.message.author.id
        rdiscID = receiver.id
        if not checkReg(discID=discID):
            await ctx.send("You might not be registered")
            return
        elif not checkReg(discID=rdiscID):
            await ctx.send("The receiver might not be registered")
            return
        discName = await self.bot.fetch_user(discID)
        if discID == rdiscID:
            await ctx.send("You can't give yourself pekos")
            return
        if amount <= 0:
            await ctx.send("You can't give zero or negative pekos")
            return
        if os.path.exists(os.path.join(sys.path[0], f"databases\\econ.db")):
            conn = sqlite3.connect(os.path.join(sys.path[0], f"databases\\econ.db"))
            cursor = conn.cursor()
            cursor.execute(f'''SELECT * FROM economy WHERE id = {discID}''')
            results = cursor.fetchall()
            #print(results)
            if results[0][1] < amount:
                await ctx.send(f"You don't have enough pekos to give {amount}")
            else:
                cursor.execute(f'''UPDATE economy SET pekos = pekos + {amount} WHERE id = {rdiscID}''')
                cursor.execute(f'''UPDATE economy SET pekos = pekos - {amount} WHERE id = {discID}''')
                conn.commit()
                conn.close()
                await ctx.send(f"{discName} gave {receiver} {amount} pekos")
        else:
            await ctx.send("Missing database")

    @commands.cooldown(1,3)
    @commands.command(name="gacha")
    async def waifugacha(self, ctx, mode:str = None):
        '''Roll for a waifu image 50 pekos per roll
        !gacha | !gacha nsfw'''
        discID = ctx.message.author.id
        if not checkReg(discID=discID):
            await ctx.send("You might not be registered")
            return
        if mode is None:
            baseurl = "http://api.waifu.im/search/?&is_nsfw=false"
        elif mode.lower() == "nsfw":
            baseurl = "http://api.waifu.im/search/?&is_nsfw=true"
            if not ctx.channel.is_nsfw():
                await ctx.send("Not a nsfw channel")
                return
        else:
            await ctx.send("Bad arguments")
            return
        if os.path.exists(os.path.join(sys.path[0], f"databases\\econ.db")):
            conn = sqlite3.connect(os.path.join(sys.path[0], f"databases\\econ.db"))
            cursor = conn.cursor()
            cursor.execute(f'''SELECT * FROM economy WHERE id = {discID}''')
            results = cursor.fetchall()
            if results[0][1] < 50:
                await ctx.send("You do not have enough pekos")
                return
            cursor.execute(f'''UPDATE economy SET pekos = pekos - 50 WHERE id = {discID}''')
            conn.commit()
            conn.close()
            waifuJSON = requests.get(baseurl).json()
            waifuimage = waifuJSON['images'][0]['url']
            await ctx.send(waifuimage)
        else:
            await ctx.send("Missing database")

    @commands.cooldown(1,10*60,commands.BucketType.user)
    @commands.command(name="steal")
    async def stealpekos(self, ctx, target: discord.User, amount: int):
        '''Steal up to 2x pekos you own
        !steal [target] [amount]'''
        discID = ctx.message.author.id
        tdiscID = target.id
        discName = await self.bot.fetch_user(discID)
        if not checkReg(discID=discID):
            await ctx.send("You might not be registered")
            ctx.command.reset_cooldown(ctx)
            return
        if not checkReg(discID=tdiscID):
            await ctx.send("They might not be registered")
            ctx.command.reset_cooldown(ctx)
            return
        if discID == tdiscID:
            await ctx.send("Can't steal from yourself....")
            return
        stealoutcomes = ["steal", "fail", "L"]
        stealweights = [.33, .60, .07]
        #stealresult = random.choices(stealoutcomes, stealweights)
        #print(stealresult)
        if os.path.exists(os.path.join(sys.path[0], f"databases\\econ.db")):
            x = 0
            conn = sqlite3.connect(os.path.join(sys.path[0], f"databases\\econ.db"))
            cursor = conn.cursor()
            cursor.execute(f'''SELECT * FROM economy WHERE id = {discID}''')
            initresults = cursor.fetchall()
            cursor.execute(f'''SELECT * FROM economy WHERE id = {tdiscID}''')
            tarresults = cursor.fetchall()
            #print(initresults)
            #print(tarresults)
            if initresults[0][1] < 1:
                await ctx.send("You must own at least 1 peko to steal")
                ctx.command.reset_cooldown(ctx)
                return
            if tarresults[0][1] < 1:
                await ctx.send("They must own at least 1 peko to steal")
                ctx.command.reset_cooldown(ctx)
                return
            if amount <= 2*initresults[0][1]:
                if amount <= tarresults[0][1]:
                    stealresult = random.choices(stealoutcomes, stealweights)
                    #print(stealresult)
                    if stealresult[0] == "steal":                            
                        cursor.execute(f'''UPDATE economy SET pekos = pekos + {amount} WHERE id = {discID}''')
                        cursor.execute(f'''UPDATE economy SET pekos = pekos - {amount} WHERE id = {tdiscID}''')
                        conn.commit()
                        conn.close()
                        await ctx.send(f"{discName} stole {amount} from {target}")
                    elif stealresult[0] == "fail":
                        await ctx.send(f"{discName} failed to steal from {target} <:PepelaughW:674427223574446092>")
                    elif stealresult[0] == "L":
                        cursor.execute(f'''UPDATE economy SET pekos = 0 WHERE id = {discID}''')
                        conn.commit()
                        conn.close()
                        await ctx.send(f"While trying to steal from {target}, {discName} tripped and fell dropping all their pekos <:PepelaughW:674427223574446092>")
                else:
                    await ctx.send(f"They do not have {amount} pekos")
                    ctx.command.reset_cooldown(ctx)
            else:
                await ctx.send("You can't steal more than 2 times the amount of pekos you own")
                ctx.command.reset_cooldown(ctx)

    #no longer needed but ima keep it incase future testing is needed for watever reason
    #@commands.is_owner()
    #@commands.command()
    #async def testuser(self, ctx):
    #    '''Test user for economy system'''
    #    if os.path.exists(os.path.join(sys.path[0], f"databases\\econ.db")):
    #        conn = sqlite3.connect(os.path.join(sys.path[0], f"databases\\econ.db"))
    #        cursor = conn.cursor()
    #        cursor.executemany('''INSERT INTO economy VALUES (?,?)''', [(1,50)])
    #        conn.commit()
    #        conn.close()
    #    else:
    #        await ctx.send("Missing database")
