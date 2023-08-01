from pymongo import MongoClient
DATABASE = 'bim'
COLLECTION = 'bim-new'
CLUSTER = 'mongodb+srv://guest_user:75FVbpxQ0iTwArO5@bim.0xndej5.mongodb.net/'

# Only-read user access to Mongo DB:
#  user name: guest_user
#  password: 75FVbpxQ0iTwArO5

class MongoConnection():
    def __init__(self):
        self.cluster = MongoClient(CLUSTER)
        self.db = self.cluster[DATABASE]
        self.connection = self.db[COLLECTION]

    def find_all(self):
        ret = [[], [], []]
        results = self.connection.find({})
        for result in results:
            ret[0].append(result["url"])
            ret[1].append(result["p_id"])
            ret[2].append(result["download_state"]) 
        return ret

if __name__ == '__main__':
    new_con = MongoConnection()
    all_data = new_con.find_all()
    print(len(all_data[0]))