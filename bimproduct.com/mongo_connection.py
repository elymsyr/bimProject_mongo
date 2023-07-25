from pymongo import MongoClient

class MongoConnection():
    def __init__(self):
        self.cluster = MongoClient("mongodb+srv://admin0:aqwer1234@bim.0xndej5.mongodb.net/")
        self.db = self.cluster["bim"]
        self.connection = self.db["bim"]
        self.selectors = ['p_id', 'download_state', 'name', 'category', 'subcategory', 'url', 'direct_link', 'brand', 'votes', 'rating', 'tech-spec', 'specification', 'description', 'related', 'classification']

    def insert(self, data):
        insert_data = {
            self.selectors[0]: str(data[0]),
            self.selectors[1]: data[1],
            self.selectors[2]: data[2][:50],
            self.selectors[3]: data[3][:40],
            self.selectors[4]: data[4][:40],
            self.selectors[5]: data[5][:210],
            self.selectors[6]: data[6][:210],
            self.selectors[7]: data[7][:40],
            self.selectors[8]: data[8][:30],
            self.selectors[9]: data[9][:30],
            self.selectors[10]: f"{data[10][:200]}",
            self.selectors[11]: f"{data[11][:200]}",
            self.selectors[12]: f"{data[12][:200]}",
            self.selectors[13]: f"{data[13][:200]}",
            self.selectors[14]: f"{data[14][:200]}",
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
        self.connection.delete_many({})

    def update_downloads(self, state, id):
        self.connection.update_one({'p_id':f'{id}'}, {"$set":{'download_state': state}})