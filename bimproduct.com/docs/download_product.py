from time import sleep
from selenium.webdriver import Chrome
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.by import By
from os import makedirs, listdir, startfile
from os.path import exists, realpath
from multiprocessing import Process
from shutil import rmtree
from check_functions import fix_state, check_all
from mongo_connection import MongoConnection
try:
    from var import DOWNLOAD_FOLDER, MULTIQUEUE_NUMBER, SLEEP_BREAK, MAX_NUMBER_AT_A_TIME
except:
    from docs.var import DOWNLOAD_FOLDER, MULTIQUEUE_NUMBER, SLEEP_BREAK, MAX_NUMBER_AT_A_TIME
class DownloadItem():
    def __init__(self, url, id, driver=None) -> None:
        if driver == None:
            raise Exception("Driver needed.")
        else: self.driver = driver
        self.id = id
        self.url = url

    def download_item(self):
        try:
            s_time = 1
            self.driver.get(self.url)
            sleep(s_time*2)
            d_button = self.driver.find_element(By.XPATH, "//div[@class='button-container']/button")
            d_button.click()
            sleep(s_time)
            download = self.driver.find_element(By.XPATH, "//div[contains(@class, 'footer-section')]/button[contains(@class, 'download-button')]")
            download.click()
            print(f'{self.id} started download')
            return 1
        except:
            try:
                s_time = 2
                self.driver.get(self.url)
                sleep(s_time*2)
                d_button = self.driver.find_element(By.XPATH, "//div[@class='button-container']/button")
                d_button.click()
                sleep(s_time)
                download = self.driver.find_element(By.XPATH, "//div[contains(@class, 'footer-section')]/button[contains(@class, 'download-button')]")
                download.click()
                print(f'{self.id} started download')
                return 1
            except:
                try:
                    s_time = 3
                    self.driver.get(self.url)
                    sleep(s_time*2)
                    d_button = self.driver.find_element(By.XPATH, "//div[@class='button-container']/button")
                    d_button.click()
                    sleep(s_time)
                    download = self.driver.find_element(By.XPATH, "//div[contains(@class, 'footer-section')]/button[contains(@class, 'download-button')]")
                    download.click()
                    print(f'{self.id} started download')
                    return 1
                except:
                    try:
                        s_time = 3.5
                        self.driver.get(self.url)
                        sleep(s_time*2)
                        d_button = self.driver.find_element(By.XPATH, "//div[@class='button-container']/button")
                        d_button.click()
                        sleep(s_time)
                        download = self.driver.find_element(By.XPATH, "//div[contains(@class, 'footer-section')]/button[contains(@class, 'download-button')]")
                        download.click()
                        print(f'{self.id} started download')
                        return 1
                    except Exception as error:
                        print(f"{self.id} Download Error\n")
                        return error

def login(driver):
    try:
        driver.get("https://account.bimobject.com/login")
        sleep(3)
        input = driver.find_element(By.XPATH, '//*[@id="username"]')
        input.send_keys("gamesstochange@gmail.com")
        input = driver.find_element(By.XPATH, '//*[@id="password"]')
        input.send_keys("aqwer1234")
        l_button = driver.find_element(By.XPATH, '//*[@id="submit-button"]')
        l_button.click()
        return 1
    except:
        try:
            driver.get("https://account.bimobject.com/login")
            sleep(5)
            input = driver.find_element(By.XPATH, '//*[@id="username"]')
            input.send_keys("gamesstochange@gmail.com")
            input = driver.find_element(By.XPATH, '//*[@id="password"]')
            input.send_keys("aqwer1234")
            l_button = driver.find_element(By.XPATH, '//*[@id="submit-button"]')
            l_button.click()
            return 1
        except: return 0

def create_process(directory, url, id):
   return Process(target=download, args=(directory, url, id))  

def download(directory, url, id):
    if not exists(directory):
        makedirs(f"{directory}")
    try:
        before = listdir(f"{directory}")
        chrome_options = ChromeOptions()
        prefs = {'download.default_directory' : f'{directory}'}
        chrome_options.add_experimental_option('prefs', prefs)
        chrome_options.add_argument('--headless=new')
        driver = Chrome(options=chrome_options)
        state = login(driver)
        if state == 1:
            test_item = DownloadItem(url, id, driver)
            download_state = test_item.download_item()
            if download_state == 1:
                now = listdir(f"{directory}")
                for e in now:
                    if e.endswith(".crdownload") or e.endswith(".tmp"):
                        now.remove(e)
                sleep_time = 0
                while before == now:
                    if sleep_time > SLEEP_BREAK:
                        raise Exception("ERROR: Waited for too long !")
                    now = listdir(f"{directory}")
                    for e in now:
                        if e.endswith(".crdownload") or e.endswith(".tmp"):
                            now.remove(e)
                            sleep_time += 1
                    sleep_time += 2
                    sleep(1)
                driver.quit()
                return download_control(id)
            else:
                print(f"Download Error: {id}")
        else:
            print(f"Login Failed: {id}")
        driver.quit()
    except Exception as error: 
        print(f"Not Downloaded: {id} --> {error}")

