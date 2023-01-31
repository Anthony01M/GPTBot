###
# ChatGPT discord bot
# Author: @Anthony01M
# License: GPL-3.0
###

# imports
import discord
import openai
import os
import datetime
import asyncio
from discord.ext import commands
from dotenv import load_dotenv

intents = discord.Intents.default()
intents.message_content = True

client = discord.Bot(intents=intents, activity=discord.Activity(
    type=2, name="https://github.com/Berry-Studios/ChatGPTBot"), status=discord.Status.do_not_disturb)

@client.event
async def on_ready():
    print(f"Bot Logged in as: {client.user.name}#{client.user.discriminator}")

load_dotenv()

client.run(os.getenv("TOKEN"))