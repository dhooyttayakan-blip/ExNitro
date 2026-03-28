import os
import discord
import requests
import random
import string
import asyncio
from discord.ext import commands

BOT_TOKEN = os.getenv('BOT_TOKEN')
if not BOT_TOKEN:
    print("BOT_TOKEN not set")
    exit(1)

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)
bot.remove_command('help')

def generate_code():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=16))

def check_code(code):
    url = f"https://discord.com/api/v9/entitlements/gift-codes/{code}?with_application=false&with_subscription_plan=true"
    try:
        r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=5)
        return r.status_code == 200
    except:
        return False

@bot.event
async def on_ready():
    print(f'ExNitro siap sebagai {bot.user}')

@bot.command(name='gifthunt')
async def gifthunt(ctx):
    await ctx.send("🔍 Mencari nitro...")
    count = 0
    while True:
        code = generate_code()
        count += 1
        if check_code(code):
            await ctx.send(f"🎁 **KODE VALID!** https://discord.gift/{code}\nBerhenti mencari.")
            break
        if count % 100 == 0:
            await ctx.send(f"🔍 {count} kode dicoba...")
        await asyncio.sleep(0.05)

@bot.command(name='help')
async def help_cmd(ctx):
    await ctx.send("**ExNitro**\n`!gifthunt` - cari nitro sampai dapat link gift.")

bot.run(BOT_TOKEN)
