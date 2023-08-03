# bimProject_mongo

## Description

Crawling product data from 'bimObject.com' by using selenium and scrapy.

## Getting Started

### Dependencies

* requirements.txt ('pip install -r requirements.txt')

### Installing

* Only fork this repository. Remember to change DOWNLOAD_FOLDER, CLUSTER and DB Settings in [var.py](bimproduct.com/docs/var.py)

### Executing program

* Open path/to/bimproduct.com in the terminal.
  * See commands:
```
py main.py -h 
```
* Use gui.py to run it as a script.
* 'scrapyd' can be used only for running spiders

## Using Repo from Zero
There are 5 main functions:
  * Find products
  * Parse products
  * Update Products
  * Download Products
  * Check Compatibilities and Errors
<br>Spiders are the main functions to find and parse all the products. Updating and downloading necessary items from the web and updating the database are done by two scripts in the docs file.
### Spiders:
* **productParse**: Uses URLs that were found before to parse product data and write data to Mongo DB.
* **urlExtractor**: Takes any number of product URLs and using them, finds other products.
* **urlExtract**: Uses category links as a start to provide URL links to *urlExtractor*.
<br>***Scrapyd*** can be used to run spiders. [Check how to do it!]([url](https://scrapeops.io/python-scrapy-playbook/extensions/scrapy-scrapyd-guide/))
### Update and Download:
* **Download**:
  * Run 'download_propuct.py' as a script. Choose one doc to download using its ID or enter 0 to download all items in DB.
  * Use GUI by running 'gui.py' as a script. Choose one doc to download using its ID or enter 0 to download all items in DB.
  * Enter cmd 'path/to/python.exe path/to/main.py -d' to run 'download_propuct.py' as a script.
* **Update**:
  * Run 'update_comp.py' as a script.
  * Use GUI by running 'gui.py' as a script.
  * Enter cmd 'path/to/python.exe path/to/main.py -u' to run 'update_comp.py' as a script.
### Check Compatibilities:
* **check_functions.py (py main.py -c):** 
  * main_check: checks MAIN_DATAS for URL compatibilities
  * check_hunted: checks database for any ID or URL that may cause an error
  * get_list/lister/hard_clear: checks downloads and correct download_states

## Other Docs
* var.py: all important variables
* update_comp_old.py: Updates 'properties' and 'images' parts of products in the database
* get_access_..._guest.py: Get data from my database as a guest.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

 - [github](https://github.com/elymsyr)
 - mail: orhun868@gmail.com
