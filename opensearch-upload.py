from opensearchpy import OpenSearch
from genericpath import isfile
import json
import os
import time

## Two types of comments:
#### FIXME: something is broken; should be addressed and removed.
#### LEAVE-IN: equivalent of "Do not erase" on a chalk board.

## Create host / auth and connect
## Note: auth in clear text, doing this because demo only.
host = 'steam-opensearch-agirlhasnona-9c3f.aivencloud.com'
port = 24022
auth = ('avnadmin', 'AVNS_bOSb2v_0fk5tzLhAtQb') 

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

## Create records
## Important: after a bunch of research for "what" issues,
####    discovered that _bulk requires the JSON document to
####    be newline delimited.

## Format Payload and Upload
#### Using "index" which is "create or replace",
####    "create" is create only.
create_or_replace={
    "index": {
        "_index": index_name
    }
}

#### Hard coding start path for now
startpath = 'data/steam_dataset/'

#### Steps in the loops:
#### 1. Walk from root and find all directories and files
#### 2. For JSON files only do:
####     - append the source file name.extension
####     - make newline delimited JSON
####     - upload record
####     - rinse, repeat all records in dataset
for root, dirs, files in os.walk(startpath, topdown=False):
   for name in files:
      #LEAVE-IN: troubleshooting
      #print(os.path.join(root, name))
      if name.endswith("json"):
         ## grabbing only the JSON files
        f = open(os.path.join(root,name), 'r')
        data = json.load(f)
        name_of_source_file = {"source": name}
        for key,value in data.items():
          # Combine the two dict type with a formatted string literal
          # And add the "what to do" with the payload
          #value_with_source = f'{value} {name_of_source_file}'
          value_with_source = value | name_of_source_file
          #print(key, "value is:\n", value_with_source)
          ## now need to make newline delimited JSON payload
          #payload = json.dumps(create_or_replace) + "\n" + json.dumps(value_with_source) + "\n"
          #LEAVE-IN: troubleshooting
          #print(payload)
          try:
            response = osClient.index(index = index_name, body = json.dumps(value_with_source), refresh = True)
          except:
            time.sleep(5)
            response = osClient.index(index = index_name, body = json.dumps(value_with_source), refresh=True)
          #response=osClient.bulk(body=json.loads(payload),index=index_name)
          print(response)
        f.close()
   #for name in dirs:
      #LEAVE-IN: troubleshooting
      #print(os.path.join(root, name))


## Notes
## 1. Connect to OpenSearch
## 2. Create index
## 3. ...
## 4. Profit, lol
