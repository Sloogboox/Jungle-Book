#A file to hold all the classes I used, better than having a bajillion files in this case.
from API import RiotAPI #imports class RiotAPI from Doc API
from PlayersAndInfo import Player
from pathlib2 import Path
from bs4 import BeautifulSoup
from time import strftime
import os.path
import glob
import pickle
import binascii
import requests
import subprocess
import time
import smtplib
from email.mime.text import MIMEText

#function to save user data
def save_data(fileName, data):   
    #if try has an error, then the except block is written.
    try:
        print ("Saving...")
        pickle.dump(data, open(fileName, "wb") )
        print ("Saved!")
            
    except:
        print ("Oh No! Unable To Save Data.")
            
#function to load data
def load_data(fileName, APIkey):
    try: 
        data = pickle.load( open( fileName, "rb" ) )
        print ("Loaded Data Correctly!")
        return data
            
    except: 
        print ("Unable To Load User Data")
        sumName = find_user_summoner_name()
        userInfo = APIkey.get_summoner_by_name(sumName)
        save_data("user_data", userInfo)
        return userInfo
        

#function to find username, if already found return immediatly
def find_user_summoner_name():  
##    initialPath = "C:\Riot Games" #inital directory to check
##
##    outdated, league removed air client
##    #if path does exist, find the summoner name in game files.
##    if Path(initialPath).exists():
##        finalPath = initialPath + "\League of Legends\RADS\projects\lol_air_client\\releases\\0.0.1.241\deploy\preferences\*.properties"
##        sumName = os.path.splitext(os.path.basename(glob.glob(finalPath)[0]))[0]
##        return sumName

    #ask user for sum name and saves it. Then just uses that
    
    var = raw_input("Couldn't Find Game Directory! Please Enter Your Summoner Name: ")
    print ("you entered", var)
    sumName = var
    return var
      
def search_for_teammates(playerInfo, userInfo):
    count = 0
    flag = False
    team1 = []
    team2 = []

    while count <= 9:    
        if playerInfo['participants'][count]['teamId'] == 100:
            x = playerInfo['participants'][count]['summonerName']

            #if user is on this team, then set a flag so I only look for teammates
            if x == userInfo['name']:
                flag = True
            
            xHex = x.encode('hex')
            team1.append(xHex)
            
        else:
            y = playerInfo['participants'][count]['summonerName']
            
            #if user is on this team, then set a flag so I only look for teammates        
            yHex = y.encode('hex')
            team2.append(yHex)

        count = count + 1

    if flag == True:
        return team1
    else:
        return team2
    
#get URL
def get_Op_URL(name):
    part1 = 'https://na.op.gg/summoner/userName='
    URL = part1 + name

    return URL

#find percentage of winrate using total wins and games played
def win_percent_maker(wins, games):
    tempWins = float(wins)
    games = float(games)
    percent = (tempWins / games) * 100
    percent = str(percent) + '%'
    return percent              

#scrape info from OP.GG and create player objects
def player_creator(URL, name):
    try:
        #download HTML doc
        r = requests.get(URL)
    except:
        print ("OP.gg is not responding.")
        raw_input("press any key to exit.")
        exit()

    soup = BeautifulSoup(r.content, "lxml")
    x = soup.find_all(class_="GameLength")
    division = soup.find(class_="tierRank").string

    #if there is enough games for data to be gathered
    if len(x) > 19:
        wins = soup.find(class_="win").string    
        losses = soup.find(class_="lose").string
        winRatio = win_percent_maker(wins, len(x))
        avgCS = 'NA'
        #avgCS = soup.find(class_="cs average").string
        kda = soup.find(class_="KDARatio").find(class_="KDARatio").string
        killPartic = soup.find(title="Kill Participation").find_next().string

        #find all past games and compute CS per minute, control wards per game, etc
        gameTimes = []
        csPerMins = []
        controlWards = []
    
        gameTime = soup.find(class_="GameLength")
        csPerMin = soup.find(class_="CS tip")
        controlWardPerGame = soup.find(class_="wards vision")
        count = 0

        #len(x) should return amount of items in gameLenght list, max 20
        while count < len(x) and len(x) > 20:
        
            gameTimes.append(gameTime.findNext(class_="GameLength"))
            csPerMins.append(csPerMin.findNext(class_="CS tip"))
            controlWards.append(controlWardPerGame.findNext(class_="wards vision"))

            count = count + 1

    #not enough data, so mark most Not Available
    else:
        wins = 'NA' 
        losses = 'NA'
        winRatio = 'NA'
        avgCS = 'NA'
        kda = 'NA'
        killPartic = 'NA'
        gameTimes = ['NA']
        csPerMins = ['NA']
        controlWards = ['NA']

    currPlayer = Player(name, division, winRatio, "NA", "NA", kda, killPartic,
                        "NA", "NA", "NA")
    
    #playerList.append(currPlayer)

    return currPlayer
    
#find data on player and create player object
def get_player_objects(teammates):
    count = 0
    playerObjList = []

    while count <= 4:
        x = binascii.unhexlify(teammates[count])
        URL = get_Op_URL(x)
        player = player_creator(URL, x)
        playerObjList.append(player)
        
        count = count + 1
        

    return playerObjList

def check_loading_screen():

    hour = strftime("%H")
    minute = strftime("%M")
    day = strftime("%d")
    month = strftime("%m")
    year = strftime("%Y")
    secs = strftime("%S")

    filePath1 = 'C:\Riot Games\League of Legends\Logs\GameLogs\\'
    folderName = year + "-" + month + "-" + day + "T" + hour + "-" + minute + "-" + secs
    filePath1 += folderName + "\\" + folderName + "_r3dlog.txt"
    
    while not os.path.exists(filePath1):
        #let filePath2 lag one step behind
        filePath2 = filePath1
        time.sleep(.8)
        
        hour = strftime("%H")
        minute = strftime("%M")
        day = strftime("%d")
        month = strftime("%m")
        year = strftime("%Y")
        secs = strftime("%S") 

        filePath1 = 'C:\Riot Games\League of Legends\Logs\GameLogs\\'
        folderName = year + "-" + month + "-" + day + "T" + hour + "-" + minute + "-" + secs
        filePath1 += folderName + "\\" + folderName + "_r3dlog.txt"

        if os.path.exists(filePath2):
            break
        

def display_text():
    print ("in display test")
