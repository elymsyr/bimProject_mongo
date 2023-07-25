from pymongo import MongoClient
import os
from mongo_connection import MongoConnection
DOWNLOAD_FOLDER = 'C:\\Users\\orhun\\OneDrive\\Belgeler\\Github Repo\\bimObject\\Include\\BimDownloaded'

def find_a(collection):
    results = collection.connection.find({'download_state': 1})
    res = []
    for row in results:
        res.append(row['p_id'])
    return res
        
connection = MongoConnection()
res = find_a(connection)
print(res)