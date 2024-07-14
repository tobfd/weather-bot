from dotenv import load_dotenv
import discord
import ezcord

import os

load_dotenv()
TOKEN = os.getenv("TOKEN")

bot = ezcord.Bot(intents=discord.Intents.all())
bot.add_help_command()
bot.add_status_changer([discord.CustomActivity(name="💻 Kevins Hackathon"), discord.CustomActivity(name="🌤️ Hier siehst du das Wetter")], interval=15)


bot.load_cogs()
bot.run()

