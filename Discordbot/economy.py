import discord
import sys
from discord.ext import commands
import discord.utils
import os
import string
import requests
import sqlite3
import random

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
            while x < len(results):
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

    @commands.cooldown(1, 24*60*60, commands.BucketType.user)
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
        '''Checks how much pekos you have or someone else has'''
        if member is None:
            discID = ctx.message.author.id
        else:
            discID = member.id
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

    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.command(name='gamba')
    async def gamba(self, ctx, amount: int):
        '''Gamble your pekos'''
        discID = ctx.message.author.id
        x = 0
        startAmount = amount
        if os.path.exists(os.path.join(sys.path[0], f"databases\\econ.db")):
            conn = sqlite3.connect(os.path.join(sys.path[0], f"databases\\econ.db"))
            cursor = conn.cursor()
            cursor.execute('''SELECT * FROM economy''')
            results = cursor.fetchall()
            for x in range(len(results)):
                if discID == results[x][0]: 
                    if amount > results[x][1]:
                        await ctx.send("You don't have enough pekos")
                        break
                    if amount < 1:
                        await ctx.send("Can't bet zero or negative pekos")
                        break
                    if amount <= 50:
                        wincon = random.randint(1,100)
                        if wincon >= 50:
                            cursor.execute(f'''UPDATE economy SET pekos = pekos + {amount} WHERE id = {discID}''')
                            conn.commit()
                            conn.close()
                            await ctx.send(f"You won {2*startAmount}!!!")
                            break
                        else:
                            cursor.execute(f'''UPDATE economy SET pekos = pekos - {amount} WHERE id = {discID}''')
                            conn.commit()
                            conn.close()
                            await ctx.send(f"You lost {amount}!!!")
                            break
                    elif amount > 50:
                        wincon = random.randint(1,100)
                        if wincon >= 90:
                            amount *= 2
                            cursor.execute(f'''UPDATE economy SET pekos = pekos + {amount} WHERE id = {discID}''')
                            conn.commit()
                            conn.close()
                            await ctx.send(f"You won {3*startAmount}!!!")
                            break
                        else:
                            cursor.execute(f'''UPDATE economy SET pekos = pekos - {amount} WHERE id = {discID}''')
                            conn.commit()
                            conn.close()
                            await ctx.send(f"You lost {amount}!!!")
                            break
                elif x >= len(results)-1:
                    await ctx.send("You might not be registered")
                    ctx.command.reset_cooldown(ctx)
        else:
            await ctx.send("Missing database")

    @commands.command(name="lb")
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
                resultembed.add_field(name=str(await self.bot.fetch_user(results[x][0])), value=f"{results[x][1]} pekos", inline=False)
                x += 1
            await ctx.send(embed=resultembed)

    @commands.command(name="give")
    async def givepekos(self, ctx, receiver: discord.User, amount: int):
        '''Gives pekos to someone'''
        discID = ctx.message.author.id
        rdiscID = receiver.id
        discName = await self.bot.fetch_user(discID)
        if discID == rdiscID:
            await ctx.send("You can't give yourself pekos")
            return
        if amount < 0:
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
                await ctx.send(f"{discName.mention} gave {receiver.mention} {amount} pekos")
        else:
            await ctx.send("Missing database")

    @commands.cooldown(1,3)
    @commands.command(name="gacha")
    async def waifugacha(self, ctx, mode:str = None):
        '''Roll for a waifu image 50 pekos per roll'''
        discID = ctx.message.author.id
        if mode is None:
            baseurl = "http://api.waifu.im/search/?&is_nsfw=false"
        elif mode.lower() == "nsfw":
            baseurl = "http://api.waifu.im/search/?&is_nsfw=true"
            if not ctx.channel.is_nsfw():
                await ctx.send("Not a nsfw channel")
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
