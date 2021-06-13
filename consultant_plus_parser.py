from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys

import requests
from lxml import html
import pandas as pd
from pymongo import MongoClient

#некоммерческая версия консультант плюс
#http://www.consultant.ru/cons/cgi/online.cgi?req=home&utm_csource=online&utm_cmedium=button

def download_documents(headers, headless = False):

    client = MongoClient('localhost', 27017)
    db = client['med_expert']

    df = pd.DataFrame(list(db['standart'].find({})))
    prikazi = df['doc_name'].to_list()

    db.drop_collection('standart_documents')

    opt = webdriver.ChromeOptions()
    if headless:
        opt.add_argument("--headless")
    opt.add_argument('--start-maximized')

    driver = webdriver.Chrome(options=opt, executable_path="C:/Users/gulch/PycharmProjects/med_expert/chromedriver.exe")

    for prikaz in prikazi:
        print(prikaz)
        driver.get('http://www.consultant.ru/cons/cgi/online.cgi')
        assert "КонсультантПлюс - Стартовая страница" in driver.title

        elem = driver.find_element_by_name('dictFilter')
        elem.send_keys(prikaz)
        time.sleep(1)
        elem.send_keys(Keys.RETURN)
        time.sleep(2)
        elem = driver.find_element_by_partial_link_text("Об утверждении")
        doc_link = elem.get_property('href')
        print(doc_link)
        driver.get(doc_link)
        time.sleep(2)
        elem = driver.find_element_by_xpath("//button[@class='dots']").click()
        time.sleep(1)
        elem = driver.find_element_by_class_name('contextMenuItem').click()
        time.sleep(1)
        elem = driver.find_elements_by_class_name('table')
        #print(elem)
        bs = elem[1].find_elements_by_class_name('contextMenuItem')
        #print(len(bs))
        bs[6].click()
        time.sleep(1)
        d = {}
        d['name'] = prikaz
        d['link'] = doc_link
        db['standart_documents'].insert_one(d)

    driver.close()


def get_standart_info(headers):

    main_link = "http://www.consultant.ru/document/cons_doc_LAW_141711/03833ffe0d8c546db533a3dd9ba4bb7a7b64aa45/"
    response = requests.get(url=main_link, headers=headers).text
    root = html.fromstring(response)

    links = root.xpath("//contents/ul/li/a/@href")

    main_link = 'http://www.consultant.ru'
    l = []
    for link in links:
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

    return

#клинические рекомендации
def get_clinic_reg_info(headers):
    main_link = "http://www.consultant.ru/document/cons_doc_LAW_141711/529d8da5a3fd5a6e7bac9da26bc0f1ce1c48b77a/"
    response = requests.get(url=main_link, headers=headers).text
    root = html.fromstring(response)

    links = root.xpath("//contents/ul/li/a/@href")

    main_link = 'http://www.consultant.ru'
    l = []
    for link in links:
        endpoint = main_link + link
        response = requests.get(url=endpoint, headers=headers).text
        root = html.fromstring(response)
        title = ''
        for i in root.xpath('//tr'):
            t0 = i.xpath("./td[1]/div/h1/div/span/span/text()")
            t1 = i.xpath("./td[1]/div/div/span/text()")
            t2 = i.xpath("./td[2]/div/div/span/text()")
            t3 = i.xpath("./td[3]/div/div/span/text()")
            #t4 = i.xpath("./td[4]/div/div/span/text()")
            if len(t0) > 0:
                title = t0[0]

            if (t1 == []) and (t2 == []) and (t3 == []):
                continue
            d = {}
            d['title'] = title
            d['name'] = t1
            d['mkb'] = t2
            d['col'] = t3
            #d['doc_name'] = t4
            l.append(d)

    print(l)

    client = MongoClient('localhost', 27017)
    db = client['med_expert']
    db.drop_collection('clinic_reg')
    db['clinic_reg'].insert_many(l)

    return

def download_clinic_reg(headless = False):

    client = MongoClient('localhost', 27017)
    db = client['med_expert']

    df = pd.DataFrame(list(db['clinic_reg'].find({})))
    clinics = df['name'].to_list()

    db.drop_collection('clinic_reg_documents')

    opt = webdriver.ChromeOptions()
    if headless:
        opt.add_argument("--headless")
    opt.add_argument('--start-maximized')

    driver = webdriver.Chrome(options=opt, executable_path="C:/Users/gulch/PycharmProjects/med_expert/chromedriver.exe")

    for clinic in clinics:
        print(clinic)
        driver.get('http://www.consultant.ru/cons/cgi/online.cgi')
        assert "КонсультантПлюс - Стартовая страница" in driver.title

        elem = driver.find_element_by_name('dictFilter')
        clinic[0] = clinic[0] + 'рекомендации'
        search_string = " ".join(clinic)
        search_string = search_string.replace('(ХВГС)','')
        search_string = search_string.replace('Меркеля', '')
        search_string = search_string.replace('Юинга', '')
        search_string = search_string.replace('Беркитта', '')
        search_string = search_string.replace('Сезари', '')

        elem.send_keys(search_string)
        time.sleep(1)
        elem.send_keys(Keys.RETURN)
        time.sleep(2)
        elem = driver.find_element_by_partial_link_text("Клинические")
        doc_link = elem.get_property('href')
        print(doc_link)
        driver.get(doc_link)
        time.sleep(2)
        elem = driver.find_element_by_xpath("//button[@class='dots']").click()
        time.sleep(1)
        elem = driver.find_element_by_class_name('contextMenuItem').click()
        time.sleep(1)
        elem = driver.find_elements_by_class_name('table')
        #print(elem)
        bs = elem[1].find_elements_by_class_name('contextMenuItem')
        #print(len(bs))
        bs[6].click()
        time.sleep(1)
        d = {}
        d['name'] = search_string
        d['link'] = doc_link
        db['clinic_reg_documents'].insert_one(d)

    driver.close()



if __name__ == "__main__":

    headers = {
        'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36'}

    #get_standart_info(headers=headers)

    #download_documents(headers=headers, headless=False)

    #get_clinic_reg_info(headers=headers)

    download_clinic_reg(headless=False)