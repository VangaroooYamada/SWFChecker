import re
import urllib3
import certifi
import networkx as nx
from bs4 import BeautifulSoup


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


class SteamUser:
    def __init__(self, url):
        self.res = pm.request('GET', url)
        self.soup = BeautifulSoup(self.res.data, 'html.parser')

        self.name = self.soup.find('span', class_='actual_persona_name').string
        self.id = id_cmp.search(url).groups()[1]
        self.fr_list = FriendsList(url)


class UserContainer(nx.Graph):
    def add_user(self, user: SteamUser):
        self.add_node(user)
        for u in self:
            if u == user:
                continue
            if u.id in user.fr_list:
                self.add_edge(user, u)
        print(self.get_friends())

    def view_users(self):
        for i, u in enumerate(self):
            print(f'PLAYER {i+1}')
            print(f'USER NAME: {u.name}')
            print(f'FRIENDS: {len(u.fr_list)}')
            # print(list(u.fr_list))
            print('*******************************')

    def view_friends(self):
        '''
        Check Users' friendship
        Returns Friendship List
        '''
        for e in self.edges:
            print(f'{e[0].name} - {e[1].name}')

    def get_friends(self):
        if self.number_of_edges() == 5 or self.number_of_edges() == 6:    # All Party
            return [[n.name for n in self.nodes]]

        if self.number_of_edges() == 4:
            if 3 not in [deg for node, deg in self.degree()]:
                return [[e[0].name, e[1].name] for e in self.edges]

            return [[n.name for n in self.nodes if not self.degree[n] == 2],
                    [n.name for n in self.nodes if not self.degree[n] == 1]]

        if self.number_of_edges() == 3:
            if 0 not in [deg for node, deg in self.degree()]:
                return [[n.name for n in self.nodes if not self.degree[n] == 0]]

        return [[e[0].name, e[1].name] for e in self.edges]


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

        uc.add_user(SteamUser(url))
        print(f'{uc.__len__()} Users contained.')

    uc.view_users()
