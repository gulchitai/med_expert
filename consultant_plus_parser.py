from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys

import requests
from lxml import html
import pandas as pd
from pymongo import MongoClient

#некоммерческая версия консультант плюс
#http://www.consultant.ru/cons/cgi/online.cgi?req=home&utm_csource=online&utm_cmedium=button

def download_document(headless = False, name =''):

    if name == '':
        return
    opt = webdriver.ChromeOptions()
    if headless:
        opt.add_argument("--headless")
    opt.add_argument('--start-maximized')

    driver = webdriver.Chrome(options=opt, executable_path="C:/Users/gulch/PycharmProjects/med_expert/chromedriver.exe")
    driver.get('http://www.consultant.ru/cons/cgi/online.cgi')
    print(driver.title)
    assert "КонсультантПлюс - Стартовая страница" in driver.title

    elem = driver.find_element_by_name('dictFilter')
    elem.send_keys(name)
    time.sleep(1)
    elem.send_keys(Keys.RETURN)
    time.sleep(10)

    #driver.close()

def get_standart_info(headers):

    main_link = "http://www.consultant.ru/document/cons_doc_LAW_141711/03833ffe0d8c546db533a3dd9ba4bb7a7b64aa45/"
    response = requests.get(url=main_link, headers=headers).text
    root = html.fromstring(response)

    links = root.xpath("//contents/ul/li/a/@href")
    return links


if __name__ == "__main__":

    headers = {
        'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36'}

    info = get_standart_info(headers=headers)

    print(info)

    main_link = 'http://www.consultant.ru'
    l = []
    for link in info:
        endpoint = main_link + link
        response = requests.get(url=endpoint, headers=headers).text
        root = html.fromstring(response)
        title = ''
        for i in root.xpath('//tr'):
            t0 = i.xpath("./td[1]/div/h1/div/span/span/text()")
            t1 = i.xpath("./td[1]/div/div/span/text()")
            t2 = i.xpath("./td[2]/div/div/span/text()")
            t3 = i.xpath("./td[3]/div/div/span/text()")
            t4 = i.xpath("./td[4]/div/div/span/text()")
            if len(t0) > 0:
                title = t0[0]

            if (t1 == []) and (t2 == []) and (t3 == []) and (t4 == []):
                continue
            d = {}
            d['title'] = title
            d['name'] = t1[0]
            d['mkb'] = t2
            d['age'] = t3
            d['doc_name'] = t4
            l.append(d)

    print(l)

    client = MongoClient('localhost', 27017)
    db = client['med_expert']
    db.drop_collection('standart')
    db['standart'].insert_many(l)

    #download_document(headless=False, name="Приказ Минздрава России от 20 декабря 2012 г. N 1139н")