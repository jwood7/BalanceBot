import discord
import os
from dotenv import load_dotenv
import requests
import json
from datetime import datetime

load_dotenv()

intents=discord.Intents.default()
intents.message_content = True
# intents.reactions = True
# intents.members = True
client = discord.Client(intents=intents)

client.options = []
client.cap1=""
client.cap2=""

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
        table += "║" + " " + team1["players"][-1]["player_name"] + " " * (longest_len1 - len(team1["players"][-1]["player_name"])) + " |"
        table += " " + str("%.3f" % round(team1["players"][-1]["player_score"],3)) + " ║"
        table += " None" + " " * (longest_len2 - len("None")) + " |"
        table += " " + "0.000" + " ║\n"
    elif(team1["team_num_players"] < team2["team_num_players"]):
        table += "║" + " None" + " " * (longest_len1 - len("None")) + " |"
        table += " " + "0.000" + " ║"
        table += " " + team2["players"][-1]["player_name"] + " " * (longest_len2 - len(team2["players"][-1]["player_name"])) + " |"
        table += " " + str("%.3f" % round(team2["players"][-1]["player_score"],3)) + " ║\n"
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

testPlayers = [
    {
        "steam_id": "STEAM_0:87492795",
        "discord": "yakobay",
        "handle": "Yakobay",
        "captain": "TRUE"
    },
    {
        "steam_id": "STEAM_1:233495",
        "discord": "Edgespresso",
        "handle": "Edge",
        "captain": "TRUE"
    },
    {
        "steam_id": "STEAM_0:474747447",
        "discord": "ogre",
        "handle": "Ogre",
        "captain": "FALSE"
    },
    {
        "steam_id": "STEAM_2:23333",
        "discord": "The Toze",
        "handle": "Toze",
        "captain": "FALSE"
    },
    {
        "steam_id": "STEAM_0:555557",
        "discord": "Mailboxhead",
        "handle": "Mailboxhead",
        "captain": "FALSE"
    },
    {
        "steam_id": "STEAM_2:666666",
        "discord": "Salty",
        "handle": "The Salty Spittoon",
        "captain": "FALSE"
    },
    {
        "steam_id": "STEAM_1:666667",
        "discord": "Nuticles",
        "handle": "Nuticles",
        "captain": "FALSE"
    },
    {
        "steam_id": "STEAM_3:22222",
        "discord": "Kura",
        "handle": "Kurevan",
        "captain": "FALSE"
    },
    {
        "steam_id": "STEAM_0:999999999",
        "discord": "Duckhead",
        "handle": "Duckhead",
        "captain": "FALSE"
    }
]

client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    client.options = testOptions
    client.cap1=""
    client.cap2=""

async def move_player(player, channel):
    print(player["discord"])
    if player["discord"] is not None:
        user = discord.utils.get(client.get_all_members(), name=player["discord"].lower())
        if user is not None:
            await user.move_to(channel)
        else:
            print(player["discord"] + " not found")
    else:
        print(player["handle"] + " has no associated Discord handle")

