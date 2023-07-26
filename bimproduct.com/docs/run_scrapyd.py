from scrapyd_api import ScrapydAPI

# https://scrapeops.io/python-scrapy-playbook/extensions/scrapy-scrapyd-guide/

scrapyda = ScrapydAPI('http://127.0.0.1:6800/')
# project = scrapyda.schedule('bimProduct', 'productParse')
# print(scrapyda.job_status('bimProduct', project))
# scrapyda.cancel('bimProduct', project)

# print(scrapyda.list_projects())
# scrapyda.delete_project('bimProduct')
# print(scrapyda.list_projects())
# print(scrapyda.list_spiders('bimProduct'))
# scrapyd-deploy bimProduct

scrapyda.delete_project('bimProduct')