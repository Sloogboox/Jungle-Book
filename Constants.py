#{*word*} is reserved for a variables, which will be named later
#the .api.pvp.net is an endpoint. Check regional endpoints. na's is "na.api.pvp.net"
URL = {
    'base': 'https://{proxy}.api.riotgames.com{url}', # same in all urls, thus the "base case"
    'summoner_by_name': '/lol/summoner/v{version}/summoners/by-name/{namesIn}', # this object will contain summonerID and other stuff
    'current_game' : '/lol/spectator/v{version}/active-games/by-summoner/{summonerIdIn}', #spectator current game
    'match_history' : '/lol/match/v{version}/matchlists/by-account/{accountIdIn}', #match history
    'match_stats' : '/lol/match/v{version}/matches/{matchIdIn}',
    'summoner_by_sumId': '/lol/summoner/v{version}/summoners/by-account/{sumIdIn}'
    }

API_Version = {'summoner': '3', 'current_game' : '3', 'match_history' : '3', 'match_stats' : '3',
               'teammateSumId' : '3'} #version numbers for above stuff.

Regions = { 'north_america' : 'na1' }
