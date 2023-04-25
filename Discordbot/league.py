import discord
import sys
from discord.ext import commands
import discord.utils
import os
import re
import asyncio
import requests

opentxt = open(os.path.join(sys.path[0], "lolapitoken.txt"), "r")
apikey = opentxt.read()

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
        '''For now gets summoner level of a summoner'''
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