import re
import urllib3
import certifi
from bs4 import BeautifulSoup
from collections import deque


pm = urllib3.PoolManager(
    cert_reqs='CERT_REQUIRED',
    ca_certs=certifi.where()
)
id_cmp = re.compile(r'(id|profiles)\/(.+)\/?')


def check_url(url):
    return pm.request('GET', url + '/friends/').status == 200


class FriendsList(set):
    def __init__(self, url):
        super().__init__()
        self.res = pm.request('GET', url + '/friends/')
        self.soup = BeautifulSoup(self.res.data, 'html.parser')
        self.add_friends()

    def add_friends(self):
        for fr in self.soup.find_all('a', class_='selectable_overlay'):
            self.add(id_cmp.search(fr.attrs['href']).groups()[1])


class Friendship(set):
    pass


class FriendshipsList(list):     # List of friendships in Container
    def append(self, friendship):
        super().append(friendship)


class SteamUser:
    def __init__(self, url):
        self.name = id_cmp.search(url).groups()[1]
        self.fr_list = FriendsList(url)


class UserContainer(deque):
    def __init__(self):
        super().__init__(maxlen=4)
        self.friendship = FriendshipsList()

    def add_user(self, user: SteamUser):
        self.append(user)

    def view_users(self):
        for i, u in enumerate(self):
            print(f'PLAYER {i+1}')
            print(f'USER NAME: {u.name}')
            print(f'FRIENDS: {len(u.fr_list)}')
            print(list(u.fr_list))
            print('*******************************')

    def check_friends(self):
        pass
        # Check Users' friendship
        # Returns Friendship List ?
        # (using set ?)
        # If exists,


if __name__ == '__main__':
    # Test ****************
    uc = UserContainer()

    while True:
        url = input('Input Steam URL: ')
        if not url:
            break

        if not check_url(url):
            print('Invalid URL!')
            continue

        uc.append(SteamUser(url))
        print(f'{uc.__len__()} Users contained.')

    uc.view_users()

    # p1 = SteamUser(url)
    # print(p1.fr_list)
