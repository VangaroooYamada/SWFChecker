import urllib3
import certifi
from bs4 import BeautifulSoup


url = 'https://steamcommunity.com/id/vangarooo/'

pm = urllib3.PoolManager(
    cert_reqs='CERT_REQUIRED',
    ca_certs=certifi.where()
)
res = pm.request('GET', url)

# print(res.data)

soup = BeautifulSoup(res.data, 'html.parser')

print(soup.select('#search_results.selectable friend_block_v2 persona in-game'))
