# bimProject_mongo

## Description

Crawling product data from 'bimObject.com' by using selenium and scrapy.

## Getting Started

### Dependencies

* requirements.txt ('pip install -r requirements.txt')

### Installing

* Only fork this repository.

### Executing program

* Open path/to/bimproduct.com in the terminal.
  * See commands:
```
py main.py -h 
```
* Use gui.py to run it as a script.
* 'scrapyd' can be used only for running spiders

## Docs

* check_functions.py (py main.py -c): 
  * main_check: checks MAIN_DATAS for URL compatibilities
  * check_hunted: checks database for any ID or URL that may cause an error
  * get_list/lister/hard_clear: checks downloads and corrected download_states
* download_product.py (py main.py -d): Gets URLs from database and downloads data
* update_comp.py (py main.py -u): Updates 'properties' and 'images' parts of products in database
* var.py: all important variables  

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

 - [github](https://github.com/elymsyr)
 - mail: orhun868@gmail.com
