import subprocess
from API import RiotAPI #imports class RiotAPI from Doc API
from PlayersAndInfo import Player
from ClassesAndFunctions import load_data
from ClassesAndFunctions import search_for_teammates
from ClassesAndFunctions import get_player_objects
from ClassesAndFunctions import check_loading_screen
from ClassesAndFunctions import display_text


#next 2 things are just what is always added, as a lock to make sure it runs 
def main():

    api = RiotAPI('API-KEY GOES HERE') #API key from riotgames site
                  
    #Load Data
    userInfo = load_data("user_data", api)
    print (userInfo)
    flag = True
    while flag == True:

        #check if person is in game
        check_loading_screen()

        #load Data from current game
        currentGameData = api.get_current_game(userInfo['id'])

        try:
            #get list of teammates' summoner names in hex 
            teammateList = search_for_teammates(currentGameData, userInfo)
            
            #creates and returns a list of player objects
            playerObjList = get_player_objects(teammateList)
            print ("obj list?")
            print (playerObjList[1].get_current_division())

        except:
            #restart program
            #display text box
            display_text()#playerObjList)
            
if __name__ == "__main__":
    main()
