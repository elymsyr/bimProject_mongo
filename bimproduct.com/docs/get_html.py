import re
from time import sleep
from selenium.webdriver import Chrome
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.by import By

def var_selenium(url, old_image):
    chrome_options = ChromeOptions()
    chrome_options.add_argument('--headless=new')
    driver = Chrome(options=chrome_options)
    driver.implicitly_wait(5)
    print("Driver opened.")
    sleep(2)
    properties = []
    other_images = []
    driver.get(url)
    sleep(2)
    l = driver.find_element(By.XPATH, "//app-detailed-info[contains(@data-test, 'properties-section')]")
    txt = l.get_attribute('innerHTML')
    p = re.compile(r'<.*?>')
    tgs = str(p.sub('\n', txt)).split('\n')
    for item in tgs:
        if item.strip() != '':
            properties.append(item.strip())
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



print(var_selenium('https://www.bimobject.com/en/woehr/product/woehr_combilift_542', 'https://admincontent.bimobject.com/public/productimages/41bb4561-5c69-4b19-b9db-cdd611235b97/9527ab73-1562-431d-9efd-fc36825ed591/653807?width=675&height=675&compress=true'))