def start_download(folder, state = '0'):
    if state.isdigit() and int(state.replace('-', '')) == 0:
        connection = MongoConnection()
        print("Getting data...")
        result = connection.connection.find({'download_state':0})
        state_data = []
        id_data = []
        url_data = []
        for res in result[:MAX_NUMBER_AT_A_TIME]:
            state_data.append(res['download_state'])
            id_data.append(res['p_id'])
            url_data.append(res['url'])
        print(len(id_data))
        processQueue = []
        print("Starting Checking...")
        check_all(0)
        print("Checked")
        print("Download Starting...")
        for index in range(len(state_data)):
            if state_data[index] != 1:
                if not exists(folder):
                    makedirs(folder)
                directory = f"{folder}\\{id_data[index]}"
                state = create_process(directory, url_data[index], id_data[index])
                processQueue.append(state)
        for order in range(len(processQueue)):
            state_id = []
            if order % MULTIQUEUE_NUMBER == 0:
                print(f"\n{len(processQueue) - order} in queue...")
                for _ in range(MULTIQUEUE_NUMBER):
                    state_id.append(id_data[order])
                    processQueue[order].start()
                    print(f"running process {order}")
                    order += 1               
                order -= MULTIQUEUE_NUMBER
                for _ in range(MULTIQUEUE_NUMBER):
                    processQueue[order].join()
                    print(f"finished process {order}")
                    order += 1
    else:
        connection = MongoConnection()
        c_download = 1
        find = connection.connection.find_one({'p_id': f'{state}'})
        if find != None:
            directory = f"{DOWNLOAD_FOLDER}\\{state}"
            if not exists(directory):
                pass
            else:
                in_dir = listdir(directory)
                if len(in_dir) == 1:
                    if not in_dir[0].endswith(".crdownload") or not in_dir[0].endswith(".tmp"):
                        c_download = 0
                else:
                    rmtree(directory, ignore_errors=True)
            if c_download == 1:
                makedirs(f"{directory}")
                url = find['url']
                chrome_options = ChromeOptions()
                prefs = {'download.default_directory' : f'{directory}'}
                chrome_options.add_experimental_option('prefs', prefs)
                chrome_options.add_argument('--headless=new')
                driver = Chrome(options=chrome_options)
                login_state = login(driver)
                before = listdir(f"{directory}")
                if login_state == 1:
                    test_item = DownloadItem(url, state, driver)
                    download_state = test_item.download_item()
                    if download_state == 1:
                        now = listdir(f"{directory}")
                        for e in now:
                            if e.endswith(".crdownload") or e.endswith(".tmp"):
                                now.remove(e)
                        sleep_time = 0
                        while before == now:
                            if sleep_time > SLEEP_BREAK:
                                raise Exception("ERROR: Waited for too long !")
                            now = listdir(f"{directory}")
                            for e in now:
                                if e.endswith(".crdownload") or e.endswith(".tmp"):
                                    now.remove(e)
                                    sleep_time += 1
                            sleep_time += 2
                            sleep(1)
                        driver.quit()
                        state = download_control(state)
                        if state:
                            path = realpath(directory)
                            startfile(path)
                            return 1
                    else:
                        print(f"Download Error: {state}")
                else:
                    print(f"Login Failed: {state}")
            else:
                print(f"Already downloaded: {state}")
                path = realpath(directory)
                startfile(path)
            return 0

def download_control(id):
    directory = f"{DOWNLOAD_FOLDER}\\{id}"    
    in_dir = listdir(directory)
    if len(in_dir) == 1:
        if not in_dir[0].endswith(".crdownload") or not in_dir[0].endswith(".tmp"):
            fix_state(id, 1)
            print(f"{id} downloaded")
            return 1
        else:
            rmtree(directory, ignore_errors=True)
            fix_state(id, 0)
            print(f"{id} error")
            return 0
    else:
        rmtree(directory, ignore_errors=True)
        fix_state(id, 0)
        print(f"{id} error")
        return 0
    
if __name__ == '__main__':
    # state = input("select[id] or all[0] : ")
    state = '0'
    if state == '0':
        for _ in range(250):
            start_download(DOWNLOAD_FOLDER, state) # "1400-87-887"