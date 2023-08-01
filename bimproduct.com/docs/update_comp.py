import re
from selenium.webdriver import Chrome
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.by import By
from mongo_connection import MongoConnection
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from multiprocessing import Process
from var import UPDATE_LOG, TIMEOUT, MAX_DRIVER

def var_selenium():
    updated = []
    ready_urls = []
    counter = 1
    with open('docs/updated_urls.txt', 'r', encoding='utf-8') as f:
        for url in f.readlines():
            updated.append(url.strip())
    chrome_options = ChromeOptions()
    chrome_options.add_argument('--headless=new')
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = Chrome(options=chrome_options)
    driver.implicitly_wait(2)
    keep_log_error(" Driver opened.")
    print(" Driver opened.")
    con = MongoConnection()
    urls = find_url(con)
    for url in urls:
        if url not in updated:
            ready_urls.append(url)
    keep_log_error(f" Total item to update -> {len(ready_urls)}")
    print(f" Total item to update -> {len(ready_urls)}")
    keep_log_error(f" Total item updated before -> {len(updated)}")
    keep_log_error(f" Total item in db -> {len(urls)}")
    for url in ready_urls:
        page_load = 1
        keep_log_state(url)
        properties = []
        other_images = []
        try:
            old_image = find_old_image(url, con)
        except Exception as error:
            keep_log_error(f"    {error}")
            old_image = []
        driver.get(url)
        try:
            element_present = expected_conditions.presence_of_element_located((By.XPATH, "//img[contains(@alt, 'BIMobject logo')]"))
            WebDriverWait(driver, TIMEOUT).until(element_present)
            # keep_log_error("Page loaded successfully.")
            print(f"Page loaded successfully -> {counter}", end="\r")
            counter += 1
        except:
            keep_log_error("    Timed out waiting for page to load.")
            page_load = 0
        if page_load:
            try:
                prop_present = expected_conditions.presence_of_element_located((By.XPATH, "//app-detailed-info[contains(@data-test, 'properties-section')]"))
                WebDriverWait(driver, TIMEOUT).until(prop_present)
                l = driver.find_element(By.XPATH, "//app-detailed-info[contains(@data-test, 'properties-section')]")
                txt = l.get_attribute('innerHTML')
                p = re.compile(r'<.*?>')
                tgs = str(p.sub('\n', txt)).split('\n')
                for item in tgs:
                    if item.strip() != '':
                        properties.append(item.strip())
                keep_log_error("    Prop found.")
            except (NoSuchElementException, TimeoutException):
                keep_log_error("    Prop was not found.")
            except:
                keep_log_error("    Something went wrong.")
            try:
                l = driver.find_element(By.XPATH, "//app-image-slider")
                txt = str(l.get_attribute('innerHTML'))
                tgs = re.findall('src="([^"]+)"',txt)
                for img in tgs:
                    if img.startswith('https://admincontent.bimobject.com/public/productimages/'):
                        if tgs.count(img) > 1:
                            tgs.remove(img)
                        else:
                            other_images.append(img.replace('&amp;', '&'))
            except:
                other_images = []
            if other_images != []:
                for new in other_images:
                    if new not in old_image:
                        old_image.append(new)
            elif other_images == []:
                keep_log_error("    No more image found.")
            if other_images != [] or properties != []:
                try:
                    update(url, con, properties, old_image)
                    with open('docs/updated_urls.txt', 'a', encoding='utf-8') as f:
                        f.write(f"{url}\n")
                    keep_log_error(f"   Updated.")
                except Exception as a:
                    keep_log_error(f"   Update Failed: {a}")
        elif page_load == 0:
            keep_log_error("Page Error --> Program Ended")
            print("Page Error --> Program Ended")
            break
    keep_log_error("\n\n")

