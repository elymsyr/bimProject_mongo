# bimProject_mongo

## Description

Crawling product datas from 'bimObject.com' by using selenium and scrapy.

## Getting Started

### Dependencies

* requirements.txt ('pip install -r requirements.txt')

### Installing

* Only fork this repository.

### Executing program

* Open path/to/bimproduct.com in terminal.
  * See commands:
```
py main.py -h 
```
* Use gui.py running it as script.
* scrapyd can be used only for running spiders

## Docs

* check_functions.py (py main.py -c): 
  * main_check : checks MAIN_DATAS for url compabilities
  * check_hunted : checks database for any ID or url that may cause an error
  * get_list/lister/hard_clear : checks downloads and corrected download_states
* download_product.py (py main.py -d): Gets urls from database and downloads datas
* update_comp.py (py main.py -u): Updates 'properties' and 'images' parts of products in database

## Version History

* 1.0.1
    * Variables were gathered in var.py
* 1.0
    *  Current Release
    * GUI and ReadME updated
        * main.py can be used from GUI now   
* 0.1
    * Initial Release

## License
...
<!-- This project is licensed under the [NAME HERE] License - see the LICENSE.md file for details -->

 - [github](https://github.com/elymsyr)
 - mail: orhun868@gmail.com
