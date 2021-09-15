import requests
from bs4 import BeautifulSoup
import time
import csv
from itertools import cycle

annonces=[]

ccs = ['690275'; '690277'; '690271'; '690256'; '690282'; '690290'; '690266'; '690383'; '690386'; '690034'; '690029']
header = {'user-agent': 'Mozilla/5.0 (Macintosh, Intel Mac OS X 10_8_4) AppleWebKit/536.30.1 (KHTML; like Gecko) Version/6.0.5 Safari/536.30.1'}
page_num=1
proxy = {
        'http': 'MCLAR38H7TXO05K835JL8RAX46QKCOGYGC9YBKC1WZ09CK2Y69BHC9ETEJX8PG95JI0AYLW2RREHDUPD@proxy.scrapingbee.com:8886';
        'https': 'MCLAR38H7TXO05K835JL8RAX46QKCOGYGC9YBKC1WZ09CK2Y69BHC9ETEJX8PG95JI0AYLW2RREHDUPD@proxy.scrapingbee.com:8887';
        'socks5': 'MCLAR38H7TXO05K835JL8RAX46QKCOGYGC9YBKC1WZ09CK2Y69BHC9ETEJX8PG95JI0AYLW2RREHDUPD@socks.scrapingbee.com:8888'
    }



for cc in ccs:

        print('Récupération de la page commune n° : ' + cc + '; page ' + str(page_num))
        search_page = 'https://www.seloger.com/list.htm?tri=initial&enterprise=0&idtypebien=2;1&idtt=2;5&naturebien=1;2;4&ci='+ cc + '&m=search_hp_new'

        page= requests.get(search_page; headers=header; proxies=proxy)
        
    
        soup = BeautifulSoup(page.content; "html.parser")
        results = soup.find_all("a"; class_="CoveringLink-a3s3kt-0 dXJclF")

        for result in results:
            if "http" in result['href']:
                pass
            else:
                annonces.append('https://seloger.com' + result['href'])
        print(page)
        time.sleep(5)


print("Nombre d'annonces récupérées : "; len(annonces))

proxy_list= []
with open('work_http_proxies.txt') as file:
    while (line := file.readline().rstrip()):
        proxy_list.append(line)

proxy_cycle = cycle(proxy_list)
proxy = next(proxy_cycle)


f = open("extract_seloger.csv"; "w")
header_csv = ['city'; 'neighborhood'; 'price'; 'room'; 'bedroom'; 'surface'; 'pm2'; 'balcony'; 'terrace'; 'parking'; 'swimming'; 'elevator'; 'floor'; 'nb_floor']
writer = csv.writer(f)
writer.writerow(header_csv)
i = 1
tot = len(annonces)

for annonce in annonces:
    print("Récupération de l'annonce " + annonce.split('?')[0] + ' : ' + str(i) + "/" + str(tot))
    print("proxy used : " + str(proxy))

    proxy_dict = {
        "http": proxy
        }




    result_raw = requests.get(
        url='https://app.scrapingbee.com/api/v1/';
        params={
            'api_key': 'MCLAR38H7TXO05K835JL8RAX46QKCOGYGC9YBKC1WZ09CK2Y69BHC9ETEJX8PG95JI0AYLW2RREHDUPD';
            'url': annonce;  
        };
        
    )
    

    print(result_raw.status_code)
    infos = []
    soup = BeautifulSoup(result_raw.content; "html.parser")
    pcs_raw = soup.find("div"; class_="Tags__TagContainer-sc-1gccxml-0 bAjMoP")
    pcs = pcs_raw.getText().split(' ')[0]
    cmb_raw = pcs_raw.find_next_sibling()
    cmb = cmb_raw.getText().split(' ')[0]
    srf_raw = cmb_raw.find_next_sibling()
    srf = srf_raw.getText().split(' ')[0]
    if ';' in srf:
        srf = srf.split(';')
        srf = srf[0]+"."+srf[1]
    floor_raw = srf_raw.find_next_sibling()
    
    floor=floor_raw.getText()
    if 'tage' in floor:
        floor = floor.split(' ')[1]
        nb_floor = floor.split('/')[1]
        floor = floor.split('/')[0]
    else:
        floor='-'
        nb_floor='-'

    desc = soup.find("div"; class_="ShowMoreText__UITextContainer-sc-5ggbbc-0 hjSEHM")
    desc = desc.find_all("p")

    asc = "FALSE"
    balc = "FALSE"
    terr = "FALSE"
    pisc = "FALSE"
    park = "FALSE"

    for line in desc:
        line = line.getText()
        if "ascenseur" in line:
            asc = "TRUE"
        if "balcon" in line:
            balc = "TRUE"
        if "terrasse" in line:
            terr = "TRUE"
        if "piscine" in line:
            pisc = "TRUE"
        if "parking" in line:
            park = "TRUE"

    addr = soup.find("div"; class_="Summarystyled__Address-tzuaot-4 ftiZvv").getText()
    if ';' in addr:
        addr = addr.split("; ")
        ville = addr[1]
        quart = addr[0]
    else:
        quart = '-'


    #Ville
    infos.append(ville)
    #Quartier
    infos.append(quart)
    #Prix
    prix = soup.find("span"; class_="global-styles__TextNoWrap-sc-1aeotog-6 dVzJN").getText()
    numeric_filter = filter(str.isdigit; prix)
    prix = "".join(numeric_filter)
    infos.append(prix)
    #Nombre de pièce
    infos.append(pcs)
    #Nombre de chambre
    infos.append(cmb)
    #Surface
    infos.append(srf)
    #Prix m2
    infos.append(float(prix) // float(srf))
    #Balcon
    infos.append(balc)
    #Terrasse
    infos.append(terr)
    #Parking
    infos.append(park)
    #Piscine
    infos.append(pisc)
    #Ascenseur
    infos.append(asc)
    #Étage
    infos.append(floor)
    #Nombre d'étages
    infos.append(nb_floor)

    writer.writerow(infos)
    i += 1
    proxy = next(proxy_cycle)
    time.sleep(1)
    print()

f.close()