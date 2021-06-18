from pymongo import MongoClient
import pandas as pd
from sqlalchemy import create_engine
import re

def get_number_date(prikaz):
    match = re.search(r'(\d+.\d+.\d+)', prikaz)
    date = match.group(1)
    lst = prikaz.split(sep=" ")
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

def get_name_kriteriy(s):
    s = s[:s.find('(')]
    s = s[s.find(' ')+1:]
    return s

def create_tables():

    client = MongoClient('localhost', 27017)
    db = client['med_expert']
    engine = create_engine('postgresql://postgres:123@localhost:5432/med_expert')

    # ******************************* МКБ ********************************************************************
    df = pd.read_excel('./docs/хакатон_2021_коды МКБ.xlsx', index_col=0, header=0, names=['КодМКБ', 'Диагноз'])
    df.to_sql('МКБ', engine)
    print("Создана таблица МКБ")

    # ******************************* Стандарты **************************************************************
    df = pd.DataFrame(list(db["standart_header"].find({})))
    df['date'] = pd.to_datetime(df['date'])
    df = df.rename(columns={'date': 'ДатаПриказа', 'number': 'НомерПриказа', 'faza': 'Фаза', 'stadiya': 'Стадия', \
                            'oslozneniya': 'Осложнения', 'sroki': 'Сроки'})

    #Стандарты.Сроки
    df.loc[df['Сроки'].str.strip() == '', ['Сроки']] = '0'
    df.loc[df['Сроки'].str.strip() == 'Средние сроки лечения (количество дней) 14', ['Сроки']] = '14'
    df['Сроки'] = df['Сроки'].astype(int)

    #Стандарты.возраст
    df['Взрослые'] = (df['vozrast'].str.strip() == 'взрослые') | (df['vozrast'].str.strip() == 'взрослые, дети') | (
                df['vozrast'].str.strip() == 'взрослые Пол пациента: любой')
    df['Дети'] = (df['vozrast'].str.strip() == 'дети') | (df['vozrast'].str.strip() == 'несовершеннолетние') | (
                df['vozrast'].str.strip() == 'взрослые, дети')

    #Стандарты.пол
    df['Женский'] = (df['pol'].str.strip() == 'женский') | (df['pol'].str.strip() == 'женщины') | (
                df['pol'].str.strip() == 'любой') | (df['pol'].str.strip() == 'все')
    df['Мужской'] = (df['pol'].str.strip() == 'мужской') | (df['pol'].str.strip() == 'любой') | (
                df['pol'].str.strip() == 'все')

    #Стандарты.ВидМедПомощи
    df['СпециализированнаяМедПомощь'] = (df['vid'].str.strip() == 'специализированная медицинская помощь') \
                                        | (df['vid'].str.strip() == 'специализированная медицинская помощь, первичная медико-санитарная помощь') \
                                        | (df['vid'].str.strip() == 'специализированная') \
                                        | (df['vid'].str.strip() == 'специализированная медицинская помощь, первичная медико-санитарная помощь, скорая медицинская помощь') \
                                        | (df['vid'].str.strip() == 'специализированная, в том числе высокотехнологичная, медицинская помощь')
    df['ПервичнаяМедПомощь'] = (df['vid'].str.strip() == 'первичная медико-санитарная медицинская помощь') \
                               | (df['vid'].str.strip() == 'специализированная медицинская помощь, первичная медико-санитарная помощь') \
                               | (df['vid'].str.strip() == 'специализированная медицинская помощь, первичная медико-санитарная помощь, скорая медицинская помощь')
    df['СкораяМедПомощь'] = (df['vid'].str.strip() == 'специализированная медицинская помощь, первичная медико-санитарная помощь, скорая медицинская помощь')
    df['ВысокотехнологичнаяМедПомощь'] = (df['vid'].str.strip() == 'специализированная, в том числе высокотехнологичная, медицинская помощь')

    #Стандарты.Условия
    df['Стационарно'] = (df['usloviya'].str.strip() == 'стационарно') \
                        | (df['usloviya'].str.strip() == 'стационарно, в дневном стационаре, амбулаторно') \
                        | (df['usloviya'].str.strip() == 'стационарно, в дневном стационаре') \
                        | (df['usloviya'].str.strip() == 'стационарно; дневной стационар') \
                        | (df['usloviya'].str.strip() == 'стационарно, амбулаторно') \
                        | (df['usloviya'].str.strip() == 'в дневном стационаре, стационарно') \
                        | (df['usloviya'].str.strip() == 'в дневном стационаре; стационарно') \
                        | (df['usloviya'].str.strip() == 'стационарно, амбулаторно, вне медицинской организации') \
                        | (df['usloviya'].str.strip() == 'стационарно, в дневном стационаре, амбулаторно, вне медицинской организации') \
                        | (df['usloviya'].str.strip() == 'стационарная') \
                        | (df['usloviya'].str.strip() == 'стационарно/дневной стационар')

    df['ДневнойСтационар'] = (df['usloviya'].str.strip() == 'стационарно, в дневном стационаре, амбулаторно') \
                             | (df['usloviya'].str.strip() == 'стационарно, в дневном стационаре') \
                             | (df['usloviya'].str.strip() == 'дневной стационар ') \
                             | (df['usloviya'].str.strip() == 'в дневном стационаре') \
                             | (df['usloviya'].str.strip() == 'стационарно; дневной стационар') \
                             | (df['usloviya'].str.strip() == 'в дневном стационаре, стационарно') \
                             | (df['usloviya'].str.strip() == 'в дневном стационаре; стационарно') \
                             | (df['usloviya'].str.strip() == 'стационарно, в дневном стационаре, амбулаторно, вне медицинской организации') \
                             | (df['usloviya'].str.strip() == 'стационарно/дневной стационар') \
                             | (df['usloviya'].str.strip() == 'амбулаторно; в дневном стационаре')

    df['Амбулаторно'] = (df['usloviya'].str.strip() == 'стационарно, в дневном стационаре, амбулаторно') \
                        | (df['usloviya'].str.strip() == 'стационарно, в дневном стационаре, амбулаторно, вне медицинской организации') \
                        | (df['usloviya'].str.strip() == 'амбулаторно; в дневном стационаре') \
                        | (df['usloviya'].str.strip() == 'стационарно, амбулаторно') \
                        | (df['usloviya'].str.strip() == 'стационарно, амбулаторно, вне медицинской организации') \
                        | (df['usloviya'].str.strip() == 'амбулаторно')

    df['ВнеМедицинскойОрганизации'] = (df['usloviya'].str.strip() == 'стационарно, амбулаторно, вне медицинской организации') \
                                      | (df['usloviya'].str.strip() == 'стационарно, в дневном стационаре, амбулаторно, вне медицинской организации')

    #Стандарты.Форма
    df['Плановая'] = (df['forma'].str.strip() == 'плановая') \
                     | (df['forma'].str.strip() == 'плановая, неотложная') \
                     | (df['forma'].str.strip() == 'плановая, экстренная') \
                     | (df['forma'].str.strip() == 'экстренная, неотложная, плановая') \
                     | (df['forma'].str.strip() == 'плановая; неотложная ') \
                     | (df['forma'].str.strip() == 'неотложная; плановая') \
                     | (df['forma'].str.strip() == 'плановая, неотложная, экстренная') \
                     | (df['forma'].str.strip() == 'экстренная, плановая') \
                     | (df['forma'].str.strip() == 'неотложная, плановая') \
                     | (df['forma'].str.strip() == 'экстренная; плановая') \
                     | (df['forma'].str.strip() == 'плановая; экстренная') \
                     | (df['forma'].str.strip() == 'плановая медицинская помощь') \
                     | (df['forma'].str.strip() == 'плановая и неотложная')

    df['Неотложная'] = (df['forma'].str.strip() == 'плановая, неотложная') \
                       | (df['forma'].str.strip() == 'экстренная, неотложная, плановая') \
                       | (df['forma'].str.strip() == 'плановая; неотложная ') \
                       | (df['forma'].str.strip() == 'неотложная; плановая') \
                       | (df['forma'].str.strip() == 'плановая, неотложная, экстренная') \
                       | (df['forma'].str.strip() == 'неотложная, плановая') \
                       | (df['forma'].str.strip() == 'плановая и неотложная') \
                       | (df['forma'].str.strip() == 'неотложная') \
                       | (df['forma'].str.strip() == 'неотложная, экстренная') \
                       | (df['forma'].str.strip() == 'экстренная и неотложная')

    df['Экстренная'] = (df['forma'].str.strip() == 'экстренная') \
                       | (df['forma'].str.strip() == 'экстренная, неотложная, плановая') \
                       | (df['forma'].str.strip() == 'плановая, экстренная') \
                       | (df['forma'].str.strip() == 'плановая, неотложная, экстренная') \
                       | (df['forma'].str.strip() == 'экстренная и неотложная') \
                       | (df['forma'].str.strip() == 'экстренная; плановая')

    df.drop(['_id', 'pol', 'vozrast', 'vid', 'usloviya', 'forma'], axis='columns', inplace=True)

    columns_type_bool = df.select_dtypes(include=['bool']).columns.to_list()

    for column in columns_type_bool:
        df[column] = df[column].astype(int)

    df['Код'] = df.index
    df.set_index('Код', drop=True, inplace=True)

    df.to_sql('Стандарты', engine)
    print("Создана таблица Стандарты")

    # ********************************* Стандарты-МКБ ****************************************
    df = pd.DataFrame(list(db["standart"].find({})))

    l = []
    for i, row in df.iterrows():
        lst_mkb = row['mkb']
        for s in lst_mkb:
            d = {}
            d['Заголовок'] = row['title']
            d['НаименованиеСтандарта'] = row['name']
            if len(row['doc_name']) > 0:
                d['НомерПриказа'], d['ДатаПриказа'] = get_number_date(row['doc_name'][0])
            sp = s.split(sep=' ')
            mkb = sp[0]
            if mkb == 'N':
                mkb += sp[1]
            if mkb == '':
                continue
            d['КодМКБ'] = mkb
            l.append(d)
    df = pd.DataFrame(l)

    df_s = pd.read_sql_query('select "Код", "НомерПриказа", "ДатаПриказа"  from public."Стандарты"', con=engine)
    df_s['ДатаПриказа'] = pd.to_datetime(df_s['ДатаПриказа'])
    df['ДатаПриказа'] = pd.to_datetime(df['ДатаПриказа'])
    df = pd.merge(df, df_s, on=['НомерПриказа', 'ДатаПриказа'], how='inner')
    df = df.rename(columns={'Код': 'КодСтандарта'})
    df = df[['КодСтандарта', 'КодМКБ', 'НаименованиеСтандарта', 'Заголовок']]
    df.set_index(['КодСтандарта', 'КодМКБ'], drop=True, inplace=True)
    df.to_sql('Стандарты_МКБ', engine)
    print("Создана таблица Стандарты_МКБ")

    # ****************************** КритерииКачества *****************************************
    df = pd.DataFrame(list(db["prikaz203n"].find({})))
    df['Наименование'] = df['p'].apply(get_name_kriteriy)
    df = df.rename(columns={'tr': 'ЧекЛист'})
    df['Код'] = df.index
    df.set_index('Код', drop=True, inplace=True)
    df = df[['Наименование', 'ЧекЛист']]
    df.to_sql('КритерииКачества', engine)
    print("Создана таблица КритерииКачества")

if __name__ == "__main__":
    create_tables()