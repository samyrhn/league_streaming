import requests
import logging
import os

class RiotFetcher:
    def __init__(self):
        self.api_key = os.environ['RIOT_API_KEY']
        self.region = 'br1'
        self.response_file_path = 'current_match.json'
        self.logger = logging.getLogger(__name__)

    def get_summoner_id(self, summoner_name: str):
        summoner_url = f'https://{self.region}.api.riotgames.com/lol/summoner/v4/summoners/by-name/{summoner_name}?api_key={self.api_key}'
        response = requests.get(summoner_url)

        if response.status_code == 200:
            summoner_data = response.json()
            self.logger.info(summoner_data)
            print(summoner_data)
            return summoner_data['id']

        self.logger.error(f"Error getting summoner ID: {response.status_code}")
        return 
    
    def get_current_game(self, summoner_id: str):
        current_game_url = f'https://{self.region}.api.riotgames.com/lol/spectator/v4/active-games/by-summoner/{summoner_id}?api_key={self.api_key}'
        response = requests.get(current_game_url)

        if response.status_code == 200:
            current_game_data = response.json()
            return  current_game_data
        
        elif response.status_code == 404:
            self.logger.info("The summoner is not currently in a game.")
            return 

        self.logger.error(f"Error getting current game data: {response.status_code}")
        return 
    
    def get_player_current_game(self,player_name:str):
        summoner_id = self.get_summoner_id(player_name)
        data = self.get_current_game(summoner_id)
        return data
    