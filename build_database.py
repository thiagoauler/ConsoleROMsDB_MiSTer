#!/usr/bin/python3

import math
import os
import re
import sys
import time
import urllib.parse
import xml.etree.ElementTree as et

datafileGames = []
smokeMonsterPack = {}

databaseOptions = [
    ["Arcadia2001.dat",
        "U", "Arcadia2001/", "Arcadia/"],
    ["Astrocade.dat",
        "U", "Astrocade/", "Astrocade/"],
    ["Atari2600.dat",
        "U", "Atari2600/", "ATARI7800/4 Atari 2600/"],
    ["Atari5200.dat",
        "U", "Atari5200/", "ATARI5200/"],
    ["Atari7800.dat",
        "U", "Atari7800/", "ATARI7800/"],
    ["ChannelF.dat",
        "U", "ChannelF/", "ChannelF/"],
    ["ColecoVision.dat",
        "U", "ColecoVision/", "Coleco/"],
    ["DiskSystem.dat",
        "J", "DiskSystem/", "NES/4 Famicom DiskSystem/"],
    ["GameBoy.dat",
        "U", "GameBoy/", "GAMEBOY/"],
    ["GameBoyColor.dat",
        "U", "GameBoyColor/", "GAMEBOY/4 GameBoy Color/"],
    ["GameBoyAdvance.dat",
        "U", "GameBoyAdvance/", "GBA/"],
    ["GameGear.dat",
        "U", "GameGear/", "SMS/4 Game Gear/"],
    ["Intellivision.dat",
        "U", "Intellivision/", "Intellivision/"],
    ["MasterSystem.dat",
        "U", "MasterSystem/", "SMS/"],
    ["MegaDrive.dat",
        "U", "MegaDrive/", "Genesis/"],
    #["Nintendo.dat",
    #    "U", "Nintendo/", "NES/"],
    ["Odyssey2.dat",
        "U", "Odyssey2/", "ODYSSEY2/"],
    ["SG1000.dat",
        "J", "SG1000/", "Coleco/4 SG-1000/"],
    ["SuperGrafx.dat",
        "J", "SuperGrafx/", "TGFX16/4 SuperGrafx/"],
    ["SuperNintendo.dat",
        "U", "SuperNintendo/", "SNES/"],
    ["TurboGrafx.dat",
        "U", "TurboGrafx/", "TGFX16/"],
    ["VC4000.dat",
        "E", "VC4000/", "VC4000/"],
    ["Vectrex.dat",
        "U", "Vectrex/", "VECTREX/"],
    ["WonderSwan.dat",
        "J", "WonderSwan/", "WonderSwan/"],
    ["WonderSwanColor.dat",
        "J", "WonderSwanColor/", "WonderSwan/4 WonderSwan Color/"]
]

def find(searchTerm, outputPath):
    selectedGames = []
    
    # Initialize entry if necessary
    if outputPath not in smokeMonsterPack:
        smokeMonsterPack[outputPath] = {}

    # Search the term and save the game
    for gameTag in datafileGames:
        gameName = gameTag.attrib["name"]
        if searchTerm in gameName:
            romTag = gameTag.find("rom")
            smokeMonsterPack[outputPath][gameName] = romTag
            selectedGames.append(gameTag)

    # Remove selected games from database
    for gameTag in selectedGames:
        datafileGames.remove(gameTag)

def findByRegion(searchTerm, outputPath):
    selectedGames = []
    
    # Search the term and save the game
    for gameTag in datafileGames:
        gameName = gameTag.attrib["name"]
        region = re.search("\(\w\w\w.*?\)", gameName).group()
        region = region.replace("(", "").replace(")", "") + "/"
        outputPathRegion = outputPath + region
        
        # Initialize entry if necessary
        if outputPathRegion not in smokeMonsterPack:
            smokeMonsterPack[outputPathRegion] = {}
        
        if searchTerm in gameName:
            romTag = gameTag.find("rom")
            smokeMonsterPack[outputPathRegion][gameName] = romTag
            selectedGames.append(gameTag)

    # Remove selected games from database
    for gameTag in selectedGames:
        datafileGames.remove(gameTag)

