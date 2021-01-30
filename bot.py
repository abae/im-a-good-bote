# Work with Python 3.6
import discord
import random
import math
import asyncio
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

def addEntry(x, y, entry, entryArray, name, nameArray):
    entryArray[x][y] = entry
    nameArray[x][y] = name

def textOutput(array, fileName):
    text = ""
    for i in range(len(array)):
        for j in range(len(array[0])):
            text += array[i][j]
            if j < len(array[0])-1:
                text += ','
        text += '\n'
    textFile = open(fileName, "w")
    textFile.write(text)
    textFile.close()

#timer
async def checkTime():
    await client.wait_until_ready()
    channelID = 284408867444490259
    #channelID = 804873337612271666
    channel = client.get_channel(channelID)
    while True:
        world = getArrayFile("map.txt")
        units = getArrayFile("units.txt")
        for i in range(len(world)):
            for j in range(len(world[0])):
                if int(units[i][j]) > 0:
                    if world[i][j] == '1':
                        units[i][j] = str(int(units[i][j]) + 4)
                    if world[i][j] == '2':
                        units[i][j] = str(int(units[i][j]) + 8)
        textOutput(units, "units.txt")

        await channel.send("12:00 PM: New units have arrived at each city")
        await asyncio.sleep(60*60*24)
    

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
        players = getArrayFile("players.txt")
        playerDict = {}
        for i in range(len(players[0])):
            playerDict[players[0][i]] = players[1][i]
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
                        worldMessage += playerDict[owner[i][j]]
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
        players = getArrayFile("players.txt")
        playerDict = {}
        for i in range(len(players[0])):
            playerDict[players[0][i]] = players[1][i]
        args = message.content.strip().split(' ')
        error = False
        infoMessage = ""
        if len(args) != 2:
            error = True
        if args[0] != "!info":
            error = True
        if len(args[1]) != 2:
            error = True
        locX = ord(args[1][0]) - 65
        locY = ord(args[1][1]) - 49
        if locX < 0 or locX > worldx-1 or locY < 0 or locY > worldy-1:
            error = True
        if error:
            pass
            #await channel.send("error, invalid command\n!info [location]\ni.e. !info B3\ntry !help for more info")
        else:
            if world[locY][locX] == '0':
                if units[locY][locX] == '0':
                    infoMessage += ":white_large_square: "+args[1]+": empty area"
                else:
                    infoMessage += playerDict[owner[locY][locX]]+" "+args[1]+": "+owner[locY][locX]+"'s square with "+units[locY][locX]+" units"
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

    if "!move" in message.content:
        world = getArrayFile("map.txt")
        names = getArrayFile("names.txt")
        symbols = getArrayFile("symbols.txt")
        units = getArrayFile("units.txt")
        owner = getArrayFile("owner.txt")
        players = getArrayFile("players.txt")
        playerDict = {}
        for i in range(len(players[0])):
            playerDict[players[0][i]] = players[1][i]
        args = message.content.strip().split(' ')
        error = False
        moveMessage = ""
        #correct number of arg
        if len(args) != 4:
            error = True
            print("not enough args")
        #correct command name
        if args[0] != "!move":
            error = True
            print("not right command")
        #locations have 2 coord
        if len(args[2]) != 2 or len(args[3]) != 2:
            error = True
            print("2 coords for each loc")
        #location translation
        locFrom = [ord(args[2][0])-65, ord(args[2][1])-49]
        locTo = [ord(args[3][0])-65, ord(args[3][1])-49]
        #make sure location is in map
        if locFrom[0] < 0 or locFrom[0] > worldx-1 or locFrom[1] < 0 or locFrom[1] > worldy-1:
            error = True
            print("out of map")
        if locTo[0] < 0 or locTo[0] > worldx-1 or locTo[1] < 0 or locTo[1] > worldy-1:
            error = True
            print("out of range")
        #make sure there are enough units
        if int(args[1]) < 2 or int(args[1]) > int(units[locFrom[1]][locFrom[0]]):
            error = True
            print("wrong number of units")
        #make sure locations are 1 king's move away
        if locFrom == locTo:
            error = True
        if abs(locTo[0] - locFrom[0]) > 1:
            error = True
        if abs(locTo[1] - locFrom[1]) > 1:
            error = True
        #make sure the message author owns the location
        if owner[locFrom[1]][locFrom[0]] != message.author.mention:
            error = True
            print("not right owner")
        if error:
            pass
            #await channel.send("movement error\n!move [# of units] [location from] [location to]\ntry !help for more info")
        else:
            #moving to a new square
            if units[locTo[1]][locTo[0]] == '0':
                units[locTo[1]][locTo[0]] = str(int(args[1])-2)
                if units[locTo[1]][locTo[0]] != '0':
                    owner[locTo[1]][locTo[0]] = message.author.mention
                units[locFrom[1]][locFrom[0]] = str(int(units[locFrom[1]][locFrom[0]])-int(args[1]))
                if units[locFrom[1]][locFrom[0]] == '0':
                    owner[locFrom[1]][locFrom[0]] = ''
                textOutput(units, "units.txt")
                textOutput(owner, "owner.txt")
                moveMessage += message.author.mention+" took control of a new square at "+args[3]+" with "+str(int(args[1])-2)+" units."
            #moving to a owned square
            elif owner[locTo[1]][locTo[0]] == message.author.mention:
                units[locTo[1]][locTo[0]] = str(int(units[locTo[1]][locTo[0]])+int(args[1])-1)
                units[locFrom[1]][locFrom[0]] = str(int(units[locFrom[1]][locFrom[0]])-int(args[1]))
                if units[locFrom[1]][locFrom[0]] == '0':
                    owner[locFrom[1]][locFrom[0]] = ''
                textOutput(units, "units.txt")
                textOutput(owner, "owner.txt")
                moveMessage += message.author.mention+" moved "+str(int(args[1])-1)+ " units from "+args[2]+" to "+args[3]
            #attack
            else:
                attackingUnits = int(args[1])
                #defensive advantage
                if world[locTo[1]][locTo[0]] == '0':
                    attackingUnits -= int(math.ceil(int(units[locTo[1]][locTo[0]])*0.1))
                elif world[locTo[1]][locTo[0]] == '1':
                    attackingUnits -= int(math.ceil(int(units[locTo[1]][locTo[0]])*0.2))
                else:
                    attackingUnits -= int(math.ceil(int(units[locTo[1]][locTo[0]])*0.5))
                #failed attack
                if attackingUnits < 1:
                    units[locFrom[1]][locFrom[0]] = str(int(units[locFrom[1]][locFrom[0]])-int(args[1]))
                    if units[locFrom[1]][locFrom[0]] == '0':
                        owner[locFrom[1]][locFrom[0]] = ''
                    textOutput(units, "units.txt")
                    textOutput(owner, "owner.txt")
                    moveMessage += message.author.mention+" tried to attack "+owner[locTo[1]][locTo[0]]+" at "+args[3]+" and failed. They lost "+args[1]+" units in the process LULW"
                #defense win
                elif attackingUnits < int(units[locTo[1]][locTo[0]]):
                    units[locTo[1]][locTo[0]] = str(int(units[locTo[1]][locTo[0]])-attackingUnits)
                    units[locFrom[1]][locFrom[0]] = str(int(units[locFrom[1]][locFrom[0]])-int(args[1]))
                    if units[locFrom[1]][locFrom[0]] == '0':
                        owner[locFrom[1]][locFrom[0]] = ''
                    textOutput(units, "units.txt")
                    textOutput(owner, "owner.txt")
                    moveMessage += owner[locTo[1]][locTo[0]]+" successfully defended against "+message.author.mention+"'s force of "+args[1]+" units, but also lost "+str(attackingUnits)+" units in the process."
                #attack win
                elif attackingUnits > int(units[locTo[1]][locTo[0]]):
                    p_units = units[locTo[1]][locTo[0]]
                    units[locTo[1]][locTo[0]] = str(attackingUnits - int(units[locTo[1]][locTo[0]]))
                    p_owner = owner[locTo[1]][locTo[0]]
                    owner[locTo[1]][locTo[0]] = message.author.mention
                    units[locFrom[1]][locFrom[0]] = str(int(units[locFrom[1]][locFrom[0]])-int(args[1]))
                    if units[locFrom[1]][locFrom[0]] == '0':
                        owner[locFrom[1]][locFrom[0]] = ''
                    textOutput(units, "units.txt")
                    textOutput(owner, "owner.txt")
                    moveMessage += message.author.mention+" took over "+args[3]+ " from "+p_owner+"\n"+message.author.mention+" lost "+str(int(args[1])-int(units[locTo[1]][locTo[0]]))+" units and "+p_owner+" lost "+p_units+" units in the battle"
                #tie
                elif attackingUnits == int(units[locTo[1]][locTo[0]]):
                    units[locTo[1]][locTo[0]] = '0'
                    p_owner = owner[locTo[1]][locTo[0]]
                    owner[locTo[1]][locTo[0]] = ''
                    units[locFrom[1]][locFrom[0]] = str(int(units[locFrom[1]][locFrom[0]])-int(args[1]))
                    if units[locFrom[1]][locFrom[0]] == '0':
                        owner[locFrom[1]][locFrom[0]] = ''
                    textOutput(units, "units.txt")
                    textOutput(owner, "owner.txt")
                    moveMessage += message.author.mention+" fought "+p_owner+" at "+args[3]+" and there was no clear victor.\n"+message.author.mention+" lost "+args[1]+" units and "+p_owner+" lost "+str(attackingUnits)+" units in the battle"
            await channel.send(moveMessage)

    if "!transfer" in message.content:
        world = getArrayFile("map.txt")
        names = getArrayFile("names.txt")
        symbols = getArrayFile("symbols.txt")
        units = getArrayFile("units.txt")
        owner = getArrayFile("owner.txt")
        players = getArrayFile("players.txt")
        playerDict = {}
        for i in range(len(players[0])):
            playerDict[players[0][i]] = players[1][i]
        args = message.content.strip().split(' ')
        error = False
        transferMessage = ""
        #correct number of arg
        if len(args) != 4:
            error = True
        #correct command name
        if args[0] != "!transfer":
            error = True
        #locations have 2 coord
        if len(args[2]) != 2 or len(args[3]) != 2:
            error = True
        #location translation
        locFrom = [ord(args[2][0])-65, ord(args[2][1])-49]
        locTo = [ord(args[3][0])-65, ord(args[3][1])-49]
        #make sure location is in map
        if locFrom[0] < 0 or locFrom[0] > worldx-1 or locFrom[1] < 0 or locFrom[1] > worldy-1:
            error = True
        if locTo[0] < 0 or locTo[0] > worldx-1 or locTo[1] < 0 or locTo[1] > worldy-1:
            error = True
        #make sure there are enough units
        if int(args[1]) < 1 or int(args[1]) > int(units[locFrom[1]][locFrom[0]]):
            error = True
        #make sure the message author owns the location
        if owner[locFrom[1]][locFrom[0]] != message.author.mention:
            error = True
        #make sure sending to another player's city
        if owner[locTo[1]][locTo[0]] == message.author.mention or owner[locTo[1]][locTo[0]] == '':
            error = True
        if world[locTo[1]][locTo[0]] != '2':
            error = True
        if error:
            pass
            #await channel.send("movement error\n!move [# of units] [location from] [location to]\ntry !help for more info")
        else:
            units[locTo[1]][locTo[0]] = str(int(units[locTo[1]][locTo[0]])+int(args[1]))
            p_owner = owner[locTo[1]][locTo[0]]
            units[locFrom[1]][locFrom[0]] = str(int(units[locFrom[1]][locFrom[0]])-int(args[1]))
            if units[locFrom[1]][locFrom[0]] == '0':
                owner[locFrom[1]][locFrom[0]] = ''
            textOutput(units, "units.txt")
            textOutput(owner, "owner.txt")
            transferMessage += message.author.mention+" transferred "+args[1]+" units to "+p_owner+"'s capital at "+args[3]

            await channel.send(transferMessage)
    
    if message.content == "!claim_victory":
        world = getArrayFile("map.txt")
        owner = getArrayFile("owner.txt")
        claimed = 0
        total = 0
        for i in range(len(world)):
            for j in range(len(world[0])):
                if world[i][j] != '0':
                    total += 1
                    if owner[i][j] == message.author.mention:
                        claimed += 1
        if claimed > total/2:
            await channel.send("Congratulations "+message.author.mention+" you are the winner!")
        else:
            await channel.send("Sorry, it doesn't seem like you've won yet...")

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

client.loop.create_task(checkTime())
client.run(TOKEN)


