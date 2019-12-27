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


class FriendsList(list):
    def __init__(self, url):
        super().__init__()
        self.res = pm.request('GET', url + '/friends/')
        self.soup = BeautifulSoup(self.res.data, 'html.parser')
        self.add_friends()

    def add_friends(self):
        for fr in self.soup.find_all('a', class_='selectable_overlay'):
            self.append(id_cmp.search(fr.attrs['href']).groups()[1])


class SteamUser:
    def __init__(self, url):
        self.name = id_cmp.search(url).groups()[1]
        self.fr_list = FriendsList(url)


class UserContainer(deque):
    def __init__(self):
        super().__init__(maxlen=4)

    def add_user(self, user: SteamUser):
        self.append(user)

    def view_users(self):
        for i, u in enumerate(self):
            print(f'PLAYER {i+1}')
            print(f'USER NAME: {u.name}')
            print(f'FRIENDS: {len(u.fr_list)}')
            print(u.fr_list)
            print('*******************************')


if __name__ == '__main__':
    # Test ****************
    uc = UserContainer()

    url = input('Input steamURL: ')

    if not check_url(url):
        print('Invalid URL')
        quit(1)

    uc.append(SteamUser(url))

    uc.view_users()

    # p1 = SteamUser(url)
    # print(p1.fr_list)