def findByLetter(searchTerm, outputPath):
    selectedGames = []

    letterA = ord("A")
    letterZ = ord("Z")
    maxThreshold = 200

    countTotal = 0
    countLetter = {}
    for letter in range(letterA, letterZ + 1):
        countLetter[letter] = 0

    region = searchTerm.split("|")[0]
    searchTerm = "\(.*?(" + searchTerm + ").*?\)"
    for gameTag in datafileGames:
        gameName = gameTag.attrib["name"]
        match = re.search(searchTerm, gameName)
        if match != None:
            firstChar = gameName[0].upper()
            if firstChar.isalpha():
                letter = ord(firstChar)
            else:
                letter = letterA
            if letter < letterA or letter > letterZ:
                print("> Invalid First Char:", gameName)
            countTotal = countTotal + 1
            countLetter[letter] = countLetter[letter] + 1;
            selectedGames.append(gameTag)

    if countTotal > 0:
        threshold = math.ceil(countTotal / maxThreshold)
        threshold = math.ceil(countTotal / threshold)

        indexIni = letterA
        indexEnd = letterA
        acumulator = 0
        while indexEnd <= letterZ:
            acumulator = acumulator + countLetter[indexEnd]
            if acumulator > threshold:
                indexEnd = indexEnd - 1
                if indexEnd < indexIni:
                    indexEnd = indexIni
                if indexIni == indexEnd:
                    rangeChar = " [" + chr(indexIni) + "]/"
                else:
                    rangeChar = " [" + chr(indexIni) + "-" + chr(indexEnd) + "]/"
                    
                for gameTag in selectedGames:
                    gameName = gameTag.attrib["name"]
                    firstChar = gameName[0].upper()
                    if firstChar.isalpha():
                        letter = ord(firstChar)
                    else:
                        letter = letterA
                    if letter >= indexIni and letter <= indexEnd:
                        if indexIni == letterA and indexEnd == letterZ and outputPath != "1 ":
                            outputPath = "2 "
                        outputPathRegion = outputPath + region + rangeChar
                        
                        # Initialize entry if necessary
                        if outputPathRegion not in smokeMonsterPack:
                            smokeMonsterPack[outputPathRegion] = {}
                        
                        romTag = gameTag.find("rom")
                        smokeMonsterPack[outputPathRegion][gameName] = romTag
                acumulator = 0
                indexIni = indexEnd + 1
            indexEnd = indexEnd + 1

        if indexIni <= letterZ:
            indexEnd = indexEnd - 1
            if indexEnd < indexIni:
                indexEnd = indexIni
            if indexIni == indexEnd:
                rangeChar = " [" + chr(indexIni) + "]/"
            else:
                rangeChar = " [" + chr(indexIni) + "-" + chr(indexEnd) + "]/"
            for gameTag in selectedGames:
                gameName = gameTag.attrib["name"]
                firstChar = gameName[0].upper()
                if firstChar.isalpha():
                    letter = ord(firstChar)
                else:
                    letter = letterA
                if letter >= indexIni and letter <= indexEnd:
                    if indexIni == letterA and indexEnd == letterZ and outputPath != "1 ":
                            outputPath = "2 "
                    outputPathRegion = outputPath + region + rangeChar
                    
                    # Initialize entry if necessary
                    if outputPathRegion not in smokeMonsterPack:
                        smokeMonsterPack[outputPathRegion] = {}
                    
                    romTag = gameTag.find("rom")
                    smokeMonsterPack[outputPathRegion][gameName] = romTag
    
    # Remove selected games from database
    for gameTag in selectedGames:
        datafileGames.remove(gameTag)

