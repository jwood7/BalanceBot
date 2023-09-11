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

def make_table(team1,team2):
    longest_name1 = team1["team_name"] #+7?
    longest_name2 = team2["team_name"]
    for player in team1["players"]:
        if (len(player["player_name"]) > len(longest_name1)):
            longest_name1 = player["player_name"]
    for player in team2["players"]:
        if (len(player["player_name"]) > len(longest_name2)):
            longest_name2 = player["player_name"]
    longest_len1 = len(longest_name1) 
    longest_len2 = len(longest_name2)
    #top border 
    table ="╔" + "═" * (longest_len1 + 10) + "╦" + "═" * (longest_len2 + 10) + "╗\n" #add 9 for spaces and score chars
    # table += "╠═" + "═" * (longest_len1 + 9) + "╬" + "═" * (longest_len2 + 9) + "╣\n"
    #team names
    table += "║ " + " " * ((longest_len1 + 8 - len(team1["team_name"])) // 2) + team1["team_name"] + " " * ((longest_len1 +8 - len(team1["team_name"])) // 2 + (longest_len1 + 8 - len(team1["team_name"])) % 2 + 1)
    table += "║ " + " " * ((longest_len2 + 8 - len(team2["team_name"])) // 2) + team2["team_name"] + " " * ((longest_len2 + 8 - len(team2["team_name"])) // 2 + (longest_len2 + 8 - len(team2["team_name"])) % 2 + 1) + "║\n"
    table += "╠═" + "═" * (longest_len1 + 9) + "╬" + "═" * (longest_len2 + 10) + "╣\n"
    #team scores
    table += "║ " + " " * ((longest_len1 + 3) // 2) + str("%.3f" % round(team1["team_score"],3)) + " " * ((longest_len1 + 3) // 2 + (longest_len1 - 3) % 2 + 1)
    table += "║ " + " " * ((longest_len2 + 3) // 2) + str("%.3f" % round(team2["team_score"],3)) + " " * ((longest_len2 + 3) // 2 + (longest_len2 - 3) % 2 + 1) + "║\n"
    #player stats
    table += "╠══" + "═" * longest_len1 + "╤" + "═" * 7 + "╬═" + "═" * (longest_len2 + 1) + "╤" + "═" * 7 + "╣\n"
    for i in range(min(team1["team_num_players"],team2["team_num_players"])):
        table += "║" + " " + team1["players"][i]["player_name"] + " " * (longest_len1 - len(team1["players"][i]["player_name"])) + " |"
        table += " " + str("%.3f" % round(team1["players"][i]["player_score"],3)) + " ║"
        table += " " + team2["players"][i]["player_name"] + " " * (longest_len2 - len(team2["players"][i]["player_name"])) + " |"
        table += " " + str("%.3f" % round(team2["players"][i]["player_score"],3)) + " ║\n"
    if (team1["team_num_players"] > team2["team_num_players"]):
        table += "║" + " " + team1["players"][i]["player_name"] + " " * (longest_len1 - len(team1["players"][i]["player_name"])) + " |"
        table += " " + str("%.3f" % round(team1["players"][i]["player_score"],3)) + " ║"
        table += " None" + " " * (longest_len2 - len("None")) + " |"
        table += " " + "0.000" + " ║\n"
    elif(team1["team_num_players"] < team2["team_num_players"]):
        table += "║" + " None" + " " * (longest_len1 - len("None")) + " |"
        table += " " + "0.000" + " ║"
        table += " " + team2["players"][i]["player_name"] + " " * (longest_len2 - len(team2["players"][i]["player_name"])) + " |"
        table += " " + str("%.3f" % round(team2["players"][i]["player_score"],3)) + " ║\n"
    #bottom border
    table += "╚" + "═" * (longest_len1 + 2) + "╧" + "═" * 7 + "╩" + "═" * (longest_len2 + 2) + "╧" + "═" * 7 + "╝\n"
    return table


testOptions = [
    {
        "team_name": "Alpha",
        "team_score": 5.9032627425,
        "team_num_players": 5,
        "players": [
            {
                "player_name": "Cloner",
                "player_score": 2.2507
            },
            {
                "player_name": "Duckhead",
                "player_score": 0.8698
            },
            {
                "player_name": "Toze",
                "player_score": 1.1778
            },
            {
                "player_name": "Yakobay",
                "player_score": 0.9579
            },
            {
                "player_name": "Ogre",
                "player_score": 0.6471
            }
        ]
    },
    {
        "team_name": "Bravo",
        "team_score": 5.8066908706,
        "team_num_players": 4,
        "players": [
            {
                "player_name": "Dream",
                "player_score": 1.9214
            },
            {
                "player_name": "Edge",
                "player_score": 1.2822
            },
            {
                "player_name": "Mailboxhead",
                "player_score": 1.0127
            },
            {
                "player_name": "Unthink",
                "player_score": 1.5904
            }
        ]
    }
]

client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.startswith('!gf_teams'): #check score of map 
        print(make_table(testOptions[0],testOptions[1]))
        if (len(message.content.split(' ')) < 2):
            await message.channel.send("!gf_teams [captain1] [captain2] to pick teams")
        else:
            command = message.content.split(' ')
            lounge = client.get_channel(737465527441555467)
            if lounge is None:
                await message.channel.send("Voice channel not found.")
                return
            members = lounge.members
            member_names = [member.name for member in members]
            await message.channel.send(f"Members in lounge: {', '.join(member_names)}")
            stats_url = "http://192.168.0.209:8000/api/stats/pick_teams/"
            # stats_url = "http://192.168.0.209:8000/api/stats/pick_teams?cap1=" + command[1] + "&cap2=" + command[2]
            # response_stats = await requests.get(stats_url)
            # stats_url = "http://stats.geekfestclan.com/api/stats/pick_teams/"
            response_stats = requests.post(stats_url, json = {"cap1": command[1], "cap2": command[2],"players": member_names, "key": os.getenv('KEY')})
            # print(response_stats)
            if response_stats.content and response_stats.status_code == 200:
                captains = json.loads(response_stats.text)
                print(response_stats.text)
                print(captains)
                await message.channel.send(captains["status"])
                picker_url = "http://localhost:5000/balance"
                response_picker = requests.post(picker_url, json = {"players": member_names})
                if response_picker.content and response_picker.status_code == 200:
                    options = json.loads(response_picker.text)
                    print(response_picker.text)
                    #*BOT* will display The 5 team options in a new DISCORD channel (Captains), with some sort of voting options
                    
                else:
                    print(response_picker.text)
                    print(response_picker.status_code)
                    print("failed")
            else:
                # print(response_stats.text)
                print(response_stats)
                print(response_stats.status_code)
                print("failed")
    
client.run(os.getenv('TOKEN'))