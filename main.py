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
from database import add_user, delete_user, get_api_key

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

@client.slash_command(
    name="chat",
    description="Chat with the bot in a thread."
)
async def chat(ctx):
    return await ctx.respond(content="This command is not ready yet.")

@client.slash_command(
    name="ask",
    description="Ask the bot a question."
)
async def ask(ctx, question: str):
    return await ctx.respond(content="This command is not ready yet.")

@client.slash_command(
    name="setup",
    description="setup your account."
)
@discord.commands.option(name="action", description="What action would you like to take?", choices=["add", "delete"], required=True)
@discord.commands.option(name="api_key", description="API key from https://openai.com/ which allows you to use the bot", required=False)
@discord.default_permissions(send_messages=True)
async def setup(ctx, action: str, api_key: str = None):
    # command cannot be used in guilds
    if ctx.guild_id is not None:
        return await ctx.respond(content="This command can only be used in DMs.")
    if action == "add":
        if api_key is None:
            return await ctx.respond(content="You must provide an API key.")
        if add_user(ctx.author.id, api_key):
            return await ctx.respond(content="You must provide a valid API key.")
        elif add_user(ctx.author.id, api_key) == "updated":
            add_user(ctx.author.id, api_key)
            await ctx.respond(content="You were already registered to the bot, your API key has been updated.")
        else:
            add_user(ctx.author.id, api_key)
            await ctx.respond(content="You have been registered to the bot.")
    if action == "delete":
        if delete_user(ctx.author.id):
            return await ctx.respond(content="You do not have an account.")
        else :
            return await ctx.respond(content="Your account has been deleted.")
    

client.run(os.getenv("TOKEN"))