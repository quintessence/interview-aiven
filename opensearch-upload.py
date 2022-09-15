from opensearchpy import OpenSearch
import json
import os
import time

## Notes
## 1. Connect to OpenSearch
## 2. Create index
## 3. ...
## 4. Profit, lol

## Create host / auth and connect
## Note: auth in clear text, doing this because demo only.
host = 'HOST' # FIXME hardcoded host, edit to your values
port = 24022
auth = ('USER', 'PASSWORD') # FIXME hardcoded user/pass, see above caveat, edit

osClient = OpenSearch(
    hosts = [{'host': host, 'port': port}],
    http_compress = True,
    http_auth = auth,
    use_ssl = True,
    verify_certs = True,
    ssl_assert_hostname = False,
    ssl_show_warn = False
)

## Create the index for the Steam data
index_name = 'steam-data-index-8'
index_body = {
  'settings': {
    'index': {
      'number_of_shards': 4
    }
  }
}
response = osClient.indices.create(index_name, body=index_body)
print('\nCreating index:')
print(response)


## Format Payload and Upload
#### Using "index" which is "create or replace",
####    "create" is create only.
#### This is for the to-be-fixed bulk uploads
create_or_replace={
    "index": {
        "_index": index_name
    }
}

#### Steps in the loops to upload data:
#### 1. Walk from root and find all directories and files
#### 2. For JSON files only do:
####     - append the source file name.extension
####     - upload record
####     - rinse, repeat all records in dataset
####     - rinse, repeat all JSON files in directory tree
startpath = 'data/steam_dataset/'   # FIXME - hardcoded startpath, edit to your values
for root, dirs, files in os.walk(startpath, topdown=False):
   for name in files:
      if name.endswith("json"):
         ## grabbing only the JSON files
        f = open(os.path.join(root,name), 'r')
        data = json.load(f)
        name_of_source_file = {"source": name}
        for key,value in data.items():
          value_with_source = value | name_of_source_file
          try:
            response = osClient.index(index = index_name, body = json.dumps(value_with_source), refresh = True)
          except:
            time.sleep(5)
            response = osClient.index(index = index_name, body = json.dumps(value_with_source), refresh=True)
            #response= = osClient.bulk(body=json.loads(payload),index=index_name) ### To be fixed bulk upload
          print(response)
        f.close()