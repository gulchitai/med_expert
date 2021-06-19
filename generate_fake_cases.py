import collections
from faker import Faker
import pandas as pd

database = []
filename = 'fake_cases'
length = 1000
faker = Faker('ru_RU')

df_s = pd.read_sql_query('select "Код", "НомерПриказа", "ДатаПриказа", "Стадия"  from public."Стандарты"', con=engine)
my_stadiya_list = list(dict.fromkeys(df_s['Стадия'].to_list()))
df_mkb = pd.read_sql_query('select "КодМКБ", "Диагноз"  from public."МКБ"', con=engine)
my_mkb_list = list(dict.fromkeys(df_mkb['КодМКБ'].to_list()))

for x in range(length):
    name = faker.name()
    stadiya = faker.word(ext_word_list=my_stadiya_list).strip()
    mkb = faker.word(ext_word_list=my_mkb_list).strip()
    date_bd = faker.date_of_birth().strftime("%d.%m.%Y")
    database.append(collections.OrderedDict([
        ('Фамилия', name.split()[0]),
        ('Имя', name.split()[1]),
        ('Отчество', name.split()[2]),
        ('ДатаРождения', date_bd),
        ('Стадия', stadiya),
        ('Диагноз', mkb)
    ]))

ddf = pd.DataFrame.from_dict(database)

with open('./docs/%s.json' % filename, 'w', encoding='utf-8') as file:
    ddf.to_json(file, force_ascii=False, orient='records')
print("Done.")