import os
from codecs import open
from re import match
from os import remove
from shutil import rmtree
from os.path import exists
# from os.path import isdir
from datetime import datetime, date
from shutil import rmtree
try:
    from docs.mongo_connection import MongoConnection
except:
    from mongo_connection import MongoConnection
try:
    from var import MAIN_DATAS, LIST_SCOPE, DOWNLOAD_FOLDER, DOWNLOAD_LOG
except:
    from docs.var import MAIN_DATAS, LIST_SCOPE, DOWNLOAD_FOLDER, DOWNLOAD_LOG

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
            
def correct_id(ids):
    connection = MongoConnection()
    connection.update_id(ids)

def check_hunted():
    print(" - check_hunted:")
    print("Getting data...")
    id_error = []
    connection = MongoConnection()
    data = connection.find_all()
    id_data = data[1]
    url_data = data[0]
    pattern = r"[0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]"
    print("Checking...")
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
            if id not in id_error:
                id_error.append(id)
    correct_id(id_error)

def keep_log(string):
    with open(DOWNLOAD_LOG, 'a', encoding='utf-8') as f:
        f.write(f"{string}") 

def get_list():
    print(" - get_list:")
    now = datetime.now()
    today = date.today()
    current_time = now.strftime("%H:%M:%S")
    downloads = os.listdir(DOWNLOAD_FOLDER)
    zips = 0
    double = 0
    empty = 0
    other = 0
    leng = len(downloads)
    cr = 0
    double_f = []
    empty_f = []
    keep_log(f"\nDownload Log {today} - {current_time}\n")
    print("Checking... ( See Log --> download_log.txt )")
    for item in downloads:
        directory = f"{DOWNLOAD_FOLDER}\\{item}"
        in_dir = os.listdir(directory)
        for file in in_dir:
            if file.endswith(".zip"):
                zips += 1
            elif file.endswith(".crdownload"):
                remove(f"{directory}\\{file}")
                cr += 1
            else:
                other += len(in_dir)
        in_dir = os.listdir(directory)
        if len(in_dir) > 1:
            double_f.append(item)
            double += (len(in_dir))
            rmtree(directory)
        elif len(in_dir) < 1:
            empty_f.append(item)
            rmtree(directory)
            empty += 1
            leng -= 1
    keep_log(f"\n - {leng} Total Folders\n - {double} Double Deleted")
    for item in double_f:
        keep_log(f"\n    + {item}")
    keep_log(f"\n - {empty} Empty Deleted")
    for item in empty_f:
        keep_log(f"\n    + {item}")    
    keep_log(f"\n - {zips} Zips\n - {other} Other Files\n - {cr} Cr Deleted\n")

def lister():
    print(" - lister:")
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
    keep_log(f"\n\nAvarage File Size: {total/(len(size)+1)}\nMax File Size: {max}\nMin File Size: {min}\n")
    print(f"\nAvarage File Size: {total/(len(size)+1)}\nMax File Size: {max}\nMin File Size: {min}\n")

def check_all(state = None):
    keep_log("\n---------------------------------------------------------------------------------\n")
    if state == 0:
        get_list()
        lister()
    else:
        main_check()
        check_hunted()

if __name__ == '__main__':
    check_all(0)
    