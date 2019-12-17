import urllib3
import certifi
from bs4 import BeautifulSoup


url = 'https://steamcommunity.com/id/vangarooo/friends/'

pm = urllib3.PoolManager(
    cert_reqs='CERT_REQUIRED',
    ca_certs=certifi.where()
)
res = pm.request('GET', url)
# print(res.data)
soup = BeautifulSoup(res.data, 'html.parser')

friends_list = list(soup.find_all('a', class_='selectable_overlay'))

for f in friends_list:
    print(f.attrs['href'])
