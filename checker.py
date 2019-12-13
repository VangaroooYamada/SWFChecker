import requests
import yaml
from collections import deque


with open('./private.yaml') as private:
    data = yaml.safe_load(private)

API_KEY = data['API_key']
steam_id = data['My_ID64']


FL_url = 'http://api.steampowered.com/ISteamUser/GetFriendList/v0001/'
params = {
    'key': API_KEY,
    'steamID': steam_id,
    'relationship': 'friend'
}


class Player():
    def __init__(self, steam_id):
        self.steam_id = steam_id

    def check_friend(self):
        params['steamID'] = self.steam_id
        self.res = requests.get(FL_url, params=params)
        self.friends = self.res.json()['friendslist']['friends']


class PlayersQueue(deque):

    def __init__(self, maxlen=4):
        super().__init__([], maxlen=maxlen)


if __name__ == '__main__':
    res = requests.get(FL_url, params=params)

    if not res.status_code == 200:
        print('Access Error: {}'.format(res.status_code))
        quit()

# How to convert CustomID to SteamID64??????

    print(res.json())
