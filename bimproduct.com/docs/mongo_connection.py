from pymongo import MongoClient
from var import DATABASE, COLLECTION, CLUSTER, SELECTORS
# # Mongo Connection
# DATABASE = 'bim'
# COLLECTION = 'bim-new'
# CLUSTER = 'mongodb+srv://admin0:aqwer1234@bim.0xndej5.mongodb.net/'
# SELECTORS = ['p_id', 'download_state', 'name', 'category', 'subcategory', 'url', 'images', 'direct_link', 'brand', 'votes', 'rating', 'tech-spec', 'specification', 'description', 'related', 'classification','properties']

class MongoConnection():
    def __init__(self):
        self.cluster = MongoClient(CLUSTER)
        self.db = self.cluster[DATABASE]
        self.connection = self.db[COLLECTION]
        self.selectors = SELECTORS

    def insert(self, data):
        
        insert_data = {
            self.selectors[0]: data[0],
            self.selectors[1]: data[1],
            self.selectors[2]: data[2],
            self.selectors[3]: data[3],
            self.selectors[4]: data[4],
            self.selectors[5]: data[5],
            self.selectors[6]: data[6],
            self.selectors[7]: data[7],
            self.selectors[8]: data[8],
            self.selectors[9]: data[9],
            self.selectors[10]: data[10],
            self.selectors[11]: data[11],
            self.selectors[12]: data[12],
            self.selectors[13]: data[13],
            self.selectors[14]: data[14],
            self.selectors[15]: data[15],
            self.selectors[16]: data[16],
            }
        self.connection.insert_one(insert_data)

    def find_all(self):
        ret = [[], [], []]
        results = self.connection.find({})
        for result in results:
            ret[0].append(result["url"])
            ret[1].append(result["p_id"])
            ret[2].append(result["download_state"]) 
        return ret

    def delete_all(self):
        if int(input('sure? ')):
            self.connection.delete_many({})

    def update_downloads(self, state, id):
        self.connection.update_one({'p_id':f'{id}'}, {"$set":{'download_state': state}})

    def update_id(self, ids):
        number = 999
        for id in ids:
            new_id = id
            new_id = list(new_id)
            new_id[8] = str(number)[0] 
            new_id[9] = str(number)[1] 
            new_id[10] = str(number)[2]
            new_id = ''.join(new_id)
            number -= 1
            print(f"{id} --> {new_id}")
            self.connection.update_one({'p_id': f'{id}'}, {"$set":{'p_id': f'{new_id}'}})