import scrapy

class NewProduct(scrapy.Item):
    name = scrapy.Field()
    category = scrapy.Field()
    subcategory = scrapy.Field()
    url = scrapy.Field()
    images = scrapy.Field()
    direct_link = scrapy.Field()
    brand = scrapy.Field()
    desc = scrapy.Field()
    spec = scrapy.Field()
    tech_spec = scrapy.Field()
    classification = scrapy.Field()
    related = scrapy.Field()
    properties = scrapy.Field()
    votes = scrapy.Field()
    rating = scrapy.Field()