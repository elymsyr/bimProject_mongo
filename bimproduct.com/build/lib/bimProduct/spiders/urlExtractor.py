import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from codecs import open
from requests import get
from re import compile, IGNORECASE
from docs.var import FOR_MAIN_DATAS, SECOND_DATAS

# scrapy crawl urlExtract

class UrlproductextractSpider(CrawlSpider):
    name = "UrlProductExtract"
    allowed_domains = ["bimobject.com"]
    crawled = []
    urls = []
    categories = []
    sub_categories = []
    # with open(f"{SECOND_DATAS}", 'r+') as f:
    #     for url in f.readlines():
    #         urls.append(url.strip())
    #         crawled.append(url.strip())
    # with open(f"{FOR_MAIN_DATAS}", 'r', "utf-8") as f:
    #     for url in f.readlines():
    #         crawled.append(url.strip())
    # with open(f"{SECOND_DATAS}", 'w+') as f:
    #     f.write('')
    #     f.close()
    start_urls = urls
    rules = [(Rule(LinkExtractor(allow='bimobject'), callback="parse_from_categories", follow= False)),]

    def parse_from_categories(self, response):
        url = response.url
        txt = get(url).text
        tgs = compile(r'<a[^<>]+?href=([\'\"])(.*?)\1', IGNORECASE)
        for match in tgs.findall(txt):
            match = str(list(match)[1])
            if '/product/' in match and 'en/' in match:
                if match.startswith('https://') and not match.startswith('https://bimobject'):
                    pass
                elif not match.startswith('https://'):
                    match = f"https://bimobject.com{match}"
                    if match not in self.crawled:
                        with open(f'{FOR_MAIN_DATAS}', 'a+', 'utf-8') as f:
                            f.write(f"{match}\n")
                            self.crawled.append(match)
                        with open(f'{SECOND_DATAS}', 'a+', 'utf-8') as f:
                            f.write(f"{match}\n")
                else:
                    if match not in self.crawled:
                        with open(f'{FOR_MAIN_DATAS}', 'a+', 'utf-8') as f:
                            f.write(f"{match}\n")
                            self.crawled.append(match)
                        with open(f'{SECOND_DATAS}', 'a+', 'utf-8') as f:
                            f.write(f"{match}\n")

# scrapy crawl urlExtract