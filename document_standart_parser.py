from bs4 import BeautifulSoup as bs
from pprint import pprint

import re
from pymongo import MongoClient

def get_number_date(filename):
    match = re.search(r'(\d+.\d+.\d+)', filename)
    date = match.group(1)
    lst = filename.split(sep=" ")
    flag = False
    num = ''
    for s in lst:
        if s == 'N':
            flag = True
            continue
        if flag:
            num = s
            break
    return num, date

def get_standart_table1():

    filename = './docs/Приказ Минздрава России от 20.12.2012 N 1095н  Об утверждени.htm'

    f = open(filename, 'r', encoding="utf8")
    result = f.read()
    parsed_html = bs(result, 'lxml')
    tables = parsed_html.find_all("table")

    for k, table in enumerate(tables):
        if k > 2:
            break
        if k == 0:
            d = {}
            rl = []
            num, date = get_number_date(filename)
            d['date'] = date
            d['number'] = num
            d['table_name'] = table.find_previous_sibling('div').find_previous_sibling('div').get_text()

        rows = table.find_all("tr")

        for i, row in enumerate(rows):
            if i < 2:
                continue
            columns = row.find_all("td")
            dc = {}
            for j, col in enumerate(columns):
                if j == 0:
                    dc['code'] = ' '.join(col.get_text().split())
                if j == 1:
                    dc['name'] = ' '.join(col.get_text().split())
                if j == 2:
                    dc['chast'] = ' '.join(col.get_text().split())
                if j == 3:
                    dc['krat'] = ' '.join(col.get_text().split())
            rl.append(dc)
        if k == 2:
            d['rows'] = rl
    return d



if __name__ == "__main__":

    path = ".\docs\Стандарты"

    client = MongoClient('localhost', 27017)
    db = client['med_expert']
    db.drop_collection('standart_table1')

    data = get_standart_table1()
    db['standart_table1'].insert_one(data)