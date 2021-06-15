from bs4 import BeautifulSoup as bs
from pprint import pprint

import re
from pymongo import MongoClient

def get_standart_data():

    filename = './docs/Приказ Минздрава России от 20.12.2012 N 1095н  Об утверждени.htm'
    f = open(filename, 'r', encoding="utf8")
    result = f.read()
    parsed_html = bs(result, 'lxml')
    tables = parsed_html.find_all("table")

    l = []
    for table in tables:
        d = {}

        rows = table.find_all("tr")
        rl = []
        for i, row in enumerate(rows):
            if i < 2:
                continue
            columns = row.find_all("td")
            dc = {}
            for j, col in enumerate(columns):
                if j == 0:
                    dc['code'] = col.get_text()
                if j == 1:
                    dc['name'] = col.get_text()
                if j == 2:
                    dc['chast'] = col.get_text()
                if j == 3:
                    dc['krat'] = col.get_text()
            rl.append(dc)
        d['table_name'] = table.find_previous_sibling('div').find_previous_sibling('div').get_text()
        d['rows'] = rl
        l.append(d)
    return l

if __name__ == "__main__":

    pprint(get_standart_data())