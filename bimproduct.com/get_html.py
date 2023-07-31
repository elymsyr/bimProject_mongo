import re
from time import sleep
from selenium.webdriver import Chrome
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.by import By
from docs.mongo_connection import MongoConnection
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.common.exceptions import NoSuchElementException, TimeoutException
TIMEOUT = 10
urls = ['https://www.bimobject.com/en/efaflex/product/s-stt-s-6000x6000','https://www.bimobject.com/en/kahrs/product/oakmoon596541',  'https://www.bimobject.com/en/kahrs/product/ashvaila586473']

def var_selenium(urls):
    chrome_options = ChromeOptions()
    # chrome_options.add_argument('--headless=new')
    driver = Chrome(options=chrome_options)
    driver.implicitly_wait(2)
    con = MongoConnection()
    print("Driver opened.")
    properties = []
    other_images = []
    old_image = []
    for url in urls:
        driver.get(url)
        try:
            element_present = expected_conditions.presence_of_element_located((By.XPATH, "//img[contains(@alt, 'BIMobject logo')]"))
            WebDriverWait(driver, TIMEOUT).until(element_present)
            print("Page loaded successfully!")
        except:
            print("Timed out waiting for page to load.")
        if element_present:
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
                print("Prop found.")
            except (NoSuchElementException, TimeoutException):
                print("Prop was not found.")
            except:
                print(f"Something went wrong with {url}")
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
                old_image.append(new)
    print(properties, old_image)
    return [properties, old_image]

def var_selenium_w(driver, url, old_image):
    print("Driver opened.")
    sleep(2)
    other_images = []
    driver.get(url)
    sleep(2)
    try:
        l = driver.find_element(By.XPATH, "//app-detailed-info[contains(@data-test, 'properties-section')]")
        txt = l.get_attribute('innerHTML')
        p = re.compile(r'<.*?>')
        tgs = str(p.sub('\n', txt)).split('\n')
        for item in tgs:
            if item.strip() != '':
                properties.append(item.strip())
    except:
        properties = 'None'
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
    if properties != 'None' or other_images != []:
        new_images = [old_image]
        for new in other_images:
            new_images.append(new)
        return [properties, new_images]
    else:
        return ['None', [old_image]]



# print(var_selenium('https://www.bimobject.com/en/woehr/product/woehr_combilift_542', 'https://admincontent.bimobject.com/public/productimages/41bb4561-5c69-4b19-b9db-cdd611235b97/9527ab73-1562-431d-9efd-fc36825ed591/653807?width=675&height=675&compress=true'))
var_selenium(urls)