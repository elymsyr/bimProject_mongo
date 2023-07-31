import re
from selenium.webdriver import Chrome
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.by import By
from mongo_connection import MongoConnection
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from var import UPDATE_LOG, TIMEOUT

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
    var_selenium()