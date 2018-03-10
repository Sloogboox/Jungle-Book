import requests #program downloaded at beginning
import Constants as Consts #We can refer to Constants as "Consts" now.

class RiotAPI(object): #inherits objects, which is nothing
    #self is an instant of this ojbect _ = private __ = public
    def __init__(self, api_key, region = Consts.Regions['north_america']) : #like a constructor from other languages. "North America" is a default.
        self.api_key = api_key
        self.region = region

    def _request(self, api_url): #params is null, nothing
        args = {'api_key' : self.api_key} #api key is in Request URL after '?'

        #I removed that HTML stuff. Was just a bunch of useless gens that made a for statement never be reached                   
        response = requests.get(
            Consts.URL['base'].format(
                proxy = self.region,
                url = api_url
                ),
            params = args
            )
        return response.json() #we get the response body as a parsed string into a dictionary. Response body from api webpage

    def get_summoner_by_name(self, name):
        api_url = Consts.URL['summoner_by_name'].format(
            version = Consts.API_Version['summoner'],
            namesIn = name 
            )
            
        return self._request(api_url)
    
    def get_current_game(self, summonerId):
        api_url = Consts.URL['current_game'].format(
            version = Consts.API_Version['current_game'],
            summonerIdIn = summonerId
            )

        return self._request(api_url)

    def get_match_history(self, accountId):
        api_url = Consts.URL['match_history'].format(
            version = Consts.API_Version['match_history'],
            accountIdIn = accountId
            )
        return self._request(api_url)

    def get_match_stats(self, matchId):
        api_url = Consts.URL['match_stats'].format(
            version = Consts.API_Version['match_stats'],
            matchIdIn = matchId
            )
        return self._request(api_url)
