import collections
from faker import Faker
import pandas as pd
from sqlalchemy import create_engine

def generate_fake_cases(length = 1000):
    database = []
    filename = 'fake_cases'

    faker = Faker('ru_RU')
    engine = create_engine('postgresql://postgres:123@localhost:5432/med_expert')

    df_s = pd.read_sql_query('select "Код", "НомерПриказа", "ДатаПриказа", "Стадия"  from public."Стандарты"', con=engine)
    my_stadiya_list = list(dict.fromkeys(df_s['Стадия'].to_list()))
    df_mkb = pd.read_sql_query('select "КодМКБ", "Диагноз"  from public."МКБ"', con=engine)
    my_mkb_list = list(dict.fromkeys(df_mkb['КодМКБ'].to_list()))
    df_d = pd.read_sql_query('select "КодУслуги", "НаименованиеУслуги", "СредняяЧастота", "СредняяКратность"  from public."Стандарты_Диагностика"', con=engine)
    my_kod_uslugi_td_list = list(dict.fromkeys(df_d['КодУслуги'].to_list()))

    df_l = pd.read_sql_query('select "КодУслуги", "НаименованиеУслуги", "СредняяЧастота", "СредняяКратность"  from public."Стандарты_Лечение"',con=engine)
    my_kod_uslugi_tl_list = list(dict.fromkeys(df_l['КодУслуги'].to_list()))

    df_lek = pd.read_sql_query('select "КодПрепарата", "Классификация", "Наименование", "СредняяЧастота", "ЕдиницаИзмерения", "ССД", "СКД"  from public."Стандарты_Лекарства"',con=engine)
    my_kod_lek_list = list(dict.fromkeys(df_lek['КодПрепарата'].to_list()))

    for x in range(length):
        name = faker.name()
        first_name = name.split()[1]
        last_name = name.split()[0]
        patronymic = name.split()[2]
        stadiya = faker.word(ext_word_list=my_stadiya_list).strip()
        mkb = faker.word(ext_word_list=my_mkb_list).strip()
        date_bd = faker.date_of_birth().strftime("%d.%m.%Y")
        sub_list_d = []
        for j in range(3):
            d = {}
            kod_uslugi = faker.word(ext_word_list=my_kod_uslugi_td_list).strip()
            d['КодУслуги'] = kod_uslugi
            d['НаименованиеУслуги'] = df_d.loc[df_d['КодУслуги'].str.strip() == kod_uslugi, "НаименованиеУслуги"].iloc[0]
            d['СредняяЧастота'] = df_d.loc[df_d['КодУслуги'].str.strip() == kod_uslugi, "СредняяЧастота"].iloc[0]
            d['СредняяКратность'] = df_d.loc[df_d['КодУслуги'].str.strip() == kod_uslugi, "СредняяКратность"].iloc[0]
            sub_list_d.append(d)

        sub_list_l = []
        for j in range(3):
            d = {}
            kod_uslugi = faker.word(ext_word_list=my_kod_uslugi_tl_list).strip()
            d['КодУслуги'] = kod_uslugi
            d['НаименованиеУслуги'] = df_l.loc[df_l['КодУслуги'].str.strip() == kod_uslugi, "НаименованиеУслуги"].iloc[0]
            d['СредняяЧастота'] = df_l.loc[df_l['КодУслуги'].str.strip() == kod_uslugi, "СредняяЧастота"].iloc[0]
            d['СредняяКратность'] = df_l.loc[df_l['КодУслуги'].str.strip() == kod_uslugi, "СредняяКратность"].iloc[0]
            sub_list_l.append(d)

        sub_list_lek = []
        for j in range(3):
            d = {}
            kod_lek = faker.word(ext_word_list=my_kod_lek_list).strip()
            d['КодПрепарата'] = kod_lek
            d['Классификация'] = df_lek.loc[df_lek['КодПрепарата'].str.strip() == kod_lek, "Классификация"].iloc[0]
            d['Наименование'] = df_lek.loc[df_lek['КодПрепарата'].str.strip() == kod_lek, "Наименование"].iloc[0]
            d['СредняяЧастота'] = df_lek.loc[df_lek['КодПрепарата'].str.strip() == kod_lek, "СредняяЧастота"].iloc[0]
            d['ЕдиницаИзмерения'] = df_lek.loc[df_lek['КодПрепарата'].str.strip() == kod_lek, "ЕдиницаИзмерения"].iloc[0]
            d['ССД'] = df_lek.loc[df_lek['КодПрепарата'].str.strip() == kod_lek, "ССД"].iloc[0]
            d['СКД'] = df_lek.loc[df_lek['КодПрепарата'].str.strip() == kod_lek, "СКД"].iloc[0]
            sub_list_lek.append(d)

        database.append(collections.OrderedDict([
            ('Фамилия', last_name),
            ('Имя', first_name),
            ('Отчество', patronymic),
            ('ДатаРождения', date_bd),
            ('Стадия', stadiya),
            ('Диагноз', mkb),
            ('ТаблицаДиагностика',sub_list_d),
            ('ТаблицаЛечения',sub_list_l),
            ('ТаблицаЛекарств',sub_list_lek)]))

        '''
                    ('ТаблицаДиагностика', collections.OrderedDict([
                        ('КодУслуги', kod_uslugi),
                        ('НаименованиеУслуги', name_uslugi),
                        ('СредняяЧастота', avg_chast),
                        ('СредняяКратность', avg_krat)])
                        )
                    '''

    ddf = pd.DataFrame.from_dict(database)

    with open('./docs/%s.json' % filename, 'w', encoding='utf-8') as file:
        ddf.to_json(file, force_ascii=False, orient='records')
    print("Done.")

if __name__ == "__main__":
    generate_fake_cases(length=10)