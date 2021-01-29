import numpy as np

#functions-------------------------------------------------------------------------
def initArray(blankArray, worldx, worldy, char):
    for row in range(worldy):
        arrayTemp = []
        for col in range(worldx):
            arrayTemp.append(char)
        blankArray.append(arrayTemp)
    return blankArray

def addEntry(x, y, entry, entryArray, name, nameArray):
    entryArray[x][y] = entry
    nameArray[x][y] = name

def textOutput(array, filename):
    text = ""
    for i in range(len(array)):
        for j in range(len(array[0])):
            text += array[i][j]
            if j < len(array[0])-1:
                text += ','
        text += '\n'
    textFile = open(filename, "w")
    textFile.write(text)
    textFile.close()



#make maps-------------------------------------------------------------------------
worldx = 9
worldy = 9

world = []
world = initArray(world, worldx, worldy, '0')
units = []
units = initArray(units, worldx, worldy, '0')
names = []
names = initArray(names, worldx, worldy, '')
owner = []
owner = initArray(owner, worldx, worldy, '')

addEntry(2,1,'1',world,"Brittle Hollow",names)
addEntry(4,8,'2',world,"Timber Hearth",names)
addEntry(5,3,'1',world,"Giant's Deep",names)
addEntry(8,8,'1',world,"Dark Bramble",names)

textOutput(world, "map.txt")
textOutput(units, "units.txt")
textOutput(names, "names.txt")
textOutput(owner, "owner.txt")

