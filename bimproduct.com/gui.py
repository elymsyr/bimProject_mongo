import tkinter as tk
from codecs import open
from os import system
from docs.download_product import start_download
from docs.mongo_connection import MongoConnection
from docs.var import SELECTORS, DOWNLOAD_FOLDER

check = ''

def openNewWindow():
    newWindow = tk.Toplevel(window)
    newWindow.title("Table")
    newWindow.geometry("1420x800")
    scrollbar = tk.Scrollbar(newWindow)
    scrollbar_x = tk.Scrollbar(newWindow)
    scrollbar.grid(row=1, column=0, sticky=tk.S+tk.E+tk.N)
    scrollbar_x.grid(row=1, column=0, sticky=tk.S+tk.E+tk.N)
    tk.Label(newWindow, text ="Table").grid(row=0, column=0, sticky=tk.W+tk.E+tk.N)
    data_entry = tk.Text(newWindow, width=180, height=85, yscrollcommand = scrollbar.set, xscrollcommand = scrollbar_x.set)
    scrollbar.config( command = data_entry.yview )
    scrollbar_x.config( command = data_entry.xview )
    data_entry.grid(row=1, column=0, sticky=tk.W+tk.E+tk.S+tk.N)
    save_button = tk.Button(newWindow, text="Save as Csv 'found_data/saved_csv.csv'", width=40, command=lambda: save(str(data_entry.get("1.0", tk.END))))
    save_button.grid(row=0, column=0, sticky=tk.N+tk.E)
    return data_entry

def save(csv_data):
    with open('docs/search_result.csv', "w+", "utf-8") as f:
        for s in SELECTORS:
            f.write(f"{s}, ")
    with open('docs/search_result.csv', "a", "utf-8") as f:
        f.write(csv_data)

def clear():
    global check
    check = ''
    search_box.delete(0, tk.END)
    
def download():
    download_id = download_box.get()
    start_download(DOWNLOAD_FOLDER, download_id)

def search():
    ret = [[], [], []]
    control = 0
    global check
    searching = search_box.get()
    con = MongoConnection()
    if searching == '' and check != '':
        control = 1
        results = con.connection.find({'category': {'$regex': f'{check}'}})
    elif searching != '' and check == '':
        control = 1
        if (searching.replace('-', '')).isdigit():
            results = con.connection.find({'p_id': {'$regex': f'{searching}'}})
        else:
            results = con.connection.find({'name': {'$regex': f'{searching.capitalize()}'}})
    elif searching != '' and check != '':
        control = 1
        results = con.connection.find({'category': {'$regex': f'{check}'}, 'name': {'$regex': f'{searching}'}})
    else:
        control = 0
        print(f"\nPlease fill in the blanks.\n")
    if control == 1: 
        data_entry = openNewWindow()
        data = []
        for result in results:
            ret[2].append(result["url"])
            ret[0].append(result["p_id"])
            ret[1].append(result["name"])
        for scope in range(len(ret[0])):
            row = f'"{ret[0][scope]}", "{ret[1][scope]}", "{ret[2][scope]}"'
            data.append(row)
        data = str('\n'.join(data))
        data_entry.config(state=tk.NORMAL )
        data_entry.insert("end",str(data))
        data_entry.config(state=tk.DISABLED)

def listbox_used(event):
    global check
    check = listbox.get(listbox.curselection())
    
def func_a():
    command = 'py main.py -c'
    system(f"start cmd /c {command}")
def func_b():
    command = 'py main.py -u'
    system(f"start cmd /c {command}")    
def func_c():
    command = 'py main.py -x'
    system(f"start cmd /c {command}")    

window = tk.Tk()
window.title("BIMOBJECT")
window.config(padx=40, pady=40)

# output = tk.Text(window, width=36, height=8)
# output.grid(row=6, column=1, sticky=tk.W+tk.N)
# scrollbar_y = tk.Scrollbar(window,orient=tk.VERTICAL,command=output.yview)
# scrollbar_x = tk.Scrollbar(window,orient=tk.HORIZONTAL,command=output.xview)
# scrollbar_y.grid(row=6, column=1, sticky=tk.N+tk.S+tk.E)
# scrollbar_x.grid(row=6, column=1, sticky=tk.W+tk.S+tk.E)

search_for = tk.Label(text="Search for: ")
search_for.grid(row=0, column=0, sticky=tk.W)
search_box = tk.Entry(width=50)
search_box.grid(row=0, column=1, sticky=tk.E)
search_box.focus()

listbox = tk.Listbox(height=10, width=50)
cats = ["Fabrics", "Fire Products","Construction","Furniture","Sanitary","Doors","Lighting","Landscaping","Kitchen", "Building Materials", "Engineering & Infrastructure","Flooring","Electronics","Software","HVAC","Electrical","Signage","Medical", "Sports & Recreation", "Windows"]
for item in cats:
    listbox.insert(cats.index(item),item)
listbox.bind("<<ListboxSelect>>", listbox_used)
scrollbar = tk.Scrollbar(window,orient=tk.VERTICAL,command=listbox.yview)
scrollbar.grid(row=1, column=1, rowspan=2, sticky=tk.N+tk.S+tk.E)
listbox['yscrollcommand'] = scrollbar.set
listbox.grid(row=1, column=1, rowspan=2, sticky=tk.W)

search_button = tk.Button(text="Search", width=12, command=search)
search_button.grid(row=4, column=1, sticky=tk.W)
clear_button = tk.Button(text="Clear", width=12, command=clear)
clear_button.grid(row=4, column=1)
download_button = tk.Button(text="Download", width=12, command=download)
download_button.grid(row=4, column=1, sticky=tk.E)
donwload_for = tk.Label(text="Download with ID: ")
donwload_for.grid(row=3, column=0, sticky=tk.W)
download_box = tk.Entry(width=50)
download_box.grid(row=3, column=1, sticky=tk.E)

check_button = tk.Button(text="Check", width=12, command=func_a)
check_button.grid(row=5, column=1, sticky=tk.W)
update_button = tk.Button(text="Update", width=12, command=func_b)
update_button.grid(row=5, column=1)
hunt_button = tk.Button(text="Run Spider", width=12, command=func_c)
hunt_button.grid(row=5, column=1, sticky=tk.E)

window.mainloop()