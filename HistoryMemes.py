import requests
import discord
import datetime
import praw
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
GUILD = os.getenv("DISCORD_GUILD")
id = os.getenv("CLIENT_ID")
secret = os.getenv("CLIENT_SECRET")
agent = os.getenv("USER_AGENT")
channelid = os.getenv("CHANNEL_ID")

client = discord.Client()
reddit = praw.Reddit(client_id=id, client_secret=secret, user_agent=agent)

# Code you can run to test if your program can connect to Discord:
#@client.event
#async def on_ready():
#    for guild in client.guilds:
#        if(guild.name == GUILD):
#            break
#            
#    print(
#        f'{client.user} has connected to: '
#        f'{guild.name}(id: {guild.id})\n'
#    )

@client.event
async def on_ready():
    #print(f"Getting Channel\n")
    channel = client.get_channel(channelid)
    #print(f"Got Channel\n")
    find_meme()
    #print(f"Meme Located\n")
    await channel.send(file=discord.File('meme.jpg'))
    #print(f"Sent meme to chat")
    
def upload_image(imgurl):
    with open('meme.jpg', 'wb') as handle:
        response = requests.get(imgurl, stream=True)

        if not response.ok:
            print(response)

        for block in response.iter_content(1024):
            if not block:
                break

            handle.write(block)

def find_meme():
    todaysdate = str(datetime.datetime.now())[0:10]
    imgurl = ""

    for submission in reddit.subreddit('HistoryMemes').hot():
        timecreated = str(datetime.datetime.fromtimestamp(submission.created))[0:10]
        if(".jpg" in str(submission.url) and (timecreated == todaysdate)):
            imgurl = submission.url
            break

    upload_image(imgurl)
    
client.run(TOKEN)
