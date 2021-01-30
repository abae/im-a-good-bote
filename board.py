import numpy as np

#functions-------------------------------------------------------------------------
def initArray(blankArray, worldx, worldy, char):
    for row in range(worldy):
        arrayTemp = []
        for col in range(worldx):
            arrayTemp.append(char)
        blankArray.append(arrayTemp)
    return blankArray

def getPlayer(fileName):
    arrayFile = open(fileName, "r")
    line = arrayFile.readline()
    array = line.strip().split(',')
    arrayFile.close()
    return array

def addEntry(x,y, entry, entryArray, name, nameArray):
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



#make maps-------------------------------------------------------------------------
worldx = 13
worldy = 13

world = []
world = initArray(world, worldx, worldy, '0')
units = []
units = initArray(units, worldx, worldy, '0')
names = []
names = initArray(names, worldx, worldy, '')
owner = []
owner = initArray(owner, worldx, worldy, '')
players = getPlayer("players.txt")

addEntry(0,0,'2',world,"Hampter",names)
addEntry(0,0,'12',units,players[6],owner)
addEntry(6,0,'2',world,"Ladville",names)
addEntry(6,0,'12',units,players[3],owner)
addEntry(12,0,'2',world,"Jin",names)
addEntry(12,0,'12',units,players[7],owner)
addEntry(12,6,'2',world,"Zagreb",names)
addEntry(12,6,'12',units,players[2],owner)
addEntry(12,12,'2',world,"Timber Hearth",names)
addEntry(12,12,'12',units,players[0],owner)
addEntry(6,12,'2',world,"Rat Island",names)
addEntry(6,12,'12',units,players[1],owner)
addEntry(0,12,'2',world,"Nutberg",names)
addEntry(0,12,'12',units,players[5],owner)
addEntry(0,6,'2',world,"Monke",names)
addEntry(0,6,'12',units,players[4],owner)

addEntry(6,6,'2',world,"Manchesta",names)
addEntry(2,0,'1',world,"New Hampter",names)
addEntry(0,2,'1',world,"Hamter",names)
addEntry(2,2,'1',world,"Engerland",names)
addEntry(4,0,'1',world,"Whippersnapper",names)
addEntry(6,2,'1',world,"Lad",names)
addEntry(8,0,'1',world,"Laddie",names)
addEntry(10,0,'1',world,"Jin#1",names)
addEntry(10,2,'1',world,"Jin#2",names)
addEntry(12,2,'1',world,"Jin#3",names)
addEntry(12,4,'1',world,"Osijek",names)
addEntry(10,6,'1',world,"Split",names)
addEntry(12,8,'1',world,"Rijeka",names)
addEntry(12,10,'1',world,"Brittle Hollow",names)
addEntry(10,10,'1',world,"Giant's Deep",names)
addEntry(10,12,'1',world,"Ash Twin",names)
addEntry(8,12,'1',world,"Many Rat",names)
addEntry(6,10,'1',world,"Pirat",names)
addEntry(4,12,'1',world,"Beeg Rat",names)
addEntry(2,12,'1',world,"Ricardo City",names)
addEntry(2,10,'1',world,"Gachitropolis",names)
addEntry(0,10,'1',world,"Coomville",names)
addEntry(0,8,'1',world,"Shown Me",names)
addEntry(2,6,'1',world,"Have",names)
addEntry(0,4,'1',world,"You",names)
addEntry(4,4,'1',world,"Charlotte",names)
addEntry(8,4,'1',world,"Seoul",names)
addEntry(8,8,'1',world,"New York City",names)
addEntry(4,8,'1',world,"Durham",names)

textOutput(world, "map.txt")
textOutput(units, "units.txt")
textOutput(names, "names.txt")
textOutput(owner, "owner.txt")

