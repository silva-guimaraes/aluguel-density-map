import requests
import csv
import sys
import json
from bs4 import BeautifulSoup

headers = {
        'authority': 'www.olx.com.br',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,\
image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;\
q=0.9',
        'cache-control': 'no-cache',
        'dnt': '1',
        'pragma': 'no-cache',
        'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", \
"Google Chrome";v="108"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 \
(KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36', }

s = requests.Session()
s.headers.update(headers)


foobar = []

for page in range(1, 24):
    url = 'https://www.olx.com.br/imoveis/aluguel/estado-es/norte-do-espirito-\
santo/vila-velha?o=' + str(page)

    response = s.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    data = soup.find(id='initial-data')['data-json']
    data = json.loads(data)
    data = [i for i in data['listingProps']['adList']
            if 'price' in i and i['price'] is not None]

    for i in data:
        local = s.get(i['url']).content
        soup = BeautifulSoup(local, 'html.parser')
        local = soup.find(id='initial-data')['data-json']
        local = json.loads(local)
        try:
            barfoo = {
                    "cep": local['ad']['locationProperties'][0]['value'],
                    "valor": i['price'][3:],
                    "subject": i['subject'],
                    "url": i['url']
                    }
            print(barfoo)
            foobar.append(barfoo)
        except KeyError:
            print('key error!', file=sys.stderr)


with open("precos.csv", "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["cep", "valor", "subject", "url"])

    for i in foobar:
        writer.writerow([
            i["cep"],
            i["valor"],
            i["subject"],
            i["url"]])
