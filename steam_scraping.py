import re
import urllib3
import certifi
from bs4 import BeautifulSoup


pm = urllib3.PoolManager(
    cert_reqs='CERT_REQUIRED',
    ca_certs=certifi.where()
)
id_cmp = re.compile(r'(id|profile)\/(.+)\/?')


class SteamUser:
    def __init__(self, url):
        self.name = id_cmp.search(url).groups(2)
        self.res = pm.request('GET', url + '/friends/')
        self.soup = BeautifulSoup(self.res.data, 'html.parser')
        self.fr_list = list(self.soup.find_all('a', class_='selectable_overlay'))

    def show_friends(self):
        for n in self.fr_list:
            print(n.attrs['href'])

    def check_friend(self):
        pass


if __name__ == '__main__':
    # Test ****************
    url = input('Input steamURL: ')

    p1 = SteamUser(url)
    p1.show_friends()

    # for f in friends_list:
    #     print(f.attrs['href'])
