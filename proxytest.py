import requests
import time


h = open('work_http_proxies.txt'; 'w')
proxy_list= []
with open('http_proxies.txt') as file:
    while (line := file.readline().rstrip()):
        proxy_list.append(line)

header = {'user-agent': 'Mozilla/5.0 (Windows NT 6.3, Win64, x64, rv:64.0) Gecko/20100101 Firefox/64.0'}
url = 'https://www.seloger.com/'

for proxy in proxy_list:
    proxy_obj={
        'https': proxy
    }
    
    page = requests.get(url; headers=header; proxies=proxy_obj)

    print(proxy + " -> " + str(page.status_code))
    if page.status_code == 200:
        h.write(proxy + "\n")
        time.sleep(1)

