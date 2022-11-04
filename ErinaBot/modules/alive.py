"""@Kaizuryu"""

from telethon import events, Button, custom
from ErinaBot.events import register
from ErinaBot import telethn as tbot
ErinaBot = "https://te.legra.ph/file/dfd7cd7877f71c10b0570.jpg"
@register(pattern=("/alive"))
async def awake(event):
  STB = event.sender.first_name
  STB = "**I m Erina** \n\n" + "**I'm Working Properly**\n\n"
  STB += "**Python Version : 3.9.7**\n\n"
  STB += "**python-Telegram-Bot : 13.7**\n\n"
  BUTTON = [[Button.url("Support", "https://t.me/ErinaSupport"), Button.url("Updates", "https://t.me/ErinaUpdate")]]
  await tbot.send_file(event.chat_id, ErinaBot, caption=STB,  buttons=BUTTON)

  # thanks to stb the gay
