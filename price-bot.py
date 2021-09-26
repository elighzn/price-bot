# bot.py
import os

import discord
from discord.ext import tasks
from dotenv import load_dotenv
from pycoingecko import CoinGeckoAPI

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
coin_id = os.getenv('COIN_ID')
currency = os.getenv('CURRENCY')
client = discord.Client()
cg = CoinGeckoAPI()


@tasks.loop(seconds=60)
async def update_price():
    result = cg.get_price(
        ids=coin_id, vs_currencies=currency, include_24hr_change=True)
    # print(result)
    price = "{:.5f}".format(result[coin_id][currency])
    change24 = "{:.2f}".format(result[coin_id]['usd_24h_change'])
    message = f'${price}({change24}%)'
    print(message)
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=message))
    # await client.user.edit(name=f'${price}')


@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

    for guild in client.guilds:
        print(guild.name)

    update_price.start()

client.run(TOKEN)
