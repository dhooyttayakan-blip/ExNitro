# ExNitro - Auto Hunt Gift Link (tanpa auto-claim)
# Ganti 'TOKEN_BOT_KAMU' dengan token bot dari developer portal

import discord
import requests
import random
import string
import asyncio
from discord.ext import commands

os.getenv('BOT_TOKEN')
PREFIX = '!'

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=PREFIX, intents=intents)
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
    print('Mode: Gift hunter (tanpa auto-claim)')

@bot.command(name='gifthunt')
async def gifthunt(ctx):
    """Loop cari kode nitro, kalau nemu kirim link gift ke channel."""
    await ctx.send("🔍 **Gift hunt dimulai.** Bot akan mencari kode nitro valid dan mengirim link gift-nya.")
    count = 0
    while True:
        code = generate_code()
        count += 1
        if check_code(code):
            gift_link = f"https://discord.gift/{code}"
            await ctx.send(f"🎁 **KODE NITRO VALID DITEMUKAN!**\n{gift_link}\n*Bot berhenti mencari.*")
            break
        if count % 100 == 0:
            await ctx.send(f"🔍 Sudah mencoba {count} kode...")
        await asyncio.sleep(0.05)

@bot.command(name='help')
async def help_cmd(ctx):
    await ctx.send("**ExNitro Gift Hunter**\n`!gifthunt` - Cari nitro sampai dapat, hasilnya link gift dikirim ke channel.")

bot.run(BOT_TOKEN)
