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
        print(f"register was called by {discID}")
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
            cursor.execute('''SELECT id FROM economy''')
            results = cursor.fetchall()
            print("results:" + str(results))
            conn.close()
        else:
            await ctx.send("Missing database")

    #no longer needed but ima keep it incase future testing is need for watever reason
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