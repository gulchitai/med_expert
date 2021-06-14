import requests
#from lxml import html
from bs4 import BeautifulSoup as bs
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
        p = t.find_previous_sibling('p')
        l.append(p.get_text())
    return l

if __name__ == "__main__":

    headers = {
        'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36'}

    print(get_garant_data(headers=headers))
