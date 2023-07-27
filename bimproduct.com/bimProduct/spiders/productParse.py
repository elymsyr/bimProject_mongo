import scrapy
from bimProduct.items import NewProduct
from random import randint
from docs.mongo_connection import MongoConnection

MAIN_DATAS = 'docs/product_data.txt'
LOG = 'docs/mongo_log.txt'

class ProductparseSpider(scrapy.Spider):
    name = "productParse"
    allowed_domains = ["bimobject.com"]
    start_urls = ["https://bimobject.com"]
    id_adding_number = randint(0, 999)
    id = 0
    merge_url = []
    crawled = []
    used_ids = []
    connection = MongoConnection()
    results = connection.find_all()
    url_data = results[0]
    id_data = results[1]
    for id in id_data:
        used_ids.append(id)
    for url in url_data:
        crawled.append(url[12:])
        
    categories = {
        'Fabrics': [],
        'Fire Products': [],
        'Construction': [],
        'Building Materials': [],
        'Engineering & Infrastructure': [],
        'Flooring': [],
        'Electronics': [],
        'HVAC': [],
        'Landscaping': [],
        'Electrical': [],
        'Lighting': [],
        'Signage': [],
        'Furniture': [],
        'Medical': [],
        'Sanitary': [],
        'Sports & Recreation': [],
        'Software': [],
        'Windows': [],
        'Walls': [],
        'Plumbing': [],
        'Loading Equipment': [],
        'Kitchen': [],
        'Doors': []
    }
    
    with open(MAIN_DATAS, 'r', encoding='utf-8') as f:
        for url in f.readlines():
            merge_url.append(url.strip())
    start_urls = merge_url

    def start_requests(self):
        for url in self.start_urls:
            if url[8:] in self.crawled:
                print(f"Already crawledd.")
                self.id_adding_number += 1
            else:
                yield scrapy.Request(url, self.parse_item)
                
    def keep_log(self, string):
        with open(LOG, 'a', encoding='utf-8') as f:
            f.write(f"{string}")                
                
    def clear_data(self, data):
        if str(data).strip() == '' or data == None:
            data = 'None'        
        while data[0] == ' ':
            data = data[1:]
        data = data.replace('[', '')
        data = data.replace(']', '')
        data = data.replace('"', '')
        data = data.replace('\n', ' ')
        return data

    def parse_item(self,response):
        new_product = NewProduct()

        name = response.css('h1.primary-heading::text').extract_first()
        new_product['name'] = self.clear_data(name)

        category = response.css('div.breadcrumb-section.uk-container-xlarge > app-breadcrumb > ul > li:nth-child(3) > a::text').extract_first()
        new_product['category'] = self.clear_data(category)

        subcategory = response.css('div.breadcrumb-section.uk-container-xlarge > app-breadcrumb > ul > li:nth-child(4) > a::text').extract_first()
        new_product['subcategory'] = self.clear_data(subcategory)
        
        new_product['url'] = response.url
        
        new_product['images'] = response.xpath("//app-image-slider//img/@src").extract_first()

        new_product['direct_link'] = response.xpath("//app-detailed-info[contains(@data-test, 'links-section')]//text()").getall()

        brand = response.css('span.secondary-heading::text').extract_first()
        new_product['brand'] = self.clear_data(brand)

        new_product['spec'] = response.xpath("//app-detailed-info[contains(@data-test, 'specification-section')]//text()").getall()

        new_product['desc'] = response.xpath("//div[contains(@data-test, 'description-text-container')]//text()").getall()

        new_product['tech_spec'] = response.xpath("//app-detailed-info[contains(@data-test, 'technical-specification-section')]//text()").getall()

        new_product['classification'] = response.xpath("//app-detailed-info[contains(@data-test, 'classification-section')]//text()").getall()

        new_product['related'] = response.xpath("//app-detailed-info[contains(@data-test, 'related-section')]//text()").getall()
        
        new_product['properties'] = response.xpath("//app-detailed-info[contains(@data-test, 'properties-section')]//text()").getall()

        new_product['votes'] = response.css('span.votes::text').extract_first()
        if new_product['votes'] == None or new_product['votes'].strip() == '':
            new_product['votes'] = '(0 reviewes)'
        new_product['rating'] = response.css('span.rating::text').extract_first()
        if new_product['rating'] == None or new_product['rating'].strip() == '':
            new_product['rating'] = 'No Rating'

        id = self.id_assign(new_product['category'], new_product['subcategory'], new_product['name'])
        data = [id, 0, new_product['name'], new_product['category'],new_product['subcategory'],new_product['url'],new_product['images'],new_product['direct_link'][2:],new_product['brand'],new_product['votes'], new_product['rating'], new_product['tech_spec'], new_product['spec'], new_product['desc'], new_product['related'],new_product['classification'],new_product['properties']]
        for item in range(len(data)):
            if item == 1:
                pass
            else:
                if data[item] == None:
                    self.keep_log(f'None found: {data[0]} | ')
                    data[item] = 'None'
                if isinstance(data[item], list) and len(data[item]) == 0:
                    self.keep_log(f'None found: {data[0]} | ')
                    data[item] = 'None'
        self.write_data(data)
    
    def cat_id(self, cat, sub_cat):
        sub_id = 99
        try:
            cat_id = list(self.categories.keys()).index(f"{cat}")
        except:
            cat_id = 99
        if cat_id < 21 or cat_id > -1:
            if sub_cat in self.categories[f'{cat}']:
                sub_id = self.categories[f'{cat}'].index(sub_cat)
            else:
                self.categories[f'{cat}'].append(sub_cat)
                sub_id = self.categories[f'{cat}'].index(sub_cat)
        return [cat_id, sub_id]

    def number_defuser(self, number, mod):
        if mod == 0:
            number_one = f"000{str(number[0] % 100)}"
            number_two = f"000{str(number[1] % 100)}"
            return str(f"{number_one[-2:]}{number_two[-2:]}")
        elif mod == 1:
            id_adding = f"00{self.id_adding_number % 1000}"
            self.id_adding_number += 1
            return id_adding[-3:]
        elif mod == 2:
            name_one = int(ord(number[0])) % 10
            name_two = int(ord(number[1])) % 10
            return str(f"{name_one}{name_two}")
        else: return '99'
 
    def id_assign(self, cat, sub_cat, name):
        pre_id = self.cat_id(cat, sub_cat)
        pre_id = self.number_defuser(pre_id, 0)
        mid_id = self.number_defuser(name, 2)
        post_id = self.number_defuser(0, 1)
        new_id = (f"{pre_id}-{mid_id}-{post_id}")[:11]
        while new_id in self.used_ids:
            self.id_adding_number += 1
            post_id = self.number_defuser(0, 1)
            new_id = (f"{pre_id}-{mid_id}-{post_id}")[:11]
        return new_id

    def write_data(self, data):
        try:
            self.connection.insert(data)
        except Exception as e:
            self.keep_log(f'\nNot written: {data[0]} - {data[5]} --> Error: {e}')

# scrapy crawl productParse