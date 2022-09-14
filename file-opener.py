import json

parent_directory = 'data/steam_dataset/appinfo/store_data/'
file_data = 'steam_store_data-two-elements.json'

## Create the index for the Steam data
index_name = 'steam-data-index'
index_body = {
  'settings': {
    'index': {
      'number_of_shards': 4
    }
  }
}
### Uncomment this is the index creation
#response = osClient.indices.create(index_name, body=index_body)
#print('\nCreating index:')
#print(response)

## Create records
## Important: after a bunch of research for "what" issues,
####    discovered that _bulk requires the JSON document to
####    be newline delimited.

## Create Creator
#### Using "index" which is "create or replace",
####    "create" is create only.

create_or_replace={
    "index": {
        "_index": index_name
    }
}


f = open(parent_directory+file_data, 'r')

data = json.load(f)
name_of_source_file = {"source": file_data}

for key,value in data.items():
    # Combine the two dict type with a formatted string literal
    # And add the "what to do" with the payload
    value_with_source = f'{value} {name_of_source_file}'
    #print(key, "value is:\n", value_with_source)

    ## now need to make newline delimited JSON payload
    payload = json.dumps(create_or_replace) + "\n" + json.dumps(value_with_source) + "\n"
    print(payload)
f.close()

## notes

## Step 1 - Open One Record
## Step 2 - Open Two Records
## Step 3 - Append Source to Each
## Step 4 - Two to N