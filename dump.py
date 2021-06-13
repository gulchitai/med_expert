from datetime import datetime
from pymongo import MongoClient
import pandas as pd
import os

def dump_tables_to_csv():
    path = './dump_med_expert_' + datetime.now().strftime('%m-%d-%Y')
    try:
        os.mkdir(path)
    except OSError:
        print("Creation of the directory %s failed" % path)
    else:
        print("Successfully created the directory %s " % path)

    client = MongoClient('localhost', 27017)
    db = client['med_expert']

    for collection_name in db.list_collection_names():
        df = pd.DataFrame(list(db[collection_name].find({})))
        collection_name = collection_name.replace('/', '=')
        filename = path + '/' + collection_name + '.csv'
        df.to_csv(filename)
        print('Create file ' + filename)

if __name__ == "__main__":
    dump_tables_to_csv()