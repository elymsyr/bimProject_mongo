import os
from codecs import open
from re import match
from os import remove
# from os.path import isdir
from datetime import datetime, date
from shutil import rmtree
try:
    from docs.mongo_connection import MongoConnection
except:
    from mongo_connection import MongoConnection

MAIN_DATAS = 'docs/product_data.txt'
# Item scope to write log
LIST_SCOPE = [0,10]
DOWNLOAD_FOLDER = 'C:\\Users\\orhun\\OneDrive\\Belgeler\\Github Repo\\bimObject\\Include\\BimDownloaded'
DOWNLOAD_LOG = 'docs/download_log.txt'

def main_check():
    urls = []
    deleted = 0
    with open(MAIN_DATAS, 'r', "utf-8") as f:
        for url in f.readlines():
            urls.append(url.strip())
    print(f"Total Number : {len(urls)}\n")
    for i in range(19050):
        if not urls[i].startswith('https://bimobject.com/en/'):
            urls.remove(urls[i])
            deleted += 1
            i += 1
            print(f"{i+1} - {urls[i]} - {urls.count(urls[i])}")
        if urls.count(urls[i]) != 1:
            urls.remove(urls[i])
            deleted += 1
            i += 1
            print(f"{i+1} - {urls[i]} - {urls.count(urls[i])}")
    with open(MAIN_DATAS, 'w', "utf-8") as f:
        f.write("")
        f.close()
    print(f"\n Deleted : {deleted}\n")
    with open(MAIN_DATAS, 'a+', "utf-8") as f:
        for url in urls:
            f.write(f"{url}\n")

def check_hunted():
    connection = MongoConnection()
    id_data = (connection.find_all())[1]
    url_data = (connection.find_all())[0]
    pattern = r"[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9][0-9]"
    for row in id_data:
        control = match(pattern, str(row))
        if control == None:
            if id_data.index(row) != 0:
                print(f"ID Error - Index:{row} , {id_data.index(row)}")
    for url in url_data:
        if not url.startswith('https://www.bimobject.com/en/'):
            print(f"URL Error - {url}: {url_data.index(url)}")
    for url in url_data:
        if url_data.count(url) > 1:
            print(f"URL Count Error - {url}: {url_data.count(url)}")
    for id in id_data:
        if id_data.count(id) > 1:
            print(f"ID Count Error - {id} : {id_data.count(id)} --> {id_data.index(id)}")

def keep_log(string):
    with open(DOWNLOAD_LOG, 'a', encoding='utf-8') as f:
        f.write(f"{string}")
        
def fix_state(id, state):
    connection = MongoConnection()
    connection.update_downloads(state, id)
    
def find_a(collection):
    results = collection.connection.find({'download_state': 1})
    res = []
    for row in results:
        res.append(row['p_id'])
    return res    

def get_list():
    del_item = []
    now = datetime.now()
    today = date.today()
    current_time = now.strftime("%H:%M:%S")
    connection = MongoConnection()
    res = find_a(connection)
    state_changed = 0
    mongo = connection.find_all()
    state_data = mongo[2] 
    id_data = mongo[1]     
    downloads = os.listdir(DOWNLOAD_FOLDER)
    for item in downloads:
        if item not in res:
            print(f"{item} was not in db as downloaded.")
            fix_state(item, 1)
            state_changed += 1
    for item in res:
        if item not in downloads:
            fix_state(item, 0)
            state_changed += 1
    zips = 0
    double = 0
    empty = 0
    other = 0
    leng = len(downloads)
    cr = 0
    keep_log(f"\nDownload Log {today} - {current_time}\n")
    for item in downloads:
        directory = f"{DOWNLOAD_FOLDER}\\{item}"
        in_dir = os.listdir(directory)
        for file in in_dir:
            if file.endswith(".zip"):
                zips += 1
            elif file.endswith(".crdownload") or file.endswith(".tmp"):
                remove(f"{directory}\\{file}")
                cr += 1
            else:
                other += len(in_dir)
        in_dir = os.listdir(directory)
        if len(in_dir) > 1:
            keep_log(f"\n - {item} : More than One Item")
            double += (len(in_dir))
        elif len(in_dir) < 1:
            keep_log(f"\n - {item} : Empty Folder")
            empty += 1
            leng -= 1
            fix_state(item, 0)
    keep_log(f"\n - Total Item: {leng}\n - {double} Double\n - {empty} Empty\n - {zips} Zips\n - {other} Other\n - {state_changed} State Changed\n - {cr} Cr Deleted\n")

def lister():
    path = DOWNLOAD_FOLDER
    size = []
    folders = os.listdir(DOWNLOAD_FOLDER)
    for path in folders[LIST_SCOPE[0]:LIST_SCOPE[1]]:
        path = f"{DOWNLOAD_FOLDER}\\{path}"
        fun = lambda x : os.path.isfile(os.path.join(path,x))
        files_list = filter(fun, os.listdir(path))
        size_of_file = [
            (f,os.stat(os.path.join(path, f)).st_size)
            for f in files_list
        ]
        path = path.split('\\')[-1]
        keep_log(f"\n{path} --> ")
        for f,s in size_of_file:
            keep_log("{} : {}MB ".format(f, round(s/(1024*1024),3)))
            size.append(float(round(s/(1024*1024),3)))
    total = 0
    max = 0
    min = 5
    if len(size) > 0:
        for x in range(len(size)):
            total += size[x]
            if max < size[x]:
                max = size[x]
            if min > size[x]:
                min = size[x]
    else:
        min = 0
    keep_log(f"\nAvarage File Size: {total/(len(size)+1)}\nMax File Size: {max}\nMin File Size: {min}\n")

def hard_clear():
    connection = MongoConnection()
    mongo = connection.find_all()
    id_data = mongo[1] 
    downloads = os.listdir(DOWNLOAD_FOLDER)
    keep_log(f"\nTotal Downloaded Folder: {len(downloads)}\n")
    for item in downloads:       
        directory = f"{DOWNLOAD_FOLDER}\\{item}"
        in_dir = os.listdir(directory)
        if len(in_dir) == 1:
            if item in id_data and (not in_dir[0].endswith(".crdownload") or not in_dir[0].endswith(".tmp")):
                fix_state(id_data.index(item), 1)
            else:
                rmtree(directory, ignore_errors=True)
                fix_state(id_data.index(item), 0)
        else:
            rmtree(directory, ignore_errors=True)
            keep_log(f' - {item} deleted.\n')
    keep_log(f"Total Downloaded Folder After Hard Clean: {len(downloads)}\n")

def check_all(state = None):
    keep_log("\n---------------------------------------------------------------------------------\n")
    get_list()
    lister()
    if state == None:
        if int(input('clear?: ')):
            hard_clear()
    else:
        if state:
            hard_clear()
            

if __name__ == '__main__':
    check_hunted()
    check_all()