if __name__ == "__main__":
    
    # Print Downloader database file
    print("{")
    print("   \"base_files_url\" : \"\",")
    print("   \"db_files\" : [],")
    print("   \"db_id\" : \"console_roms_db\",")
    print("   \"default_options\" : {},")
    print("   \"files\" :")
    print("   {")
    
    isFirst = True    
    for options in databaseOptions:
        smokeMonsterPack = {}
        
        datafile   = options[0]    
        mainRegion = options[1]
        inputPath  = options[2]
        outputPath = options[3]
    
        datafileGames = et.parse("DataBases/" + datafile).findall("game")

        # Atari Add-ons
        find("SC3000", "4 SC-3000/")
        find("SC-3000", "4 SC-3000/")
        find("SF-7000", "4 SF-7000/")
        find("Othello Multivision", "4 Othello Multivision/")
        find(".WAV", "4 Kid Vid Voice Module (USA) (Audio Tapes)/")

        # BIOS
        find("[BIOS]", "3 BIOS/")
        find("(Competition Cart)", "3 BIOS/Competition Cart/")
        find("(Program)", "3 BIOS/Program/")
        find("(Enhancement Chip)", "3 BIOS/Enhancement Chip/")
        find("(Test Program)", "3 BIOS/Test Program/")

        # Collections
        find("(Arcade)", "3 Collection/Nintendo Super System/")
        find("(NP)", "3 Collection/Nintendo Power/")
        find("Atari Anthology", "3 Collection/Atari Anthology/")
        find("Bomberman Collection", "3 Collection/Bomberman Collection/")
        find("Castlevania Advance Collection", "3 Collection/Castlevania Advance Collection/")
        find("Castlevania Anniversary Collection", "3 Collection/Castlevania Anniversary Collection/")
        find("Classic NES Series", "3 Collection/Classic NES Series, NES Classics/")
        find("Collection of Mana", "3 Collection/Collection of Mana/")
        find("Collection of SaGa", "3 Collection/Collection of SaGa/")
        find("Contra Anniversary Collection", "3 Collection/Contra Anniversary Collection/")
        find("Darius Cozmic Collection", "3 Collection/Darius Cozmic Collection/")
        find("Disney Classic Games", "3 Collection/Disney Classic Games/")
        find("Famicom Mini", "3 Collection/Famicom Mini/")
        find("Game Boy Advance Video", "3 Collection/Game Boy Advance Video/")
        find("Game no Kanzume Otokuyou", "3 Collection/Game no Kanzume Otokuyou/")
        find("Genesis Mini", "3 Collection/Genesis Mini, Mega Drive Mini/")
        find("Kiosk", "3 Collection/Kiosk/")
        find("Konami Collector's Series", "3 Collection/Konami Collector's Series/")
        find("Mega Drive Mini", "3 Collection/Genesis Mini, Mega Drive Mini/")
        find("Mega Man Legacy Collection", "3 Collection/Mega Man Legacy Collection/")
        find("Mega Man X Legacy Collection", "3 Collection/Mega Man X Legacy Collection/")
        find("Namco Museum Archives Vol 1", "3 Collection/Namcot Collection, Namco Museum Archives/")
        find("Namco Museum Archives Vol 2", "3 Collection/Namcot Collection, Namco Museum Archives/")
        find("Namcot Collection", "3 Collection/Namcot Collection, Namco Museum Archives/")
        find("NES Classics", "3 Collection/Classic NES Series, NES Classics/")
        find("PC Rerelease", "3 Collection/PC Rerelease/")
        find("Sega Ages", "3 Collection/Sega Ages/")
        find("Sega Channel", "3 Collection/Sega Channel, SegaNet/")
        find("SEGA Classic Collection", "3 Collection/SEGA Classic Collection/")
        find("Sega Smash Pack", "3 Collection/Sega Smash Pack/")
        find("SegaNet", "3 Collection/Sega Channel, SegaNet/")
        find("Seiken Densetsu Collection", "3 Collection/Collection of Mana/")
        find("SNK 40th Anniversary Collection", "3 Collection/SNK 40th Anniversary Collection/")
        find("Sonic Classic Collection", "3 Collection/Sonic Classic Collection/")
        find("The Disney Afternoon Collection", "3 Collection/The Disney Afternoon Collection/")
        #find("", "3 Collection//")

        # Virtual Console
        findByRegion("Switch Online", "3 Collection/Virtual Console/")
        findByRegion("Virtual Console", "3 Collection/Virtual Console/")
        #findByRegion("", "3 Collection/Virtual Console/")

        # Old Console Ports
        find("GameCube", "3 Collection/GameCube/")
        find("Wii", "3 Collection/Wii/")

        # Revisions
        find("(Beta", "3 Revisions/Beta/")
        find("(Demo", "3 Revisions/Demo/")
        find("(Prerelease", "3 Revisions/Prerelease/")
        find("(Proto", "3 Revisions/Prototype/")
        find("(Possible Proto", "3 Revisions/Prototype/")
        find("(Sample", "3 Revisions/Sample/")
        find("(Tech Demo", "3 Revisions/Demo/")
        find("(Alt", "3 Revisions/Alternative/")

        # Unlicensed
        find("(Aftermarket)", "2 Unlicensed/Aftermarket/")
        find("(Pirate)", "2 Unlicensed/Pirate/")
        findByRegion("(Unl)", "2 Unlicensed/")

        # Other "conflicting" Collections :[
        find("Collector's Edition", "3 Collection/Collector's Edition/")

        # Main Regions
        if mainRegion == "U":
            findByLetter("USA|World", "1 ")
            findByLetter("Europe", "2 Europe [A-Z]/")
            findByLetter("Japan", "2 Japan [A-Z]/")
        if mainRegion == "E":
            findByLetter("Europe|World", "1 ")
            findByLetter("Japan", "2 Japan [A-Z]/")
        if mainRegion == "J":
            findByLetter("Japan|World", "1 ")

        # Other Regions
        findByRegion("", "2 Other Regions/")

        # Print any uncategorized ROM
        for gameTag in datafileGames:
            gameName = gameTag.attrib["name"]
            print(">", gameName)
    
        for gamePath, selectedGames in sorted(smokeMonsterPack.items()):
            gameOutputPath = outputPath + gamePath
            for gameName, romTag in sorted(selectedGames.items()):
                if isFirst:
                    isFirst = False
                else:
                    print("      },")
                romName, romExtension = os.path.splitext(romTag.attrib["name"])
                romExtension = romExtension.lower()
                romHash = romTag.attrib["md5"].lower()
                romSize = romTag.attrib["size"]
                print("      \"games/" + gameOutputPath + romName + romExtension + "\": {")
                print("         \"hash\" : \"" + romHash + "\",")
                print("         \"overwrite\" : \"true\",")
                print("         \"size\" : " + romSize + ",")
                print("         \"url\" : \"file://" + urllib.parse.quote("/media/fat/cifs/" + inputPath + romHash + ".rom") + "\"")
    print("      }")
    print("   },")
    print("   \"folders\" :")
    print("   {")
    print("      \"games\" : {}")
    print("   },")
    print("   \"timestamp\" : " + str(int(time.time())) + ",")
    print("   \"zips\" : {}")
    print("}")