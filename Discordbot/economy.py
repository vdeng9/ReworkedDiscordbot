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

    def customcd(message):
        cd = 24*60*60 - (datetime.datetime.now() - datetime.datetime.now().replace(hour=0,minute=0,second=0)).total_seconds()
        return commands.Cooldown(1, cd)

    @commands.dynamic_cooldown(customcd, commands.BucketType.user)
    @commands.command(name='daily')
    async def daily(self, ctx):
        '''Daily pekos
        !daily
        Treasurebox = [50, 100, 500, 1000, 5000, 10000]'''
        discID = ctx.message.author.id
        discUser = await self.bot.fetch_user(discID)
        #print(discUser)
        #print(discID)
        treasurebox = [50, 100, 500, 1000, 5000, 10000]
        boxweights = [.80625, .10, .05, .025, .0125, .00625]
        if os.path.exists(os.path.join(sys.path[0], f"databases\\econ.db")):
            conn = sqlite3.connect(os.path.join(sys.path[0], f"databases\\econ.db"))
            cursor = conn.cursor() 
            if checkReg(discID):
                amount = random.choices(treasurebox, boxweights)
                cursor.execute(f'''UPDATE economy SET pekos = pekos + {amount[0]} WHERE id = {discID}''')
                conn.commit()
                conn.close()
                pekosembed = discord.Embed(title="Daily", description="<:PekoSmug:797748881642356756>", color=0x80FFFF)
                pekosembed.add_field(name="pekos",value=f"+{amount[0]}")
                pekosembed.set_author(name=str(discUser))
                await ctx.send(embed=pekosembed)
            else:
                await ctx.send("You might not be registered, !register to register")
                ctx.command.reset_cooldown(ctx)
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
                await ctx.send("You might not be registered, !register to register")
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
    async def gamba(self, ctx, amount: int, multiplier: str = None):
        '''Gamble your pekos
        !gamba [amount] [multiplier]'''
        discID = ctx.message.author.id
        if not checkReg(discID=discID):
            await ctx.send("You might not be registered, !register to register")
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
            if multiplier is not None:
                if multiplier == "2x" or multiplier == "2":
                    gambaresult = random.choices(outcomes, twoxweights)
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
                elif multiplier == "3x" or multiplier == "3":
                    gambaresult = random.choices(outcomes, threexweights)
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
                elif multiplier == "5x" or multiplier == "5":
                    gambaresult = random.choices(outcomes, fivexweights)
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
                    await ctx.send(f"Invalid Multiplier")
            else:
                await ctx.send(f"What multiplier? {multiplierOptions}")
                try:
                    res = await self.bot.wait_for('message', timeout=10.0, check=check)
                except asyncio.TimeoutError:
                    await ctx.send("no response")
                else:
                    #print(res.content)
                    #print(type(res.content))
                    if res.content.lower() == multiplierOptions[0] or res.content.lower() == "2":
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
                    elif res.content.lower() == multiplierOptions[1] or res.content.lower() == "3":
                        gambaresult = random.choices(outcomes, threexweights)
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
                    elif res.content.lower() == multiplierOptions[2] or res.content.lower() == "5":
                        gambaresult = random.choices(outcomes, fivexweights)
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
            await ctx.send("You might not be registered, !register to register")
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
            await ctx.send("You might not be registered, !register to register")
            return
        if mode is None:
            baseurl = "https://api.waifu.im/search/?is_nsfw=false"
        elif mode.lower() == "nsfw":
            baseurl = "https://api.waifu.im/search/?is_nsfw=true"
            if not ctx.channel.is_nsfw():
                await ctx.send("Not a nsfw channel")
                return
        else:
            raise commands.BadArgument
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
            await ctx.send("You might not be registered, !register to register")
            ctx.command.reset_cooldown(ctx)
            return
        if not checkReg(discID=tdiscID):
            await ctx.send("They might not be registered")
            ctx.command.reset_cooldown(ctx)
            return
        if discID == tdiscID:
            await ctx.send("Can't steal from yourself....")
            return
        # Mutual Assured Money feelsokayman
        stealoutcomes = ["steal", "fail", "L", "MAD", "MAM"]
        stealweights = [.35, .60, .04, .005, .005]
        #stealweights = [0, 0, 0, 0, 1] # testweights
        #stealresult = random.choices(stealoutcomes, stealweights)
        #print(stealresult)
        if os.path.exists(os.path.join(sys.path[0], f"databases\\econ.db")):
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
            if amount <= 3*initresults[0][1]:
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
                        await ctx.send(f"While trying to steal from {target}, {discName} tripped and fell dropping all {initresults[0][1]} of their pekos <:PepelaughW:674427223574446092>")
                    elif stealresult[0] == "MAD":
                        cursor.execute(f'''UPDATE economy SET pekos = 0 WHERE id = {discID}''')
                        cursor.execute(f'''UPDATE economy SET pekos = 0 WHERE id = {tdiscID}''')
                        conn.commit()
                        conn.close()
                        await ctx.send(f"{discName} tried to steal from {target} but {target} realized and fought back. They both punched the air for an hour while hobo bot Shademare12 stole {initresults[0][1]} pekos from {discName} and {tarresults[0][1]} pekos from {target}")
                        await ctx.send("<:worryhobo:1119108746652688494>")
                    elif stealresult[0] == "MAM":
                        cursor.execute(f'''UPDATE economy SET pekos = pekos + {amount} WHERE id = {discID}''')
                        cursor.execute(f'''UPDATE economy SET pekos = pekos + {amount} WHERE id = {tdiscID}''')
                        conn.commit()
                        conn.close()
                        await ctx.send(f"{discName} stole {amount} from {target}")
                        await ctx.send(f"While walking a hobo walked up to {target} and handed them {amount} pekos. \"This shit is worthless, take it!\" yelled the hobo as he walked away")
                        await ctx.send("<:worryhobo:1119108746652688494>")
                else:
                    await ctx.send(f"They do not have {amount} pekos")
                    ctx.command.reset_cooldown(ctx)
            else:
                await ctx.send("You can't steal more than 3 times the amount of pekos you own")
                ctx.command.reset_cooldown(ctx)
        else:
            await ctx.send("Missing database")

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command()
    async def slots(self, ctx, amount: int):
        '''Slots
        !slots [amount]
        2 matches = 3x, 3 matches = 20x, 1 jackpot = 3x, 1 jackpot and 2 matches = 5x, 2 jackpot = 5x, 3 jackpot = !bank'''
        discID = ctx.message.author.id
        #test = ["<a:hutaoCash:1118473906915917935>"] # for testing 3 jackpots cuz realistically testing for it would be so rare...
        slotschar = ["<a:intoTheAyayaLand:1045225606352220190>", "<a:polkaSpin:797750618466287636>", "<:PekoSmug:797748881642356756>",
                    "<:painpeko:854652380158230528>", "<:whenlifegetsscuffed:933325588003967056>", "<:FaunaStare:1074027074391646278>",
                    "<:oddowo:741191279945449532>", "<:smadge:1039443341038850109>", "<a:rainbowpls:703162735256535120>",
                    "<a:HazmatMutsuki:786756436964933692>", "<a:ROWOW:704438082631630988>", "<:AYAYA:649470611843710976>", 
                    "<a:hutaoCash:1118473906915917935>"]
        if not checkReg(discID=discID):
            await ctx.send("You might not be registered, !register to register")
            ctx.command.reset_cooldown(ctx)
            return
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
            cursor.execute(f'''UPDATE economy SET pekos = pekos - {amount} WHERE id = {discID}''')
            cursor.execute(f'''UPDATE bank SET pekos = pekos + {amount} WHERE id = "slots"''')
            conn.commit()
            cursor.execute(f'''SELECT * FROM bank WHERE id = "slots"''')
            bank = cursor.fetchall()
            #print(bank[0][0], bank[0][1])
            slotsresults = random.choices(slotschar, k=3)
            await ctx.send("Slots Results!!!")
            await ctx.send(f"{slotsresults[0]} {slotsresults[1]} {slotsresults[2]}")
            #print(slotsresults[0], slotsresults[1], slotsresults[2])
            #print(type(slotsresults[0]), type(slotsresults[1]), type(slotsresults[2]))
            # print(1 == 1 == 1) returns true
            if slotsresults[0] == slotsresults[1] == slotsresults[2]:
                if slotsresults[0] == "<a:hutaoCash:1118473906915917935>":
                    cursor.execute(f'''UPDATE economy SET pekos = pekos + {bank[0][1]} WHERE id = {discID}''')
                    cursor.execute(f'''UPDATE bank SET pekos = 0 WHERE id = "slots"''')
                    conn.commit()
                    slotsembed = discord.Embed(title="Slots", description="JACKPOT!!!", color=0xFF0000)
                    slotsembed.add_field(name="pekos",value=f"+{bank[0][1]}")
                    await ctx.send(embed=slotsembed)
                    await ctx.send("<a:hutaoCash:1118473906915917935>")
                else:
                    cursor.execute(f'''UPDATE economy SET pekos = pekos + {20*amount} WHERE id = {discID}''')
                    conn.commit()
                    slotsembed = discord.Embed(title="Slots", description="3 Matches!!!", color=0xFF0000)
                    slotsembed.add_field(name="pekos",value=f"+{20*amount}")
                    await ctx.send(embed=slotsembed)
                    await ctx.send("<:Poggie:674427373440991232>")
            elif slotsresults[0] == slotsresults[1] == "<a:hutaoCash:1118473906915917935>" or slotsresults[1] == slotsresults[2] == "<a:hutaoCash:1118473906915917935>" or slotsresults[0] == slotsresults[2] == "<a:hutaoCash:1118473906915917935>":
                cursor.execute(f'''UPDATE economy SET pekos = pekos + {5*amount} WHERE id = {discID}''')
                conn.commit()
                slotsembed = discord.Embed(title="Slots", description="2 Jackpots!!!", color=0xFF0000)
                slotsembed.add_field(name="pekos",value=f"+{5*amount}")
                await ctx.send(embed=slotsembed)
                await ctx.send("<:Poggie:674427373440991232>")
            elif (slotsresults[0] == slotsresults[1] and slotsresults[2] == "<a:hutaoCash:1118473906915917935>") or (slotsresults[1] == slotsresults[2] and slotsresults[0] == "<a:hutaoCash:1118473906915917935>") or (slotsresults[0] == slotsresults[2] and slotsresults[1] == "<a:hutaoCash:1118473906915917935>"):
                cursor.execute(f'''UPDATE economy SET pekos = pekos + {5*amount} WHERE id = {discID}''')
                conn.commit()
                slotsembed = discord.Embed(title="Slots", description="1 Jackpot and 2 Matches!!!", color=0xFF0000)
                slotsembed.add_field(name="pekos",value=f"+{5*amount}")
                await ctx.send(embed=slotsembed)
                await ctx.send("<:Poggie:674427373440991232>")
            elif slotsresults[0] == slotsresults[1] or slotsresults[1] == slotsresults[2] or slotsresults[0] == slotsresults[2]:
                cursor.execute(f'''UPDATE economy SET pekos = pekos + {3*amount} WHERE id = {discID}''')
                conn.commit()
                slotsembed = discord.Embed(title="Slots", description="2 Matches!!!", color=0xFF0000)
                slotsembed.add_field(name="pekos",value=f"+{3*amount}")
                await ctx.send(embed=slotsembed)
                await ctx.send("<a:umpsmug:710004835641983054>")
            elif slotsresults[0] == "<a:hutaoCash:1118473906915917935>" or slotsresults[1] == "<a:hutaoCash:1118473906915917935>" or slotsresults[2] == "<a:hutaoCash:1118473906915917935>":
                cursor.execute(f'''UPDATE economy SET pekos = pekos + {3*amount} WHERE id = {discID}''')
                conn.commit()
                slotsembed = discord.Embed(title="Slots", description="1 Jackpot!!!", color=0xFF0000)
                slotsembed.add_field(name="pekos",value=f"+{3*amount}")
                await ctx.send(embed=slotsembed)
                await ctx.send("<a:umpsmug:710004835641983054>")
            else:
                slotsembed = discord.Embed(title="Slots", description="Unlucky", color=0xFF0000)
                slotsembed.add_field(name="pekos",value=f"+0")
                await ctx.send(embed=slotsembed)
                await ctx.send("<:oddoneSmug:747346231595892766>")
            conn.close()
        else:
            await ctx.send("Missing database")

    @commands.command()
    async def bank(self, ctx):
        '''Jackpot prize pool'''
        if os.path.exists(os.path.join(sys.path[0], f"databases\\econ.db")):
            conn = sqlite3.connect(os.path.join(sys.path[0], f"databases\\econ.db"))
            cursor = conn.cursor()
            cursor.execute('''SELECT * FROM bank''')
            bank = cursor.fetchall()
            for x in range(len(bank)):
                await ctx.send(f"Game: {bank[x][0]}, Bank: {bank[x][1]}")
        else:
            await ctx.send("Missing database")

    @commands.command(name="coinflip")
    async def coinflip(self, ctx, mode: str = None, amount: int = None):
        '''Flip a coin
        You can play vs the coin with pve mode
        !coinflip | !coinflip pve [amount]'''
        discID = ctx.author.id
        coinoutcomes = ["heads", "tails"]
        headoptions = ["heads", "head", "h"]
        tailoptions = ["tails", "tail", "t"]
        weights = [.5,.5]
        if mode is None and amount is None:
            outcome = random.choices(coinoutcomes, weights)
            await ctx.send(f"Coin landed on {outcome[0]}")
        elif mode.lower() == "pve" and amount is not None:
            outcome = random.choices(coinoutcomes, weights)
            if not checkReg(discID=discID):
                await ctx.send("You might not be registered, !register to register")
                return
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
                await ctx.send(f"Heads or Tails?")
                try:
                    res = await self.bot.wait_for('message', timeout=10.0, check=lambda message: message.author == ctx.author)
                except asyncio.TimeoutError:
                    await ctx.send("no response")
                else:
                    if res.content.lower() in headoptions:
                        cursor.execute(f'''UPDATE economy SET pekos = pekos - {amount} WHERE id = {discID}''')
                        conn.commit()
                        if outcome[0] == "heads":
                            cursor.execute(f'''UPDATE economy SET pekos = pekos + {2*amount} WHERE id = {discID}''')
                            conn.commit()
                            conn.close()
                            await ctx.send(f"Coin landed on {outcome[0]} and you picked {res.content}, you won here is {2*amount} pekos")
                        else:
                            await ctx.send(f"Coin landed on {outcome[0]} and you picked {res.content}, you lost")
                            conn.close()
                    elif res.content.lower() in tailoptions:
                        cursor.execute(f'''UPDATE economy SET pekos = pekos - {amount} WHERE id = {discID}''')
                        conn.commit()
                        if outcome[0] == "tails":
                            cursor.execute(f'''UPDATE economy SET pekos = pekos + {2*amount} WHERE id = {discID}''')
                            conn.commit()
                            conn.close()
                            await ctx.send(f"Coin landed on {outcome[0]} and you picked {res.content}, you won here is {2*amount} pekos")
                        else:
                            await ctx.send(f"Coin landed on {outcome[0]} and you picked {res.content}, you lost")
                            conn.close()
                    else:
                        await ctx.send("Not a valid option")
            else:
                await ctx.send("Missing database")
        else:
            raise commands.BadArgument
        
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
