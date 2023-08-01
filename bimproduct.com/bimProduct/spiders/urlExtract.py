import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from bimProduct.items import BimobjectsItem
from codecs import open
from docs.var import FOR_MAIN_DATAS

# scrapy crawl urlExtract

class UrlextractSpider(CrawlSpider):
    name = "urlExtract"
    allowed_domains = ["bimobject.com"]
    category_links = ['https://www.bimobject.com/en/categories/building-materials?sort=trending&page=', 'https://www.bimobject.com/en/categories/construction?sort=trending&page=', 'https://www.bimobject.com/en/categories/doors?sort=trending&page=', 'https://www.bimobject.com/en/categories/electrical?sort=trending&page=', 'https://www.bimobject.com/en/categories/electronics?sort=trending&page=', 'https://www.bimobject.com/en/categories/engineering?sort=trending&page=', 'https://www.bimobject.com/en/categories/fabrics?sort=trending&page=', 'https://www.bimobject.com/en/categories/fire-products?sort=trending&page=', 'https://www.bimobject.com/en/categories/flooring?sort=trending&page=', 'https://www.bimobject.com/en/categories/furniture?sort=trending&page=', 'https://www.bimobject.com/en/categories/hvac?sort=trending&page=', 'https://www.bimobject.com/en/categories/kitchen?sort=trending&page=', 'https://www.bimobject.com/en/categories/landscaping?sort=trending&page=', 'https://www.bimobject.com/en/categories/lighting?sort=trending&page=', 'https://www.bimobject.com/en/categories/loading-equipment?sort=trending&page=', 'https://www.bimobject.com/en/categories/medical?sort=trending&page=', 'https://www.bimobject.com/en/categories/plumbing?sort=trending&page=', 'https://www.bimobject.com/en/categories/sanitary?sort=trending&page=', 'https://www.bimobject.com/en/categories/signage?sort=trending&page=', 'https://www.bimobject.com/en/categories/software?sort=trending&page=', 'https://www.bimobject.com/en/categories/sports-recreation?sort=trending&page=', 'https://www.bimobject.com/en/categories/walls?sort=trending&page=', 'https://www.bimobject.com/en/categories/windows?sort=trending&page=']
    crawled = []
    urls = []
    categories = []
    sub_categories = []
    for link in category_links:
        urls.append(f"{link}1")
    start_urls = urls
    id_number = 1
    rules = [(Rule(LinkExtractor(allow=("/categories/")), callback="parse_from_categories", follow= True)),]

    def parse_from_categories(self, response):
        product = BimobjectsItem()
        product_template = response.css("div.product-card-content")
        for p in product_template:
            # product['name'] = str(p.css('span.product-card-title::text').extract_first()).replace('"', '')
            product['url'] = "https://bimobject.com" + (str(p.css('div.product-card-image-container > a::attr(href)').extract_first()).replace('../', ''))
            the_link = f"{product['url']}"
            if the_link not in self.crawled:
                with open(FOR_MAIN_DATAS, 'a', 'utf-8') as f:
                    f.write(f"{the_link}\n")
                    self.crawled.append(the_link)

# scrapy crawl urlExtract