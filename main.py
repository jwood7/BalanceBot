import discord
import os
from dotenv import load_dotenv
import requests
import json

load_dotenv()

intents=discord.Intents.default()
intents.message_content = True
# intents.reactions = True
# intents.members = True
client = discord.Client(intents=intents)

client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.startswith('!gf_teams'): #check score of map 
        if (len(message.content.split(' ')) < 2):
            await message.channel.send("!gf_teams [captain1] [captain2] to pick teams")
        else:
            command = message.content.split(' ')
            # url = "http://192.168.0.209:8000/api/stats/pick_teams"
            url = "http://192.168.0.209:8000/api/stats/pick_teams?cap1=" + command[1] + "&cap2=" + command[2]
            # url = "http://stats.geekfestclan.com/api/stats/pick_teams"
            response = await requests.get(url)
            # response = requests.post(url, json = {"cap1": command[1], "cap2": command[2], "key": os.getenv('KEY')})
            captains = json.loads(response.text)
            #Something is wrong with the format of the json response (it's full of "/"s), so I need to parse it twice. Fix on API side. 
            captains = json.loads(captains)
            if response.content and response.status_code == 200:
                print(response.text)
                print(captains)
                print(type(captains))
                print(captains["status"])
                await message.channel.send(captains["status"])
                lounge = client.get_channel(737465527441555467)
                if lounge is None:
                    await message.channel.send("Voice channel not found.")
                    return
                members = lounge.members
                member_names = [member.name for member in members]
                await message.channel.send(f"Members in lounge: {', '.join(member_names)}")
                response2 = await requests.post(url, json = {"players": member_names, "key": os.getenv('KEY')})
                if response2.content and response2.status_code == 200:
                    print(response2.text)
                    print("success")
                else:
                    print(response2.text)
                    print(response2.status_code)
            else:
                # print(response.text)
                print(response)
                print(response.status_code)
                print("failed")
    
client.run(os.getenv('TOKEN'))