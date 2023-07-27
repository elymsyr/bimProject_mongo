from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import argparse
from docs.check_functions import check_hunted
from pandas import DataFrame
from os import system
from docs.mongo_connection import MongoConnection

MAIN_DATAS = 'docs/product_data.txt'
LIST_SCOPE = [0,10]
DOWNLOAD_FOLDER = 'C:\\Users\\orhun\\OneDrive\\Belgeler\\Github Repo\\bimObject\\Include\\BimDownloaded'
DOWNLOAD_LOG = 'docs/download_log.txt'

# def urlExtract():
#     process = CrawlerProcess(get_project_settings())
#     process.crawl('urlExtract')
#     process.start()
#     process.join()
def productParse():
    process = CrawlerProcess(get_project_settings())
    process.crawl('productParse')
    process.start()
    process.join()
    
def clear():
    connection = MongoConnection()
    connection.delete_all()
        
def export():
    with open('exported.csv', 'w', encoding='utf-8') as f:
        f.write('')
    connection = MongoConnection()
    cursor = connection.connection.find({})  
    df =  DataFrame(list(cursor))
    if '_id' in df:
        del df['_id']       
    df.to_csv('docs/exported.csv', index=False)
 

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="crawl helper", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', action='store_true', help='check data compabilities')
    parser.add_argument('-x', action='store_true', help='run product parser')
    parser.add_argument('-d', action='store_true', help='start downloading')
    parser.add_argument('-l', action='store_true', help='clear database')
    parser.add_argument('-e', action='store_true', help='export database')
    args = parser.parse_args()
    config = vars(args)
    check_key = config['c']
    hunter_key = config['x']
    download_key = config['d']
    clear_key = config['l']
    export_key = config['e']
    if check_key:
        check_hunted()
    elif hunter_key:
        productParse()
    elif download_key:
        system('py download_product.py')    
    elif clear_key:
        clear()
    elif export_key:
        export()