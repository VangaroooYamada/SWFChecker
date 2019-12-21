import re
import urllib3
import certifi
from bs4 import BeautifulSoup


pm = urllib3.PoolManager(
    cert_reqs='CERT_REQUIRED',
    ca_certs=certifi.where()
)
id_cmp = re.compile(r'(id|profiles)\/(.+)\/?')


def check_url(url):
    return pm.request('GET', url + '/friends/').status == 200


class SteamUser:
    def __init__(self, url):
        self.name = id_cmp.search(url).groups()[1]
        self.res = pm.request('GET', url + '/friends/')
        self.soup = BeautifulSoup(self.res.data, 'html.parser')
        self.fr_list = [
            id_cmp.search(fr.attrs['href']).groups()[1] for fr
            in self.soup.find_all('a', class_='selectable_overlay')]

    def show_friends(self):
        print(f'My name is {self.name}({len(self.fr_list)})')
        for n in self.fr_list:
            print(n)

    def check_friend(self):
        pass


if __name__ == '__main__':
    # Test ****************
    url = input('Input steamURL: ')

    if not check_url(url):
        print('Invalid URL')
        quit(1)

    p1 = SteamUser(url)
    p1.show_friends()
