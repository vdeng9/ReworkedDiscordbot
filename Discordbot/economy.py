import discord
import sys
from discord.ext import commands
import discord.utils
import os
import string
import asyncio
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
                    await ctx.send(embed=pekosembed)
                    break
                elif x >= len(results)-1:
                    await ctx.send("You might not be registered")
                    ctx.command.reset_cooldown(ctx)
            #print(x)
        else:
            await ctx.send("Missing database")

    @commands.command(name='pekos')
    async def checkpekos(self, ctx, member: discord.User = None):
        '''Checks how much pekos you have or someone else has'''
        if member is None:
            discID = ctx.message.author.id
        else:
            discID = member.id
        if os.path.exists(os.path.join(sys.path[0], f"databases\\econ.db")):
            conn = sqlite3.connect(os.path.join(sys.path[0], f"databases\\econ.db"))
            cursor = conn.cursor()
            cursor.execute(f'''SELECT pekos FROM economy WHERE id = {discID}''')
            result = cursor.fetchall()
            pekosembed = discord.Embed(title="Check", description="<:PekoSmug:797748881642356756>", color=0x80FFFF)
            pekosembed.add_field(name="pekos", value=result[0][0])
            await ctx.send(embed=pekosembed)
        else:
            await ctx.send("Missing database")

    @commands.command(name='gamba')
    async def gamba(self, ctx, amount: int):
        discID = ctx.message.author.id
        x = 0
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
                            amount *= 2
                            cursor.execute(f'''UPDATE economy SET pekos = pekos + {amount} WHERE id = {discID}''')
                            conn.commit()
                            conn.close()
                            await ctx.send(f"You won {amount}!!!")
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
                            amount *= 3
                            cursor.execute(f'''UPDATE economy SET pekos = pekos + {amount} WHERE id = {discID}''')
                            conn.commit()
                            conn.close()
                            await ctx.send(f"You won {amount}!!!")
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
