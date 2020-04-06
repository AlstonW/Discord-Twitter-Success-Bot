import discord
from discord.ext.commands import Bot
import asyncio
import json
from datetime import datetime
import requests
import os
import re
import tweepy
import emoji

"""
Bot Config (config.json)
"""
with open('config.json') as file:
    data = json.load(file)
BOT_TOKEN = data['token']
BOT_PREFIX = data['prefix']
SUCCESS_CHANNEL_NAME = data['SuccessChannelName']
TWEET_MESSAGE = data['TweetMessage']
CONSUMER_KEY = data['consumer_key']
CONSUMER_SECRET = data['consumer_secret']
ACCESS_TOKEN = data['access_token']
ACCESS_TOKEN_SECRET = data['access_token_secret']

# authentication
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET) 
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET) 
api = tweepy.API(auth)

client = Bot(command_prefix = BOT_PREFIX)

"""
Startup Code [Main]
"""
@client.event
async def on_ready():
    await client.change_presence(activity = discord.Game(name = data['BotStatus']))
    print('The Twitter Success Bot is Online.')

@client.event
async def on_message(message):
    if message.author.bot:
        pass

    elif (len(message.attachments) != 0 and SUCCESS_CHANNEL_NAME in str(message.channel)):
        try:
            channel = message.channel
            user = str(message.author).split('#')[0]

            attachment = str(message.attachments[0])
            
            # accepted pic extension types
            pic_ext = ['.jpg','.png','.jpeg']
            for ext in pic_ext:
                if attachment.find(ext) != -1:
                    # get tweet + success picture link
                    tweet = TWEET_MESSAGE + ' by user ' + user + ' 🔥'
                    img_url = re.search("url='(.*)'>", attachment).group(1)

                    # temporarily download img to post in tweet
                    filename = 'temp.jpg'
                    request = requests.get(img_url, stream=True)
                    if request.status_code == 200:
                        with open(filename, 'wb') as image:
                            for chunk in request:
                                image.write(chunk)

                    status = api.update_with_media(filename, tweet)
                    os.remove(filename)

                    embed = discord.Embed(title = 'Your success post has been tweeted.', color=0xADD8E6)

                    embed.set_footer(text = 'Twitter Success Bot')
                    embed.timestamp = datetime.utcnow()

                    await channel.send(embed = embed)

        except Exception as e:
            embed = discord.Embed(title = 'File is too big, must be less than 3072kb.', color=0xADD8E6)

            embed.set_footer(text = 'Twitter Success Bot')
            embed.timestamp = datetime.utcnow()

            await channel.send(embed = embed)

    await client.process_commands(message)

client.run(BOT_TOKEN)