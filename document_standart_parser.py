from bs4 import BeautifulSoup as bs
from pprint import pprint

import re
import os
import zipfile
import shutil
from pymongo import MongoClient

def get_immediate_subdirectories(a_dir):
    return [os.path.join(path, name) for name in os.listdir(a_dir)
            if os.path.isdir(os.path.join(a_dir, name))]

def del_all_subdirectories(path):
    list_catalogs_for_del = get_immediate_subdirectories(path)
    for catalog in list_catalogs_for_del:
        shutil.rmtree(catalog)

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

def first_table_is_valid(table1):
    rows = table1.find_all("tr")
    for i, row in enumerate(rows):
        if i < 2:
            continue
        columns = row.find_all("td")
        if len(columns) < 4:
            return False
        else:
            return True

def second_table_is_valid(table):
    rows = table.find_all("tr")
    for i, row in enumerate(rows):
        if i < 2:
            continue
        columns = row.find_all("td")
        if len(columns) > 4:
            return False
        else:
            return True

def get_standart_table1(filename):

    f = open(filename, 'r', encoding="utf8")
    result = f.read()
    parsed_html = bs(result, 'lxml')
    tables = parsed_html.find_all("table")

    #нужна проверка на первую таблицу
    if first_table_is_valid(tables[0])==False:
        tables.pop(0)
    d = {}
    for k, table in enumerate(tables):
        if k > 2:
            break
        if k == 0:

            rl = []
            num, date = get_number_date(filename)
            d['date'] = date
            d['number'] = num
            #d['table_name'] = table.find_previous_sibling('div').find_previous_sibling('div').get_text()
            d['table_name'] = 'Медицинские мероприятия для диагностики'

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


def get_standart_table2(filename):

    f = open(filename, 'r', encoding="utf8")
    result = f.read()
    parsed_html = bs(result, 'lxml')
    tables = parsed_html.find_all("table")

    #нужна проверка на первую таблицу
    if first_table_is_valid(tables[0])==False:
        tables.pop(0)

    #это все первая таблица
    tables.pop(0)
    tables.pop(0)
    tables.pop(0)

    d = {}

    for k, table in enumerate(tables):
        if second_table_is_valid(table)==False:
            break
        if k == 0:
            rl = []
            num, date = get_number_date(filename)
            d['date'] = date
            d['number'] = num
            #d['table_name'] = table.find_previous_sibling('div').find_previous_sibling('div').get_text()
            d['table_name'] = 'Медицинские услуги для лечения заболевания'

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

def get_standart_table3(filename):

    f = open(filename, 'r', encoding="utf8")
    result = f.read()
    parsed_html = bs(result, 'lxml')
    tables = parsed_html.find_all("table")

    #нужна проверка на первую таблицу
    if first_table_is_valid(tables[0])==False:
        tables.pop(0)

    #это все первая таблица
    tables.pop(0)
    tables.pop(0)
    tables.pop(0)

    #это все вторая таблица
    while len(tables) > 0 and second_table_is_valid(tables[0]):
        tables.pop(0)

    d = {}

    if len(tables) == 0:
        return d
    #третья таблица не разбита - цикл по таблицам не нужен

    rl = []
    num, date = get_number_date(filename)
    d['date'] = date
    d['number'] = num
    #d['table_name'] = table.find_previous_sibling('div').find_previous_sibling('div').get_text()
    d['table_name'] = 'Перечень лекарственных препаратов'

    rows = tables[0].find_all("tr")

    for i, row in enumerate(rows):
        if i == 0:
            continue
        columns = row.find_all("td")
        dc = {}
        for j, col in enumerate(columns):
            if j == 0:
                dc['code'] = ' '.join(col.get_text().split())
            if j == 1:
                dc['class'] = ' '.join(col.get_text().split())
            if j == 2:
                dc['name'] = ' '.join(col.get_text().split())
            if j == 3:
                dc['chast'] = ' '.join(col.get_text().split())
            if j == 4:
                dc['ed_izm'] = ' '.join(col.get_text().split())
            if j == 5:
                dc['ssd'] = ' '.join(col.get_text().split())
            if j == 6:
                dc['skd'] = ' '.join(col.get_text().split())
        rl.append(dc)

    d['rows'] = rl
    return d

def get_standart_header(filename):

    f = open(filename, 'r', encoding="utf8")
    result = f.read()
    parsed_html = bs(result, 'lxml')
    print(parsed_html.find('div', text=re.compile('Возраст')).contents)

if __name__ == "__main__":

    path = ".\docs\Стандарты"

    del_all_subdirectories(path)

    files = os.listdir(path)

    client = MongoClient('localhost', 27017)
    db = client['med_expert']
    db.drop_collection('standart_table1')
    db.drop_collection('standart_table2')
    db.drop_collection('standart_table3')

    for file in files:
        _, file_extension = os.path.splitext(file)
        if file_extension != '.zip':
            continue
        filename = os.path.join(path, file)

        with zipfile.ZipFile(filename, "r") as zip_ref:
            zip_ref.extractall(path)
        filename, _ = os.path.splitext(filename)
        filename += '.htm'

        get_standart_header(filename)
        break

        data = get_standart_table1(filename)
        db['standart_table1'].insert_one(data)

        data = get_standart_table2(filename)
        db['standart_table2'].insert_one(data)

        data = get_standart_table3(filename)
        db['standart_table3'].insert_one(data)

    del_all_subdirectories(path)