import discord
from discord.ext import commands, tasks
import requests
import re, os, sys, random, sqlite3

vtubers = [["Omaru Polka", "https://www.youtube.com/@OmaruPolka"], ["Ceres Fauna", "https://www.youtube.com/@CeresFauna"], ["Nanashi Mumei", "https://www.youtube.com/@NanashiMumei"], ["Usada Pekora", "https://www.youtube.com/@UsadaPekora"], ["Sakamata Chloe", "https://www.youtube.com/@SakamataChloe"],
           ["Laplus Darknesss", "https://www.youtube.com/@LaplusDarknesss"], ["Hakui Koyori", "https://www.youtube.com/@HakuiKoyori"], ["Yukihana Lamy", "https://www.youtube.com/@YukihanaLamy"], ["Momosuzu Nene", "https://www.youtube.com/@MomosuzuNene"], ["Shishiro Botan", "https://www.youtube.com/@ShishiroBotan"],
           ["Kazama Iroha", "https://www.youtube.com/@KazamaIroha"], ["Gawr Gura", "https://www.youtube.com/@GawrGura"], ["Watson Amelia", "https://www.youtube.com/@WatsonAmelia"], ["Minato Aqua", "https://www.youtube.com/@MinatoAqua"], ["Shirakami Fubuki", "https://www.youtube.com/@ShirakamiFubuki"],
           ["AZKi", "https://www.youtube.com/@AZKi"]]

