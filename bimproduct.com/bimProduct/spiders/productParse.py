import scrapy
from pandas import read_csv
from csv import writer
from bimProduct.items import NewProduct
from re import sub
from mongo_connection import MongoConnection

MAIN_DATAS = 'product_data.txt'

class ProductparseSpider(scrapy.Spider):
    name = "productParse"
    allowed_domains = ["bimobject.com"]
    start_urls = ["https://bimobject.com"]
    id_adding_number = 0
    id = 0
    merge_url = []
    crawled = []
    used_ids = []
    connection = MongoConnection()
    results = connection.find_all()
    connection.delete_all()
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
            else:
                yield scrapy.Request(url, self.parse_item)
                
    def keep_log(self, string):
        with open('mongo_log.txt', 'a', encoding='utf-8') as f:
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

    def clear_text(self, string):
        clean = [sub('<[^>]*>', '', string)]
        clean_text = sub(r"(\w)([A-Z])", r"\1 \2", str(clean))
        return clean_text[2:-2]

    def parse_item(self,response):
        new_product = NewProduct()

        name = response.css('h1.primary-heading::text').extract_first()
        new_product['name'] = self.clear_data(name)

        category = response.css('div.breadcrumb-section.uk-container-xlarge > app-breadcrumb > ul > li:nth-child(3) > a::text').extract_first()
        new_product['category'] = self.clear_data(category)

        subcategory = response.css('div.breadcrumb-section.uk-container-xlarge > app-breadcrumb > ul > li:nth-child(4) > a::text').extract_first()
        new_product['subcategory'] = self.clear_data(subcategory)

        new_product['url'] = self.clear_data(response.url)
        
        direct_link = response.css('div.content > a.ng-star-inserted::text').extract_first()
        new_product['direct_link'] = self.clear_data(direct_link)

        brand = response.css('span.secondary-heading::text').extract_first()
        new_product['brand'] = self.clear_data(brand)

        spec = response.css('li.specification-list-item > div > span::text').getall()
        spec = (' '.join(spec)).replace('\n', ' ')
        new_product['spec'] = self.clear_data(spec)

        desc = response.css('span.description-text::text').getall()
        desc = (' '.join(desc)).replace('\n', ' ')
        new_product['desc'] = self.clear_data(desc)

        tech_spec = response.xpath('/html/body/app-root/div[1]/div/app-product-page/div/div[2]/div[2]/div[3]/div/app-detailed-info[2]/div/div/ul').getall()
        tech_spec = (' '.join(tech_spec)).replace('\n', ' ') 
        tech_spec = str(self.clear_text(tech_spec))
        new_product['tech_spec'] = self.clear_data(tech_spec)

        classification = response.xpath('/html/body/app-root/div[1]/div/app-product-page/div/div[2]/div[2]/div[3]/div/app-detailed-info[5]/div[1]/div/ul').getall()
        classification = (' '.join(classification)).replace('\n', ' ') 
        classification = str(self.clear_text(classification))
        new_product['classification'] = self.clear_data(classification)

        related = response.xpath('/html/body/app-root/div[1]/div/app-product-page/div/div[2]/div[2]/div[3]/div/app-detailed-info[4]/div[1]/div/ul').getall()
        related = (' '.join(related)).replace('\n', ' ') 
        related = str(self.clear_text(related))
        new_product['related'] = self.clear_data(related)

        new_product['votes'] = response.css('span.votes::text').extract_first()
        if new_product['votes'] == None or new_product['votes'].strip() == '':
            new_product['votes'] = '(0 reviewes)'
        new_product['rating'] = response.css('span.rating::text').extract_first()
        if new_product['rating'] == None or new_product['rating'].strip() == '':
            new_product['rating'] = 'No Rating'

        id = self.id_assign(new_product['category'], new_product['subcategory'], new_product['name'])
        data = [id, 0, new_product['name'], new_product['category'],new_product['subcategory'],new_product['url'],new_product['direct_link'],new_product['brand'],new_product['votes'], new_product['rating'], new_product['tech_spec'], new_product['spec'], new_product['desc'], new_product['related'],new_product['classification']]
        for item in range(len(data)):
            if item == 1:
                pass
            else:
                if data[item] == None or data[item] == 'None':
                    self.keep_log(f'None found: {data[0]} - {data[5]}\n')
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
        except:
            self.keep_log(f'Not written: {data[0]} - {data[5]}')
            

# scrapy crawl productParse