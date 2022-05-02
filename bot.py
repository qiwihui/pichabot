# bot.py
import os
import random
import json
import string
import discord
import logging
from pathlib import Path
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# logging
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(
    filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter(
    '%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

bot = commands.Bot(command_prefix='!')


@bot.command(name='99', help='Responds with a random quote from Brooklyn 99')
async def nine_nine(ctx):
    brooklyn_99_quotes = [
        'I\'m the human form of the 💯 emoji.',
        'Bingpot!',
        (
            'Cool. Cool cool cool cool cool cool cool, '
            'no doubt no doubt no doubt no doubt.'
        ),
    ]

    response = random.choice(brooklyn_99_quotes)
    await ctx.send(response)


@bot.command(name='connect', help='Connect starcoin wallet address')
async def connect(ctx, wallet_address: str):
    session = ''.join(random.choice(string.ascii_letters) for _ in range(10))
    url = f"https://ov.qiwihui.com/?session={session}"
    db = {}
    if Path("db.json").exists():
        with open("db.json") as f:
            db = json.load(f)
    db[str(ctx.author.id)] = {
        "session": session,
        "wallet_address": wallet_address,
        "name": ctx.author.name,
        "verified": False,
    }
    with open('db.json', 'w') as f:
        json.dump(db, f)
    await ctx.send(f"Check {url} to verify your wallet address")


@bot.command(name='getme', help='Get your information')
async def get_me(ctx):
    db = {}
    if Path("db.json").exists():
        with open("db.json") as f:
            db = json.load(f)
    author_id = str(ctx.author.id)
    if author_id in db and db[author_id]['verified']:
        await ctx.send(f"Verified: {db[author_id]['verified']}\nWallet Address: {db[author_id]['wallet_address']}\nName: {db[author_id]['name']}")
    elif author_id in db:
        await ctx.send(f"Verified: {db[author_id]['verified']}\nName: {db[author_id]['name']}")
    else:
        await ctx.send("You are not connected yet")


@bot.command(name='create-channel', help='Creates a new text channel')
@commands.has_role('admin')
async def create_channel(ctx, channel_name: str):
    guild = ctx.guild
    existing_channel = discord.utils.get(guild.channels, name=channel_name)
    if not existing_channel:
        print(f'Creating channel: {channel_name}')
        await guild.create_text_channel(channel_name)
    else:
        print(f'Channel {channel_name} already exists')


@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CommandNotFound):
        await ctx.send('Command not found')

    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send('You do not have permission to use this command')


bot.run(TOKEN)
