# //h4[@class='media-heading']

import requests
from lxml import html
import pandas as pd

def get_documents_links():
    main_link = 'https://minzdrav.gov.ru/documents?document_search%5Bcategory_ids%5D%5B%5D=&document_search%5Bissued_by%5D=&document_search%5Bissued_from%5D=&document_search%5Bissued_until%5D=&document_search%5Bkind%5D=+%D0%9F%D1%80%D0%B8%D0%BA%D0%B0%D0%B7&document_search%5Bnumber%5D=&document_search%5Border%5D=date_desc&document_search%5Bq%5D=%D0%9E%D0%B1+%D1%83%D1%82%D0%B2%D0%B5%D1%80%D0%B6%D0%B4%D0%B5%D0%BD%D0%B8%D0%B8+%D1%81%D1%82%D0%B0%D0%BD%D0%B4%D0%B0%D1%80%D1%82%D0%B0+%D1%81%D0%BF%D0%B5%D1%86%D0%B8%D0%B0%D0%BB%D0%B8%D0%B7%D0%B8%D1%80%D0%BE%D0%B2%D0%B0%D0%BD%D0%BD%D0%BE%D0%B9+%D0%BC%D0%B5%D0%B4%D0%B8%D1%86%D0%B8%D0%BD%D1%81%D0%BA%D0%BE%D0%B9+%D0%BF%D0%BE%D0%BC%D0%BE%D1%89%D0%B8+%D0%BF%D1%80%D0%B8+&document_search%5Btitle_only%5D=false&utf8=%E2%9C%93&page='

    links = []
    for start in range(1, 25):
        print(start)
        endpoint = main_link + str(start)
        headers = {
            'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36'}

        response = requests.get(url=endpoint, headers=headers).text
        root = html.fromstring(response)

        links = links + root.xpath("//h4[@class='media-heading']/a/@href")
    return links
# 'https://minzdrav.gov.ru'

if __name__ == "__main__":
    links = get_documents_links()
