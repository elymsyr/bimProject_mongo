#DATABASE SETTINGS
DATABASE = 'bim'
COLLECTION = 'bim-new'
CLUSTER = 'mongodb+srv://admin0:aqwer1234@bim.0xndej5.mongodb.net/'
SELECTORS = ['p_id', 'name', 'category', 'subcategory', 'url', 'images', 'direct_link', 'brand', 'votes', 'rating', 'tech-spec', 'specification', 'description', 'related', 'classification','properties']

#FOLDER PATHS
MAIN_DATAS = 'docs/product_data.txt'
DOWNLOAD_FOLDER = 'C:\\Users\\orhun\\OneDrive\\Belgeler\\Github Repo\\bimObject\\Include\\BimDownloaded'
DOWNLOAD_LOG = 'docs/download_log.txt'
MONGO_LOG = 'docs/mongo_log.txt'
UPDATE_LOG = 'docs/update_log.txt'
FOR_MAIN_DATAS = 'docs/main_data_storage.txt'
SECOND_DATAS = 'docs/new_data_storage.txt'

RESET_DRIVE_EVERY_ = 20
# Item scope to write log
LIST_SCOPE = [0,10]

# Driver Number to run at the same time
MULTIQUEUE_NUMBER = 3
# Wait time for a product document to download. (a*2) -> waits a seconds, if the file was detected as still downloading, wait for a*2 seconds
SLEEP_BREAK = 40*2
# Get max number of items to update through the execute of the script
MAX_NUMBER_AT_A_TIME = 99999

# Wait time for page to load 
TIMEOUT = 10