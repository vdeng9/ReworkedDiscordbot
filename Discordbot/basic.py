import discord
from discord.ext import commands
import random
import re, os, sys, requests

vtubers = [["Omaru Polka", "https://www.youtube.com/@OmaruPolka"], ["Ceres Fauna", "https://www.youtube.com/@CeresFauna"], ["Nanashi Mumei", "https://www.youtube.com/@NanashiMumei"], ["Usada Pekora", "https://www.youtube.com/@UsadaPekora"], ["Sakamata Chloe", "https://www.youtube.com/@SakamataChloe"],
           ["Laplus Darknesss", "https://www.youtube.com/@LaplusDarknesss"], ["Hakui Koyori", "https://www.youtube.com/@HakuiKoyori"], ["Yukihana Lamy", "https://www.youtube.com/@YukihanaLamy"], ["Momosuzu Nene", "https://www.youtube.com/@MomosuzuNene"], ["Shishiro Botan", "https://www.youtube.com/@ShishiroBotan"],
           ["Kazama Iroha", "https://www.youtube.com/@KazamaIroha"], ["Gawr Gura", "https://www.youtube.com/@GawrGura"], ["Watson Amelia", "https://www.youtube.com/@WatsonAmelia"], ["Minato Aqua", "https://www.youtube.com/@MinatoAqua"], ["Shirakami Fubuki", "https://www.youtube.com/@ShirakamiFubuki"]]

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
    async def watch(self, ctx):
        '''Gives a random vtuber to watch'''
        vtuber, vtuberurl = random.choice(vtubers)
        await ctx.send("vtuber: " + vtuber)
        await ctx.send("vtuber url: " + vtuberurl)
        await self.bot.change_presence(activity=discord.Activity(name=vtuber, type=discord.ActivityType.watching, url=vtuberurl), status="dnd")

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

    @commands.command(name="goodbot")
    async def gudbot(self, ctx):
        '''Compliment the bot :^)'''
        await ctx.send("Arigato peko! {}".format(ctx.message.author.mention))
        await ctx.send("https://tenor.com/view/pekora-usada-pekora-ogey-rrat-rrat-hololive-gif-24283304")

    @commands.command(name="badbot")
    async def badbot(self, ctx):
        '''Insult the bot :^('''
        await ctx.send("Faq you peko! {}".format(ctx.message.author.mention))
        await ctx.send("https://tenor.com/view/hololive-vtuber-usada-pekora-crazy-usagi-laser-gif-16904860")

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