import discord
import logging
from discord.ext import commands
import sqlite3
import time

#start logging (disable if you want, pretty useless unless you're modifying the bot)
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

#create database
conn = sqlite3.connect('messagelog.db')
c = conn.cursor()
c.execute("""CREATE TABLE IF NOT EXISTS messages (author TEXT, contents TEXT, channel TEXT, timestamp INTEGER)""")
conn.commit()

bot = commands.Bot(command_prefix='!', description="description goes here")

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

@bot.event
async def on_message(message):
    #throw everything about the message into a list to prepare for execute
    messagelist = [str(message.author), message.clean_content, message.channel.name, int(message.timestamp.timestamp())]
    c.execute("""INSERT INTO messages VALUES (?,?,?,?)""", messagelist)
    conn.commit()
    #non plus ultra
    await bot.process_commands(message)

@bot.command(description="lit-o-meter functionality")
async def isitlit(*args):
    """finds a lit-o-meter value then idk what next I haven't thought that far"""
    t = time.time() - 60
    c.execute("""c.execute('SELECT * FROM messages WHERE timestamp >= ?', t)""")
    litvalue = len(c.fetchall())
    print(litvalue)


@bot.command(description="kill the bot")
#don't forget to add the role check
async def kys(*args):
    """kills the bot on request, add check for role in the final version"""
    await bot.say("powering down")
    await bot.close()
    conn.close()

#Your token goes here
bot.run("")