def update_process(url, order):
    log = []
    chrome_options = ChromeOptions()
    chrome_options.add_argument('--headless=new')
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = Chrome(options=chrome_options)
    name = (str(url).split('/'))[-1]
    driver.implicitly_wait(2)
    print(f"Driver {order+1} opened.")
    con = MongoConnection()    
    print(f"{name} assigned to driver {order}")
    page_load = 1
    properties = []
    other_images = []
    try:
        old_image = find_old_image(url, con)
    except Exception as error:
        old_image = []
    driver.get(url)
    try:
        element_present = expected_conditions.presence_of_element_located((By.XPATH, "//img[contains(@alt, 'BIMobject logo')]"))
        WebDriverWait(driver, TIMEOUT).until(element_present)
    except:
        log.append(f"     Error: Timed out waiting for page to load {name}")
        page_load = 0
    if page_load:
        try:
            prop_present = expected_conditions.presence_of_element_located((By.XPATH, "//app-detailed-info[contains(@data-test, 'properties-section')]"))
            WebDriverWait(driver, TIMEOUT).until(prop_present)
            l = driver.find_element(By.XPATH, "//app-detailed-info[contains(@data-test, 'properties-section')]")
            txt = l.get_attribute('innerHTML')
            p = re.compile(r'<.*?>')
            tgs = str(p.sub('\n', txt)).split('\n')
            for item in tgs:
                if item.strip() != '':
                    properties.append(item.strip())
        except (NoSuchElementException, TimeoutException):
            log.append(f"     Error: No prop {name}")
        except:
            log.append(f"     Error: Something went wrong {name}")
        try:
            l = driver.find_element(By.XPATH, "//app-image-slider")
            txt = str(l.get_attribute('innerHTML'))
            tgs = re.findall('src="([^"]+)"',txt)
            for img in tgs:
                if img.startswith('https://admincontent.bimobject.com/public/productimages/'):
                    if tgs.count(img) > 1:
                        tgs.remove(img)
                    else:
                        other_images.append(img.replace('&amp;', '&'))
        except:
            other_images = []
        if other_images != []:
            for new in other_images:
                if new not in old_image:
                    old_image.append(new)
        elif other_images == []:
            log.append(f"     Error: No more image {name}")
        if other_images != [] or properties != []:            
            try:
                update(url, con, properties, old_image)
                with open('docs/updated_urls.txt', 'a', encoding='utf-8') as f:
                    f.write(f"{url}\n")
                log.append(f"     Updated {name}")
            except Exception as a:
                            log.append(f"     Error: Update Failed {name}")
    elif page_load == 0:
        log.append(f"     Error: Page Error --> Program Ended {name}")
    keep_log_error(f"\n   {name} --> {url}:")
    for row in log:
        keep_log_error(row)
    driver.quit()

def var_selenium_process():
    keep_log_error("PROCESS QUEUE\n")
    updated = []
    with open('docs/updated_urls.txt', 'r', encoding='utf-8') as f:
        for url in f.readlines():
            updated.append(url.strip())
    processQueue = []
    ready_urls = []
    con = MongoConnection()
    print("Getting URL data...")
    urls = find_url(con)
    for url in urls:
        if url not in updated:
            ready_urls.append(url)
    keep_log_state(f"Total item updated before -> {len(updated)+1}")
    keep_log_state(f"Total item in db -> {len(urls)+1}")
    keep_log_state(f"Total item to update -> {len(ready_urls)+1}")
    print("Processing URLs...")
    total = len(ready_urls)+1
    start = 0
    end = len(ready_urls)
    step = MAX_DRIVER
    block = 0
    for i in range(start, end, step):
        x = i
        block += 1
        processQueue.append(ready_urls[x:x+step])
    keep_log_state(f"{block} block created. Each has {MAX_DRIVER} items.")
    for indexes in range(len(processQueue)):
        print(f"\n{indexes+1}/{len(processQueue)}\n")
        processes = []
        for order in range(len(processQueue[indexes])):
            create_process = Process(target=update_process, args=(processQueue[indexes][order], order))
            processes.append(create_process)
        for items in range(len(processes)):
            processes[items].start()
            print(f"{items+1} started")
        for items in range(len(processes)):
            processes[items].join()
            print(f"{items+1} finished")

def find_old_image(url, con):
    old_image = con.connection.find_one({'url':f'{url}'})
    return old_image['images']

def find_url(con):
    results = con.find_all()
    return results[0]
  
def update(url, con, prop, img):
    filter = { "url": f"{url}" }
    newvalues = { "$set": {
        "properties": tuple(prop),
        "images": tuple(img)
        }}
    con.connection.update_one(filter, newvalues)

def keep_log_error(error):
    with open(UPDATE_LOG, 'a', encoding='utf-8') as f:
        f.write(f"{error}\n")

def keep_log_state(url):
    with open(UPDATE_LOG, 'a', encoding='utf-8') as f:
        f.write(f" - {url}\n")

if __name__ == '__main__':
    var_selenium_process()