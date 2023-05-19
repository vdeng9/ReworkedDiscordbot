import discord
import sys
from discord.ext import commands
import discord.utils
import os
import re
import asyncio
import requests

opentxt = open(os.path.join(sys.path[0], "textfiles\\lolapitoken.txt"), "r")
apikey = opentxt.read()
ddVersionControl = "https://ddragon.leagueoflegends.com/api/versions.json"
ddvcJSON = requests.get(ddVersionControl).json()
currentVersion = ddvcJSON[0]
ddurl = f"http://ddragon.leagueoflegends.com/cdn/{currentVersion}/data/en_US/champion.json"
ddResJSON = requests.get(ddurl).json()

class leagueplugin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.is_owner()
    @commands.command(name='leaguetest')
    async def hello(self, ctx):
        await ctx.send("hello! from league.py")
        await self.bot.change_presence(activity=discord.Game(name="League Of Legends"))

    @commands.is_owner()
    @commands.command(name='lolapikey')
    async def leagueapikey(self, ctx):
        '''Gets league api key (only sends to personal bot testing channel)'''
        testing_channel = self.bot.get_channel(1088649684358266892)
        await testing_channel.send(apikey)
        await ctx.send("key was sent!")
        await self.bot.change_presence(activity=discord.Game(name="League Of Legends"))

    @commands.command(name='summoner')
    async def getsummoner(self, ctx, summoner):
        '''Gets summoner level of a summoner'''
        baselink = 'https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/'
        apilink = '?api_key=' + apikey
        fullurl = baselink + summoner + apilink
        #await ctx.send(fulllink) check that link was created correctly (it was)
        response = requests.get(fullurl)
        responseJSON = response.json()
        if response.status_code == 404:
            await ctx.send(str(responseJSON['status']['message']))
        else:
            await ctx.send(f"summoner level of {summoner} is " + str(responseJSON['summonerLevel']))

        await self.bot.change_presence(activity=discord.Game(name="League Of Legends"))

    @commands.command(name="mastery")
    async def masterypts(self, ctx, summoner):
        '''Gets top 5 champions based on mastery pts'''
        sumlink = 'https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/'
        apilink = '?api_key=' + apikey
        sumfullurl = sumlink + summoner + apilink
        response = requests.get(sumfullurl)
        sumresponseJSON = response.json()
        summonerid = sumresponseJSON['id']
        #await ctx.send(summonerid)
        masterylink = "https://na1.api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-summoner/"
        masteryfulllink = masterylink + summonerid + apilink
        #await ctx.send(masteryfulllink)
        masteryres = requests.get(masteryfulllink)
        masteryresJSON = masteryres.json()
        #https://riot-api-libraries.readthedocs.io/en/latest/ddragon.html championid to champion name conversion
        output = {}
        x = 0
        ddVersionControl = "https://ddragon.leagueoflegends.com/api/versions.json"
        ddVCRes = requests.get(ddVersionControl)
        ddVCResJSON = ddVCRes.json()
        currentVersion = ddVCResJSON[0]
        #await ctx.send(currentVersion)
        ddurl = f"http://ddragon.leagueoflegends.com/cdn/{currentVersion}/data/en_US/champion.json"
        #await ctx.send(ddurl)
        ddResJSON = requests.get(ddurl).json()
        while x < 5:
            for champion in ddResJSON['data']:
                #await ctx.send(champion)
                if ddResJSON['data'][champion]['key'] == str(masteryresJSON[x]['championId']):
                    output[ddResJSON['data'][champion]['id'] + ", " + ddResJSON['data'][champion]['title']] = masteryresJSON[x]['championPoints']
                    x += 1
        await ctx.send(output)
        await self.bot.change_presence(activity=discord.Game(name="League Of Legends"))

    @commands.command(name="freechamps")
    async def freechampions(self, ctx):
        '''Gets the free to play champion rotation'''
        champurl = "https://na1.api.riotgames.com/lol/platform/v3/champion-rotations"
        apilink = '?api_key=' + apikey
        fullurl = champurl + apilink
        champJSON = requests.get(fullurl).json()
        output = ''
        for freechamps in champJSON['freeChampionIds']:
            for champions in ddResJSON['data']:
                if ddResJSON['data'][champions]['key'] == str(freechamps):
                    output += ddResJSON['data'][champions]['id'] + ", " + ddResJSON['data'][champions]['title'] + "\n"
        await ctx.send(output)
        await self.bot.change_presence(activity=discord.Game(name="League Of Legends"))

    @commands.command(name="champstats")
    async def championstats(self, ctx, champname: str):
        '''Gets Champion Stats (some champs don't work idk y...)'''
        output = ""
        offrole = "None" # default if singular role
        for champ in ddResJSON['data']:
            if champname.lower() == str(champ).lower():
                #print(champname + "|" + champ) check name comparison is correct
                name = ddResJSON['data'][champ]['name']
                title = ddResJSON['data'][champ]['title']
                blurb = ddResJSON['data'][champ]['blurb']
                x = 0 # counts how many roles a champ has
                for role in ddResJSON['data'][champ]['tags']:
                    #print(str(x) + "|" + str(role)) check rolenum to role 0|mage, 1|tank, etc...
                    if x == 0: 
                        mainrole = role
                    if x == 1:
                        offrole = role
                    x += 1
                resourcetype = ddResJSON['data'][champ]['partype']
                for stats in ddResJSON['data'][champ]['stats']:
                    output += str(stats) + ": " + str(ddResJSON['data'][champ]['stats'][stats]) + "\n"
                await ctx.send("Name: " + name + "\nTitle: " + title + "\nLore: " + blurb + "\nMainrole: " + mainrole + "\nOffrole: " + offrole + "\nResourcetype: " + resourcetype + "\nStats: \n" + output)
                await self.bot.change_presence(activity=discord.Game(name="League Of Legends"))