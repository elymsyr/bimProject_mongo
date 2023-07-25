from time import sleep
from selenium.webdriver import Chrome
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.by import By
from os import makedirs, listdir
from os.path import exists
from multiprocessing import Process
from check_functions import check_all, get_list
from mongo_connection import MongoConnection

DOWNLOAD_FOLDER = 'C:\\Users\\orhun\\OneDrive\\Belgeler\\Github Repo\\bimObject\\Include\\BimDownloaded'
DOWNLOAD_LOG = 'project_docs/download_log.txt'
MULTIQUEUE_NUMBER = 2
SLEEP_BREAK = 40*2

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

def select_downloaded(connection, id):
    connection.update_downloads(1, id)

def download(directory, url, id):
    connection = MongoConnection()
    if not exists(f"{directory}"):
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
                select_downloaded(connection, id)
                return 1
            else:
                print(f"Download Item Error")
        else:
            print(f"Login Failed")
    except Exception as error: 
        print(f"Download Error:\n{error}")

def start_download(folder):
    connection = MongoConnection()
    result = connection.find_all()
    state_data = result[2] 
    id_data = result[1]
    url_data = result[0]               
    processQueue = []
    for index in range(len(state_data)):
        if state_data[index] != 1:
            if not exists(folder):
                makedirs(folder)
            directory = f"{folder}\\{id_data[index]}"
            state = create_process(directory, url_data[index], id_data[index])
            processQueue.append(state)
    for order in range(len(processQueue)):
        if order % MULTIQUEUE_NUMBER == 0:
            print(f"\n{len(processQueue) - order} in queue...")
            for _ in range(MULTIQUEUE_NUMBER):
                processQueue[order].start()
                print(f"running process {order}")
                order += 1               
            order -= MULTIQUEUE_NUMBER
            for _ in range(MULTIQUEUE_NUMBER):
                processQueue[order].join()
                print(f"finished process {order}")
                order += 1

def create_process(directory, url, id):
   return Process(target=download, args=(directory, url, id))


