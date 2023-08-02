from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import argparse
from pandas import DataFrame
from os import system
from datetime import datetime, date
from docs.mongo_connection import MongoConnection
from time import time
from docs.var import MONGO_LOG, UPDATE_LOG, DOWNLOAD_LOG

def convert(seconds):
    seconds = int(seconds)
    seconds = seconds % (24 * 3600)
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
    adder = []
    if hour != 0:
        adder.append(f" {hour} hours,")
    else:
        adder.append("")
    if minutes != 0:
        adder.append(f" {minutes} minutes,")
    else:
        adder.append("")                  
    if seconds != 0:
        adder.append(f" {seconds} seconds")
    else:
        adder.append("")
    return f"{adder[0]}{adder[1]}{adder[2]}"

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
    print("\nEND\n")
    
def clear():
    connection = MongoConnection()
    connection.delete_all()
        
def export():
    with open('docs/exported.csv', 'w', encoding='utf-8') as f:
        f.write('')
    connection = MongoConnection()
    cursor = connection.connection.find({})  
    df =  DataFrame(list(cursor))
    if '_id' in df:
        del df['_id']       
    df.to_csv('docs/exported.csv', index=False)

def start_log(LOG):
    now = datetime.now()
    today = date.today()
    current_time = now.strftime("%H:%M:%S")
    with open(LOG, 'a', encoding='utf-8') as f:
        f.write(f"\nLOG {today} - {current_time}\n")

def finish_log(LOG, string):
    with open(LOG, 'a', encoding='utf-8') as f:
        f.write(f"\n{string}\n")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="crawl helper", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', action='store_true', help='check data compabilities and downloads')
    parser.add_argument('-x', action='store_true', help='run product parser')
    parser.add_argument('-d', action='store_true', help='start downloading')
    parser.add_argument('-l', action='store_true', help='clear database')
    parser.add_argument('-e', action='store_true', help='export database')
    parser.add_argument('-s', action='store_true', help='open search gui')
    parser.add_argument('-u', action='store_true', help='start updating components')
    args = parser.parse_args()
    config = vars(args)
    check_key = config['c']
    hunter_key = config['x']
    download_key = config['d']
    clear_key = config['l']
    export_key = config['e']
    search_key = config['s']
    update_key = config['u']
    if check_key:
        start = time()
        remainder = start
        start = 0
        system('py docs/check_functions.py')
        stop = time()
        stop -= remainder         
        print("Elapsed time during the whole program in seconds:", convert(stop))
        finish_log(DOWNLOAD_LOG, f"Elapsed time during the whole program in seconds:{convert(stop)}")
    elif hunter_key:
        start = time()
        remainder = start
        start = 0
        start_log(MONGO_LOG)
        productParse()
        stop = time()
        stop -= remainder         
        print("Elapsed time during the whole program in seconds:", convert(stop))
        finish_log(MONGO_LOG, f"Elapsed time during the whole program in seconds:{convert(stop)}")
    elif search_key:
        system('py gui.py')  
    elif download_key:
        start = time()
        remainder = start
        start = 0
        system('py docs/download_product.py')
        stop = time()
        stop -= remainder         
        print("Elapsed time during the whole program in seconds:", convert(stop))
        finish_log(DOWNLOAD_LOG, f"Elapsed time during the whole program in seconds:{convert(stop)}")      
    elif clear_key:
        clear()
    elif export_key:
        start = time()
        remainder = start
        start = 0        
        export()
        stop = time()
        stop -= remainder         
        print("Elapsed time during the whole program in seconds:", convert(stop))        
    elif update_key:
        start = time()
        remainder = start
        start = 0
        start_log(UPDATE_LOG)
        system('py docs/update_comp.py')
        stop = time()
        stop -= remainder        
        print("Elapsed time during the whole program in seconds:", convert(stop))
        finish_log(UPDATE_LOG, f"Elapsed time during the whole program in seconds:{convert(stop)}")      