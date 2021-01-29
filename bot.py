# Work with Python 3.6
import discord
import random
from operator import itemgetter
from os import environ

worldx = 9
worldy = 9

#TOKEN = environ['TOKEN']
file = open("TOKEN.txt", "r")
if file.mode == 'r':
    TOKEN = file.read()

client = discord.Client()

def getArrayFile(fileName):
    arrayFile = open(fileName, "r")
    array = []
    for line in arrayFile:
        array.append(line.strip().split(','))
    arrayFile.close()
    return array

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    channel = message.channel
    messages = await channel.history(limit=10).flatten()
    
#game-----------------------------------------------------------------------------------------------------------
    if message.content == "!map":
        world = getArrayFile("map.txt")
        names = getArrayFile("names.txt")
        symbols = getArrayFile("symbols.txt")
        units = getArrayFile("units.txt")
        owner = getArrayFile("owner.txt")
        worldMessage = ":black_large_square: "
        for i in range(len(world[0])):
            worldMessage += symbols[0][i] + " "
        worldMessage += "\n"
        for i in range(len(world)):
            worldMessage += symbols[1][i] + " "
            for j in range(len(world[0])):
                if world[i][j] == '0':
                    if int(units[i][j]) == 0:
                        worldMessage += ":white_large_square:"
                    else:
                        worldMessage += ":blue_square:"
                if world[i][j] == '1':
                    if int(units[i][j]) == 0:
                        worldMessage += ":house_abandoned:"
                    else:
                        worldMessage += ":house:"
                if world[i][j] == '2':
                    if int(units[i][j]) == 0:
                        worldMessage += ":city_dusk:"
                    else:
                        worldMessage += ":cityscape:"
                worldMessage += " "
            worldMessage += "\n"
        await channel.send(worldMessage)

    if message.content == "!gamehelp":
        helpFile = open("help.txt", "r")
        helpMessage = ""
        for line in helpFile:
            helpMessage += line
        await channel.send(helpMessage)
    
    if "!info" in message.content:
        world = getArrayFile("map.txt")
        names = getArrayFile("names.txt")
        symbols = getArrayFile("symbols.txt")
        units = getArrayFile("units.txt")
        owner = getArrayFile("owner.txt")
        args = message.content.strip().split(' ')
        error = False
        infoMessage = ""
        if len(args) != 2:
            error = True
        if len(args[1]) != 2:
            error = True
        locX = ord(args[1][0]) - 65
        locY = ord(args[1][1]) - 49
        if locX < 0 or locX > worldx-1 or locY < 0 or locY > worldy-1:
            error = True
        if error:
            await channel.send("error, invalid command\n!info [location]\ni.e. !info B3\ntry !help for more info")
        else:
            if world[locY][locX] == '0':
                if units[locY][locX] == '0':
                    infoMessage += ":white_large_square: "+args[1]+": empty area"
                else:
                    infoMessage += args[1]+": "+owner[locY][locX]+"'s square with "+units[locY][locX]+" units"
            elif world[locY][locX] == '1':
                infoMessage += "**"+names[locY][locX]+"**\n"
                if units[locY][locX] == '0':
                    infoMessage += ":house_abandoned: "+args[1]+": empty city"
                else:
                    infoMessage += ":house: " + args[1]+": "+owner[locY][locX]+"'s city with "+units[locY][locX]+" units"
            elif world[locY][locX] == '2':
                infoMessage += "**"+names[locY][locX]+"**\n"
                if units[locY][locX] == '0':
                    infoMessage += ":city_dusk: "+args[1]+": empty capital"
                else:
                    infoMessage += ":cityscape: " + args[1]+": "+owner[locY][locX]+"'s capital with "+units[locY][locX]+" units"
        
        await channel.send(infoMessage)

