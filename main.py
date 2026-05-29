import os
import discord
import logging
from discord.ext import commands
from dotenv import load_dotenv
from discord import app_commands

load_dotenv()
token=os.getenv("token")
guild_id=os.getenv("guild_id")
target_channel=os.getenv("target_channel")

intents=discord.Intents.default() # Giving default permissions to bot which includes guild, members & messages(metadata) permissions.
intents.message_content=True # Allowing bot to read messages from the server.

bot=commands.Bot(command_prefix="!",intents=intents) # config bot perfix & permissions.

# Configure Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('bot_logger')



@bot.event
async def setup_hook(): # Alert discord about new commands
    try:
        for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
                await bot.load_extension(f'cogs.{filename[:-3]}')
            print(f"Cog loaded: {filename}")
    except Exception as e:
        print(f"Failed to load cog my_cog: {e}")

@bot.event
async def on_ready():
    print(f'Logged as {bot.user}')

    # sync
    guild = discord.Object(id=int(guild_id))
    bot.tree.copy_global_to(guild=guild)
    await bot.tree.sync(guild=guild)
    print(f"Synced commands to guild: {guild_id}")

bot.run(token)