@client.event
async def on_message(message):
    
    channel_a = client.get_channel(737465015904239717)
    channel_b = client.get_channel(737465087710724168)
    lounge = client.get_channel(737465527441555467)
    captainsQuarter = client.get_channel(1138996335585022032)
    if message.author == client.user:
        return
    if message.content.startswith('!gf_test'): #send test data to balance api
        picker_url = os.getenv('PICKER_IP') + "/balance"
        # test data
        # member_names = ["Edge", "Mailboxhead", "Dream", "Unthink", "Duckhead", "Yakobay", "Ogre", "Cloner", "Toze"]
        # response_picker = requests.post(picker_url, json = {"players": member_names})
        response_picker = requests.post(picker_url, json = testPlayers)
        if response_picker.content and response_picker.status_code == 200:
            print(response_picker)
            print(response_picker.text)
            options = json.loads(response_picker.text)
            client.options = options
            #*BOT* will display The 5 team options in a new DISCORD channel (Captains), with some sort of voting options
            for i in range(len(options)):
                await message.channel.send("Option " + str(i+1) +  ":\n```" + make_table(options[i]["team_a"],options[i]["team_b"]) + "```")
            await message.channel.send("Choose your teams by typing !gf_pick [option number]")
            client.cap1 = "Yakobay"
            client.cap2 = "Edge"
        else:
            print(response_picker.text)
            print(response_picker.status_code)
            print("picker api failed")
    if message.content.startswith('!gf_teams'): #check score of map 
        if (len(message.content.split(' ')) < 2):
            await message.channel.send("!gf_teams [captain1] [captain2] to pick teams")
        else:
            command = message.content.split(' ')
            if lounge is None:
                await message.channel.send("Voice channel not found.")
                return
            members = lounge.members
            member_names = [member.name for member in members]
            await message.channel.send(f"Members in lounge: {', '.join(member_names)}")
            # stats_url = os.getenv('STATS_IP') + "/api/stats/pick_teams/"
            # stats_url = os.getenv('STATS_IP')+ "/api/stats/pick_teams?cap1=" + command[1] + "&cap2=" + command[2]
            # response_stats =  requests.get(stats_url)
            stats_url = "http://stats.geekfestclan.com/api/stats/pick_teams/"
            response_stats = requests.post(stats_url, json = {"cap1": command[1], "cap2": command[2],"players": member_names, "key": os.getenv('KEY')})
            # print(response_stats)
            if response_stats.content and response_stats.status_code == 200:
                teams = json.loads(response_stats.text)
                captainsAttending = 0
                for player in teams["players"]:
                    if player["handle"].lower() == command[1].lower() or player["handle"].lower() == command[2].lower() or player["discord"].lower() == command[1].lower() or player["discord"].lower() == command[2].lower():
                        player["captain"] = "TRUE"
                        captainsAttending += 1
                    else:
                        player["captain"] = "FALSE"
                if captainsAttending < 2:
                    await message.channel.send("Both captains must be in the lounge to pick teams.")
                    return
                print(teams)
                print(teams["players"])
                client.cap1 = teams['captains']["captain1"]
                client.cap2 = teams['captains']["captain2"]
                # await message.channel.send(captains["status"])
                picker_url = os.getenv('PICKER_IP') + "/balance"
                # test data
                # member_names = ["Edge", "Mailboxhead", "Dream", "Unthink", "Duckhead", "Yakobay", "Ogre", "Cloner", "Toze"]
                # response_picker = requests.post(picker_url, json = {"players": member_names})
                
                response_picker = requests.post(picker_url, json = teams["players"])
                if response_picker.content and response_picker.status_code == 200:
                    print(response_picker)
                    print(response_picker.text)
                    options = json.loads(response_picker.text)
                    client.options = options
                    #*BOT* will display The 5 team options in a new DISCORD channel (Captains), with some sort of voting options
                    for i in range(len(options)):
                        await message.channel.send("Option " + str(i+1) +  ":\n```" + make_table(options[i]["team_a"],options[i]["team_b"]) + "```")
                    await message.channel.send("Choose your teams by typing !gf_pick [option number]")
                    # Faster version, but hits the character limit. Only viable if less than 5 options.
                    # option_text = ""
                    # for i in range(len(options)):
                    #     option_text+= "Option " + str(i+1) +  ":\n```" + make_table(options[i]["team_a"],options[i]["team_b"]) + "```\n"
                    # option_text+="Choose your teams by typing !gf_pick [option number]"
                    # print(len(option_text))
                else:
                    print(response_picker.text)
                    print(response_picker.status_code)
                    print("picker api failed")
            else:
                # print(response_stats.text)
                print(response_stats.text)
                print(response_stats.status_code)
                print("stats api failed")
    elif message.content.startswith('!gf_pick'):
        if (len(message.content.split(' ')) < 2):
            await message.channel.send("!gf_pick [option number] to pick teams")
        else:
            command = message.content.split(' ')
            # print(client.options)
            selected_option = client.options[int(command[1])-1]
            print(selected_option)
            #move players to team channels
            for player in selected_option["team_a"]["players"]:
                await move_player(player, channel_a)
            for player in selected_option["team_b"]["players"]:
                await move_player(player, channel_b)
            #send selected team to selectedTeam API
            # select_url = os.getenv('PICKER_IP') + "/selectedTeam"
            # response_select = requests.post(select_url, json = selected_option) 
            # if response_select.content and response_select.status_code == 200:
            #     print(response_select.text)
            # else:
            #     print(response_select.text)
            #     print(response_select.status_code)
            #     print("select api failed")
            #add captains 
            for player in selected_option["team_a"]["players"]:
                if player["player_name"] == client.cap1:
                    # selected_option["team_a"]["captain"] = client.cap1
                    # selected_option["team_b"]["captain"] = client.cap2
                    # captains are correct
                    break
                if player["player_name"] == client.cap2:
                    # selected_option["team_a"]["captain"] = client.cap2
                    # selected_option["team_b"]["captain"] = client.cap1
                    # teams need to be swapped
                    temp = selected_option["team_a"]
                    selected_option["team_a"] = selected_option["team_b"]
                    selected_option["team_b"] = temp
                    break
            print(selected_option)
            save_url = os.getenv('STATS_IP') + "/api/stats/save_teams/"
            response_save = requests.post(save_url, json = {"team1": selected_option["team_a"], "team2": selected_option["team_b"], "cap1": client.cap1, "cap2": client.cap2, "key": os.getenv('KEY')})
            if(response_save.content and response_save.status_code == 200):
                print(response_save.text)
            else:
                print(response_save.text)
                print(response_save.status_code)
                print("save api failed")
    elif message.content.startswith('!get_attendance') | message.content.startswith('$get_attendance') | message.content.startswith('/get_attendance'):
        # send discord members in lounge, captain's quarters, and team A/ team B channels to API 
        if lounge is None or captainsQuarter is None or channel_a is None or channel_b is None:
            await message.channel.send("Voice channel not found.")
            return
        members = captainsQuarter.members + lounge.members +  channel_a.members + channel_b.members
        member_names = [member.name for member in members]
        
        url = os.getenv("STATS_API_URL") + "/teams/load-discord-geeks/"

        secret_key = os.getenv('STATS_API_KEY')
        headers = {
            "Authorization": f"Bearer {secret_key}",
            "Content-Type": "application/json"
        }

        # Make the POST request
        response = requests.post(url, json=member_names, headers=headers)

        # Print the response
        print(response.status_code)
        print(response.json())
    elif message.content.startswith('!move_teams') | message.content.startswith('$move_teams') | message.content.startswith('/move_teams'):
        # move attendees to correct channels
        today = str(datetime.today()).split()[0]
        url = os.getenv("STATS_API_URL") + "/teams/team-geek?event_date=" + today
        response =  requests.get(url)
        # print(response.json())
        channels = [channel_a, channel_b]
        for index, team in enumerate(response.json()):
            for player in team['team']: 
                if len(channels) > index:
                    await move_player(player, channels[index])
            
#new to do: 
# Move to proper / commands
# Clean up code (move into separate functions)
# On user join or leave discord channel, resend the get_attendance data

#to do: 
# Vote functionality. Embed and send tables.
# Send team data to team API. Call stats captain api
# Move/get teams from last week
# return everyone to lounge
# shorten commands
    
client.run(os.getenv('TOKEN'))