#old------------------------------------------------------------------------------------------------------------
    if "heck" in message.content:
        await channel.send("hey! no hecks in here")

    if "frick" in message.content:
        await channel.send("hey! no fricks in here")

    if message.content == "a":
        await message.delete()
        await messages[1].add_reaction('<:UpVote:507327220730167306>')

    if message.content == "z":
        await message.delete()
        await messages[1].add_reaction('<:DownVote:507327220495417395>')

    if "elel" in message.content or "ELE" in message.content:
        responses = ['OULOULOULOULOULOULOUL!!!',
                     'NREEEEEEEEEEEEEEEE!!!!!']
        await channel.send(f'{random.choice(responses)}')
        #await messages[0].add_reaction('<:UpVote:507327220730167306>')

    if "NREE" in message.content:
        responses = ['OULOULOULOULOULOULOUL!!!',
                     'ELELELELELELELELELE!!!!!']
        await channel.send(f'{random.choice(responses)}')
        #await messages[0].add_reaction('<:UpVote:507327220730167306>')

    if "OULO" in message.content:
        responses = ['ELELELELELELELELELE!!!',
                     'NREEEEEEEEEEEEEEEE!!!!!']
        await channel.send(f'{random.choice(responses)}')
        #await messages[0].add_reaction('<:UpVote:507327220730167306>')

    if message.content == "karma count":
        #karma invented 10-13-2018
        messageN = 50000
        print('getting messages...')
        messages = await channel.history(limit=messageN).flatten()
        print('got messages...')
        karma = []
        for x in range(len(messages)):
            if (not messages[x].reactions) or (messages[x].author.bot):
                continue
            else:
                for y in range(len(messages[x].reactions)):
                    #print(str(messages[x].reactions[y]))
                    if str(messages[x].reactions[y]) == '<:UpVote:507327220730167306>':
                        found = False
                        for z in range(len(karma)):
                            if (karma[z][0] == messages[x].author.display_name):
                                karma[z][1] += messages[x].reactions[y].count
                                found = True
                                break
                        if (not found):
                            karma.append([messages[x].author.display_name,messages[x].reactions[y].count,0,0])
                    if str(messages[x].reactions[y]) == '<:DownVote:507327220495417395>':
                        found = False
                        for z in range(len(karma)):
                            if (karma[z][0] == messages[x].author.display_name):
                                karma[z][2] += messages[x].reactions[y].count
                                found = True
                                break
                        if (not found):
                            karma.append([messages[x].author.display_name,0,messages[x].reactions[y].count,0])
        for x in range(len(karma)):
            karma[x][3] = karma[x][1] - karma[x][2]
        karma = sorted(karma,key=itemgetter(3), reverse=True)
        karmastr = "Total karma count:\n"
        for x in range(len(karma)):
            if(x == 0):
                karmastr += (f"🥇 ")
            elif(x == 1):
                karmastr += (f"🥈 ")
            elif(x == 2):
                karmastr += (f"🥉 ")
            karmastr += (f"{karma[x][0]} has {karma[x][1]} upvotes and {karma[x][2]} downvotes for a total karma of: {karma[x][3]} \n")
            if(karma[x][2] > 0):
                karmastr += (f"    (with a karma ratio of {karma[x][1]/karma[x][2]})\n")
            else:
                karmastr += ("    (with a perfectly clean record)\n")
        await channel.send(karmastr)
        print(f"{karma}")
        print('-----------')
        await message.delete()

    #print(message.content)
    if message.content.startswith("poll:"):
       if "1" in message.content: await messages[0].add_reaction('1⃣')
       if "2" in message.content: await messages[0].add_reaction('2⃣')
       if "3" in message.content: await messages[0].add_reaction('3⃣')
       if "4" in message.content: await messages[0].add_reaction('4⃣')
       if "5" in message.content: await messages[0].add_reaction('5⃣')
       if "6" in message.content: await messages[0].add_reaction('6⃣')
       if "7" in message.content: await messages[0].add_reaction('7⃣')
       if "8" in message.content: await messages[0].add_reaction('8⃣')
       if "9" in message.content: await messages[0].add_reaction('9⃣')

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="for karma"))
    # for getting emoji list
    # print('Custom Emoji ID available:')
    # emojiList = client.emojis
    # for x in range(len(emojiList)):
    #     print(emojiList[x])
    # print('------')

client.run(TOKEN)


