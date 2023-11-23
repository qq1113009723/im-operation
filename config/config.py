import configparser
import json

# Initialize the ConfigParser
config = configparser.ConfigParser()
config.read('config/config-test.ini')
# MongoDB setup
MONGO_URI = config.get('mongodb', 'mongo_uri')
MONGO_DATABASE_NAME = config.get('mongodb', 'database_name')
# Append the database name to the URI
MONGO_URI = f"{MONGO_URI}{MONGO_DATABASE_NAME}"

# MONGO_COLLECTION_NAME = config.get('mongodb', 'collection_name')
# MongoDB query configuration
# Parse the JSON string from the config file into a Python dictionary
# MONGO_COLLECTION_QUERY = json.loads(config.get('db_query', 'mongo_query'))

## query datasource
DB_QUERIES = {
    'accounts_query': json.loads(config.get('db_queries', 'accounts_query')),
    'groups_query': json.loads(config.get('db_queries', 'groups_query')),
    'group_ids_query': json.loads(config.get('db_queries', 'group_ids_query')),
    'accounts_delete_query': json.loads(config.get('db_queries', 'accounts_delete_query')),
}

# im
IM_APIS = {
    'account_import' : config.get('im_api_urls','account_import'),
    'account_delete':config.get("im_api_urls",'account_delete'),
    'create_group' : config.get('im_api_urls','create_group'),
    'add_group_member' : config.get('im_api_urls','add_group_member')
}
IM_CONFIG = {
    'sdk_app_id':config.get('im', 'sdk_appid'),
    'secret_key':config.get('im', 'secret_key'),
    'admin_account':config.get('im', 'admin_account')
}