class basicplugin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.is_owner()
    @commands.command(name='basictest')
    async def test(self, ctx):
        await ctx.send("hello! from basic.py")

    @commands.command()
    async def add(self, ctx, *args):
        '''Addition'''
        totalsum = 0
        #print(type(totalsum))
        for num in args:
            #print(type(num))
            convertedStrToFloat = float(num)
            totalsum += convertedStrToFloat
        #print(type(totalsum))
        await ctx.send(totalsum)

    @commands.command()
    async def sub(self, ctx, *args):
        '''Subtraction'''
        totaldiff = 0
        for num in args:
            convertedStrToFloat = float(num)
            totaldiff -= convertedStrToFloat
        await ctx.send(totaldiff)

    @commands.command()
    async def mul(self, ctx, *args):
        '''Multiplication'''
        totalproduct = 1
        for num in args:
            convertedStrToFloat = float(num)
            totalproduct *= convertedStrToFloat
        await ctx.send(totalproduct)

    @commands.command()
    async def div(self, ctx, top:float, bot:float):
        '''Division'''
        solution = top / bot
        await ctx.send(solution)

    @commands.command()
    async def exp(self, ctx, base:float, exponent:float):
        '''Exponents'''
        solution = base ** exponent
        await ctx.send(solution)

    @commands.command()
    async def watch(self, ctx, vtuberindex: int = None):
        '''Gives a random vtuber to watch'''
        if vtuberindex is None:
            vtuber, vtuberurl = random.choice(vtubers)
        else:
            vtuber, vtuberurl = vtubers[vtuberindex]
        await ctx.send(f"vtuber: {vtuber} \nvtuber url: {vtuberurl}")
        await self.bot.change_presence(activity=discord.Activity(name=vtuber, type=discord.ActivityType.watching, url=vtuberurl), status="dnd")

    @commands.command()
    async def watchindex(self, ctx):
        '''Returns index of watch'''
        vtuberindex = 0
        response = ""
        while len(vtubers) > vtuberindex:
            response += str(vtuberindex) + ": " + str(vtubers[vtuberindex][0]) + "\n"
            vtuberindex += 1
        await ctx.send(response)

    @commands.command(name="clearstatus")
    async def clearstat(self, ctx):
        '''Clears bot status'''
        await self.bot.change_presence(activity=None, status=None)

    @commands.command(name="shademare12")
    async def shademare12(self, ctx):
        '''I'm Back'''
        await ctx.send("https://tenor.com/view/imback-imbackbitch-springam-gif-21929800")

    @commands.command(name="pekofy")
    async def pekofy(self, ctx):
        '''Peko!'''
        if ctx.message.reference is not None:
            message = await ctx.channel.fetch_message(ctx.message.reference.message_id)
            recentmsg = message.content
        else:
            message = [message async for message in ctx.channel.history(limit=2)]
            recentmsg = message[1].content
        output = ''
        punctuation = re.compile(r"[.?!]")
        for x in range(len(recentmsg)):
            if punctuation.match(recentmsg[x]):
                temp = " peko" + recentmsg[x]
                output += temp
            elif x == len(recentmsg)-1:
                temp = recentmsg[x] + " peko"
                output += temp
            else:
                output += recentmsg[x]
        await ctx.send(output)

    #@commands.command(name="loopbug")
    #tests if bot can call its own commands. results: it will not loop
    #async def testloop(self,ctx):
    #    await ctx.send("!loopbug")

    @commands.command(name="echo")
    async def echo(self, ctx, *args):
        '''Echos input'''
        output = ''
        for message in args:
            output += message + " "
        await ctx.send(output)

    @commands.cooldown(1, 5*60, commands.BucketType.user)
    @commands.command(name="goodbot")
    async def gudbot(self, ctx):
        '''Compliment the bot :^)'''
        if os.path.exists(os.path.join(sys.path[0], f"databases\\review.db")):
            conn = sqlite3.connect(os.path.join(sys.path[0], f"databases\\review.db"))
            cursor = conn.cursor()
            updatequery = '''UPDATE botreview SET score = score + 1 WHERE review = "good"'''
            cursor.execute(updatequery)
            conn.commit()
            conn.close()
            await ctx.send("Arigato peko! {}".format(ctx.message.author.mention))
            await ctx.send("https://tenor.com/view/pekora-usada-pekora-ogey-rrat-rrat-hololive-gif-24283304")
        else:
            await ctx.send("Missing database")

    @commands.cooldown(1, 5*60, commands.BucketType.user)
    @commands.command(name="badbot")
    async def badbot(self, ctx):
        '''Insult the bot :^('''
        if os.path.exists(os.path.join(sys.path[0], f"databases\\review.db")):
            conn = sqlite3.connect(os.path.join(sys.path[0], f"databases\\review.db"))
            cursor = conn.cursor()
            updatequery = '''UPDATE botreview SET score = score + 1 WHERE review = "bad"'''
            cursor.execute(updatequery)
            conn.commit()
            conn.close()
            await ctx.send("Faq you peko! {}".format(ctx.message.author.mention))
            await ctx.send("https://tenor.com/view/hololive-vtuber-usada-pekora-crazy-usagi-laser-gif-16904860")
        else:
            await ctx.send("Missing database")

    @commands.command(name="botreview")
    async def getreviews(self, ctx):
        '''Get the bots review scores'''
        output = ''
        if os.path.exists(os.path.join(sys.path[0], f"databases\\review.db")):
            conn = sqlite3.connect(os.path.join(sys.path[0], f"databases\\review.db"))
            cursor = conn.cursor()
            cursor.execute('''SELECT * FROM botreview''')
            results = cursor.fetchall()
            conn.close()
            embed = discord.Embed(title="Bot Statistics", description="How good or how bad <:suske:1108942794900373544> the bot is doing", color=0xFF0000)
            embed.add_field(name=results[0][0], value=results[0][1])
            embed.add_field(name=results[1][0], value=results[1][1])
            await ctx.send(embed=embed)
        else:
            await ctx.send("Missing database")

    @commands.command(name="weather", aliases=["w"])
    async def weatherapi(self, ctx, lat, long):
        '''Get weather using lat and long (no more than 4 decimal places and US only)'''
        weatherurl = "https://api.weather.gov/points/" + lat + ',' + long
        #await ctx.send(weatherurl) #check url is created correctly (works)
        reponse = requests.get(weatherurl)
        reponseJSON = reponse.json()
        forecast_url = reponseJSON['properties']['forecast']
        relativelocation = reponseJSON['properties']['relativeLocation']['properties']
        city = relativelocation['city']
        state = relativelocation['state']
        #await ctx.send(forecast_url)
        forecast_res = requests.get(forecast_url)
        forecastJSON = forecast_res.json()
        forecast_data = []
        row, col = 10,2
        for i in range(row):
            column = []
            for j in range(col):
                if j == 0:
                    column.append(forecastJSON['properties']['periods'][i]['name'])
                else:
                    column.append(forecastJSON['properties']['periods'][i]['detailedForecast'])
            forecast_data.append(column)
        await ctx.send(city + ", " + state)
        await ctx.send(str(forecast_data))

    @commands.command()
    async def ping(self, ctx):
        '''Gets Bot latency'''
        ping = f"{str(round(self.bot.latency * 1000))} ms"
        await ctx.send(ping)

    @commands.command(name='imposter')
    async def sus(self, ctx, member: discord.Member, *messages):
        '''Sussy ඞ'''
        output = ''
        for message in messages:
            output += message + " "
        webhook = await ctx.channel.create_webhook(name=member.display_name)
        await webhook.send(str(output), username=member.display_name, avatar_url=member.display_avatar.url)

        webhooks = await ctx.channel.webhooks()
        for webhook in webhooks:
            await webhook.delete()

    @commands.Cog.listener()
    async def on_ready(self):
        self.change_stat.start()

    @tasks.loop(seconds=60*60)
    async def change_stat(self):
        vtuber, vtuberurl = random.choice(vtubers)
        await self.bot.change_presence(activity=discord.Activity(name=vtuber, type=discord.ActivityType.watching, url=vtuberurl), status="dnd")
