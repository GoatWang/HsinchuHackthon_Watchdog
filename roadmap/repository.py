from pymongo import MongoClient
from datetime import datetime
import pandas as pd
class LocationDB():
    def __init__(self):
        conn = MongoClient("mongodb://hsinchu_watchdog:a1234567@ds131900.mlab.com:31900/hsinchu_watchdog")
        db = conn.hsinchu_watchdog
        self.collection = db.roadmap

    def get_datasets(self, rows):
        df = pd.DataFrame(rows)
        categories = list(set(df['category']))
        datasets_dict = {}
        for cat in categories:
            datasets_dict[cat] = list(set(df[df['category'] == cat]['dataset']))
        return datasets_dict

    def transformdata(self, cursor, topn = -1):
        rows = [item for item in cursor]
        df = pd.DataFrame(rows)
        df = df.fillna("無")
        def modify_address(row):
            if len(row['address']) > 35:
                row['address'] = row['address'].split("、")[0]
            row['note'] = row['note'].replace('nan', '無')

            if "網頁" in row['note']:
                url = row['note'].split("網頁:")[1]
                url = url.split("\n")[0]
                if url != '無':
                    new_url = " <a href=\"" + url + "\">連結</a>"
                    row['note'] = row['note'].replace(url, new_url)

            if 'nan' in row['phone']:
                row['phone'] = row['phone'].replace('nan', '')
            return row
        df = df.apply(modify_address, axis=1)
        rows = list(df.T.to_dict().values())[:topn]
        locations = [{'lat':item['latitude'], 'lng':item['longitude']} for item in rows]
        names = [item['name'] for item in rows]
        return rows, locations, names

    def getAll(self):
        cursor = self.collection.find({})
        return self.transformdata(cursor)

    def getFirst(self, searchingDict={}):
        cursor = self.collection.find(searchingDict)
        return self.transformdata(cursor, 1)

    def getLocationsByCat(self, category):
        cursor = self.collection.find({'category':category})
        return self.transformdata(cursor)

    def getLocationsByDataset(self, dataset):
        cursor = self.collection.find({'dataset':dataset})
        return self.transformdata(cursor)

    def gettest(self):
        cursor = self.collection.find({'latitude':{"$ne":None}})
        return self.transformdata(cursor, 50)





if __name__ == "__main__":
    LDB = LocationDB()
    rows, locations, names = LDB.getAll()
    # rows, locations, names = LDB.gettest()
    # locations = LDB.getAll()

    df = pd.DataFrame(rows)
    categories = list(set(df['category']))
    for cat in categories:
        print(cat)
        print(set(df[df['category'] == cat]['dataset']))

    