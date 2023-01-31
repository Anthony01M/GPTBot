###
# ChatGPT discord bot
# Author: @Anthony01M
# License: GPL-3.0
###

import discord
import openai
import os
import datetime
import asyncio
from discord.ext import commands
from dotenv import load_dotenv

intents = discord.Intents.default()
intents.message_content = True

load_dotenv()

client = discord.Bot(intents=intents, activity=discord.Activity(
    type=2, name="https://github.com/Berry-Studios/ChatGPTBot"), status=discord.Status.do_not_disturb)

startTime = datetime.datetime.utcnow()

@client.event
async def on_ready():
    print(f"Bot Logged in as: {client.user.name}#{client.user.discriminator}")

@client.slash_command(
    name="ping",
    description="Bot latency"
)
async def ping(ctx):
    await ctx.respond(content=f"Pong! {round(client.latency * 1000)}ms")

@client.slash_command(
    name="uptime",
    description="Bot uptime."
)
async def uptime(ctx):
    now = datetime.datetime.utcnow()
    delta = now - startTime
    uptime = ""
    if delta.days // 365 > 0:
        if delta.days // 365 == 1:
            uptime = uptime[:-2] + " year, "
        else:
            uptime += f"{delta.days // 365} years, "
    # months and week should show too
    if delta.days % 365 // 30 > 0:
        if delta.days % 365 // 30 == 1:
            uptime = uptime[:-2] + " month, "
        else:
            uptime += f"{delta.days % 365 // 30} months, "
    if delta.days % 365 % 30 // 7 > 0:
        if delta.days % 365 % 30 // 7 == 1:
            uptime = uptime[:-2] + " week, "
        else:
            uptime += f"{delta.days % 365 % 30 // 7} weeks, "
    if delta.days % 365 % 30 % 7 > 0:
        if delta.days % 365 % 30 % 7 == 1:
            uptime = uptime[:-2] + " day, "
        else:
            uptime += f"{delta.days % 365 % 30 % 7} days, "
    if delta.seconds // 3600 > 0:
        if delta.seconds // 3600 == 1:
            uptime = uptime[:-2] + " hour, "
        else:
            uptime += f"{delta.seconds // 3600} hours, "
    if delta.seconds % 3600 // 60 > 0:
        if delta.seconds % 3600 // 60 == 1:
            uptime = uptime[:-2] + " minute, "
        else:
            uptime += f"{delta.seconds % 3600 // 60} minutes, "
    if delta.seconds % 3600 % 60 > 0:
        if delta.seconds % 3600 % 60 == 1:
            uptime = uptime[:-2] + " second, "
        else:
            uptime += f"{delta.seconds % 3600 % 60} seconds, "

    if uptime.endswith(", "):
        uptime = uptime[:-2]

    await ctx.respond(content=f"Uptime: {uptime}")

client.run(os.getenv("TOKEN"))