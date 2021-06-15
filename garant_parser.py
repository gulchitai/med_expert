import requests
from bs4 import BeautifulSoup as bs

import re
from pymongo import MongoClient

#//table[@class='primeTab']

def get_garant_data(headers):
    main_link = 'https://www.garant.ru/products/ipo/prime/doc/71575880/'
    reg = requests.get(main_link, headers=headers)
    html = reg.text
    parsed_html = bs(html, 'lxml')
    tables = parsed_html.find_all(attrs={'class': 'primeTab'})

    l = []
    for t in tables:
        d = {}
        p = t.find_previous_sibling('p')
        d['p'] = p.get_text()
        rows = t.find_all('tr')
        l2 = []
        for i, r in enumerate(rows):
            if i == 0:
                continue
            deleted_symbols = r'[\r\n]'
            text = r.get_text()
            text = re.sub(deleted_symbols, '', text)
            text = text.replace('Да/Нет','')
            l2.append(text)
        d['tr'] = l2
        l.append(d)

    client = MongoClient('localhost', 27017)
    db = client['med_expert']
    db.drop_collection('prikaz203n')
    db['prikaz203n'].insert_many(l)
    #return l[1]

if __name__ == "__main__":

    headers = {
        'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36'}

    get_garant_data(headers=headers)
