import discord
import os
import sys
import logging
import asyncio
from logging.handlers import TimedRotatingFileHandler
from discord.ext import commands

import admin
import music
import basic

def setuplogs():
    os.makedirs(r'..\Discordbot\logs', exist_ok=True)

    formatter = logging.Formatter('%(asctime)s %(levelname)s:%(name)s %(message)s', '%Y-%m-%d %H:%M:%S')

    filehandler = logging.handlers.TimedRotatingFileHandler("logs.txt", when='midnight')
    filehandler.setLevel(logging.INFO)
    filehandler.setFormatter(formatter)

    logging.basicConfig(
        level=logging.INFO,
        handlers=[filehandler]
    )

async def command_error(ctx, exc):
    exc_type = type(exc)
    if exc_type in [commands.BadArgument, commands.MissingRequiredArgument]:
        await ctx.send("Bad arguments")

    if ctx.message.guild is None or ctx.prefix.startswith(ctx.bot.user.mention):
        if exc_type is commands.CommandNotFound:
            await ctx.send(str(exc))
            return

async def main():
    setuplogs()

    f = open(r'..\Discordbot\token.txt', 'r')
    token = f.read()
    prefixes = commands.when_mentioned_or('!')
    description = "Shademare24 Simp Bot :^)"
    intents = discord.Intents.all()
    activity = discord.Game(name="League of Legends")

    bot = commands.Bot(command_prefix=prefixes, description=description, intents=intents, activity=activity)
    bot.on_command_error = command_error

    async with bot:
        await bot.add_cog(basic.basicplugin(bot))
        await bot.add_cog(admin.adminplugin(bot))
        await bot.add_cog(music.musicplugin(bot))
        await bot.start(token)
    #bot.run(token)

asyncio.run(main())
