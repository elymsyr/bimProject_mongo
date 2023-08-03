from scrapyd_api import ScrapydAPI

# https://scrapeops.io/python-scrapy-playbook/extensions/scrapy-scrapyd-guide/

scrapyda = ScrapydAPI('http://127.0.0.1:6800/')
project = scrapyda.schedule('bimProduct', 'productParse')
print(scrapyda.job_status('bimProduct', project))
# print(scrapyda.job_status('bimProduct', 'ff0faa1f2cbf11eebf02809133c35112'))
# scrapyda.list_jobs('default')
# print(project)
# scrapyda.cancel('bimProduct', '55eafa902cbc11ee8dc4809133c35112')

# print(scrapyda.list_projects())
# scrapyda.delete_project('bimProduct')
# print(scrapyda.list_projects())
# print(scrapyda.list_spiders('bimProduct'))
# scrapyd-deploy default

# scrapyda.delete_project('bimProduct')