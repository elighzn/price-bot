# bot.py
import os
import http.client
import json

import discord
from discord.ext import tasks
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('MPB_BOT_DISCORD_TOKEN')
client = discord.Client()


@tasks.loop(seconds=60)
async def update_price():
    connection = http.client.HTTPSConnection(
        'www.bakeryswap.org')
    headers = {'Content-type': 'application/json'}
    foo = {
        "nftTypes": "107,113,117,118",
        "fileType": "",
        "offset": 0,
        "limit": 13,
        "sortName": "price",
        "sortBy": "asc",
        "onSale": 1,
        "status": 1,
        "keyword": "Matrix Plus Box"
    }
    payload = json.dumps(foo)
    connection.request('POST', '/api/v3/nfts', payload, headers)
    response = connection.getresponse().read().decode()

    data = json.loads(response)
    floor_mpb = data['data']['list'][0]
    price = "{:.2f}".format(float(floor_mpb["price"]))
    url = floor_mpb["tokenURI"]
    mpb_number = url[url.rfind('/') + 1:len(url)]
    message = f'${price} (id: {mpb_number})'
    print(message)
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=message))


@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

    for guild in client.guilds:
        print(guild.name)

    update_price.start()

client.run(TOKEN)
