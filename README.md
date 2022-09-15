# Aiven Interview Project

The purpose of this project is to write a coding exercise for my 2022 interview with Aiven. Hooray!

Let's talk about the journey:

* v0 - The Zillow Bathtub Project: turns out getting Zillow to programmatically do what I want in order to surface the data I need to do this was more than the whole exercise. Harrumph! This is being migrated to a different project For A Later Time where I'll focusly solely on making the scraper work. Thus, no spoilers for any of the context for what this means.
* v1 - Go on Kaggle and get some NYC Bus Data, load it into Aiven's postgres offering and use Aiven's Grafana offering to build some dashboards. Drawback: this is a no-code solution to a coding exercise, so that won't do!
* v2 - The Final Version: I still want to write a way to scrape the data I need out of the Zillow API, but it turns out I'll also need a way to bulk load the data into OpenSearch whether the data is Zillow or any other source. This means that I'm focusing on bulk uploadig JSON files into the Aiven platform.

There are three segements to my write up here: the first will be the "public facing post" that I would write about as if it were a blog. The next is what I would be submitting if I were giving internal feedback on the process to a relevant team. And finally I'll have some of my initial thoughts on code in the GitHub repo.

Some context for the blog post that follows: I try to keep them in about 10 minutes of "reading time" as implementation is always a time consuming process in and of itself, so I don't want the reading portion to be a barrier.

---

# Uploading JSON Data into Aiven via Python

Hello everyone! Today I'll be talking about how to bulk upload data into Aiven for when you need to get data from files, rather than streams, into our amazing Aiven platform! If you would like to follow along here's what you'll need:

* A development environment with Python 3.x. There will be some specific notes on which verions of Python3 to use.
* An Aiven account - a free trial will work just fine!


## The Data: Kaggle

In order to get a suitably "large, but not _that_ large" data set I made use of Kaggle. The specific data set I used is [Steam Data by Souyama](https://www.kaggle.com/datasets/souyama/steam-dataset). The code we will be working with only requires JSON documents, the contents of the JSON objects does not matter.

## Aiven Configuration

In our platform, create an OpenSearch instance. To keep costs down while building a working proof of concept, please use the **Hobbyist** tier. You will find the higher / production-sized tiers will eat through your credits rapidly if you're using a free trial.

To configure the Hobbyist OpenSearch instance there are 5 steps:

1. Click "Create a Service" when you're in the Services View:<br />![Screenshot to create a service](images/aiven-create-service.png)

2. Select "OpenSearch" from the service list on the first step of the creation wizard:<br />![Screenshot to select OpenSearch from service list on Step 1](images/aiven-service-list.png)

3. Select a Cloud Provider for Step 2 on the creation wizard

4. Select the region you want/need to work in for Step 3

5. Select the **Hobbyist** tier for Step 4:<br />![Screenshot to select Hobbyist Tier on Step 4](images/aiven-hobbyist-tier.png)

6. Name your service as the final step!

Once your service is running, which should only take a few moments, we can start to interact with it.

## The Code 🐍

To keep a reference of the code, please keep [this repo](handy), which has the code itself and notes. The full code is here:

```python
from opensearchpy import OpenSearch
from genericpath import isfile
import json
import os
import time

## Notes
## 1. Connect to OpenSearch
## 2. Create index
## 3. ...
## 4. Profit, lol

host = 'HOST'
port = 24022
auth = ('USER', 'PASSWORD') 

osClient = OpenSearch(
    hosts = [{'host': host, 'port': port}],
    http_compress = True,
    http_auth = auth,
    use_ssl = True,
    verify_certs = True,
    ssl_assert_hostname = False,
    ssl_show_warn = False
)

index_name = 'steam-data-index'
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

startpath = 'data/steam_dataset/'

#### Steps in the loops to upload data:
#### 1. Walk from root and find all directories and files
#### 2. For JSON files only do:
####     - append the source file name.extension
####     - upload record
####     - rinse, repeat all records in dataset
####     - rinse, repeat all JSON files in directory tree
for root, dirs, files in os.walk(startpath, topdown=False):
   for name in files:
      ## grabbing only the JSON files
      if name.endswith("json"):
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
          print(response)
        f.close()
```

Let's review what each segment is doing.

The very, very first thing the code does, after importing all the necessary libraries that is, is connect to the OpenSearch instance. Since this is a demo environment this is done in clear text. _When using this code in a non-demo environment, including dev and staging in addition to prod, do not hard code your credentials in this way._

```python
host = 'HOST'
port = 24022
auth = ('USER', 'PASSWORD') 

osClient = OpenSearch(
    hosts = [{'host': host, 'port': port}],
    http_compress = True,
    http_auth = auth,
    use_ssl = True,
    verify_certs = True,
    ssl_assert_hostname = False,
    ssl_show_warn = False
)
```

The next thing we do is create the index that will be storing all of our JSON documents, and print some output to console to tell us if that was successful:

```python
index_name = 'steam-data-index'
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
```

Note that this code will error if you re-run the script after an index of that name is created. If you plan on running this code on the same index more than once, you should wrap that block in either a `try` or some other way to skip over the create once it exists. The error you will see will be similar to:

```
Traceback (most recent call last):
  File "/../interviews/aiven/opensearch-upload.py", line 36, in <module>
    response = osClient.indices.create(index_name, body=index_body)
  File "/opt/homebrew/lib/python3.10/site-packages/opensearchpy/client/utils.py", line 177, in _wrapped
    return func(*args, params=params, headers=headers, **kwargs)
  File "/opt/homebrew/lib/python3.10/site-packages/opensearchpy/client/indices.py", line 124, in create
    return self.transport.perform_request(
  File "/opt/homebrew/lib/python3.10/site-packages/opensearchpy/transport.py", line 407, in perform_request
    raise e
  File "/opt/homebrew/lib/python3.10/site-packages/opensearchpy/transport.py", line 368, in perform_request
    status, headers_response, data = connection.perform_request(
  File "/opt/homebrew/lib/python3.10/site-packages/opensearchpy/connection/http_urllib3.py", line 275, in perform_request
    self._raise_error(
  File "/opt/homebrew/lib/python3.10/site-packages/opensearchpy/connection/base.py", line 300, in _raise_error
    raise HTTP_EXCEPTIONS.get(status_code, TransportError)(
opensearchpy.exceptions.RequestError: RequestError(400, 'resource_already_exists_exception', 'index [steam-data-index/_u6FzketTCqqZAQB3dKTQw] already exists')
```

The most relevant portion of this error is the `400` followed by `resource_already_exists_exception` with the name of the resource.

**Now for the JSON documents themselves.**

As a reminder, this code needs to be able to grab one or more files from one or more subdirectories of a parent data directory. Since it is grabbing one or more files, I wanted to make sure to append what the file name of the specific data `source` is, which looks like this all together:

```python
startpath = 'data/steam_dataset/'

#### Steps in the loops to upload data:
#### 1. Walk from root and find all directories and files
#### 2. For JSON files only do:
####     - append the source file name.extension
####     - upload record
####     - rinse, repeat all records in dataset
####     - rinse, repeat all JSON files in directory tree
for root, dirs, files in os.walk(startpath, topdown=False):
   for name in files:
      ## grabbing only the JSON files
      if name.endswith("json"):
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
          print(response)
        f.close()
```

**Specific Versions of Python**

I mentioned earlier that which specific version of Python3.x you're using will matter and it actually has specifically to do with this line here:

```python
value_with_source = value | name_of_source_file
```

This concats to dictionaries together into one. This one line actually took a bit to suss out and the answer came via an expected mechanism - a [Stack Overflow post](https://stackoverflow.com/questions/38987/how-do-i-merge-two-dictionaries-in-a-single-expression). 

Succinctly, to merge dictionaries:
* In Python 3.9.0+ : `z = x | y`
* In Python 3.5.x+ : `z = {**x, **y}`
* In Python 3.4 and earlier, including Python2: you'll  need to write a method.

The Stack Overflow post itself isn't recent, originally published in 2008, but the responder who made the original version of the answer has been keeping it updated with a last update of only a few days ago! Amazing and greatly appreciated.


## What Next?

Now that you have your data uploaded into Aiven, you can start to use OpenSearch's built in visualization tools to do some initial analysis and surface additional information. You can search the data for how many games are from a particular genre, how many unique records were uploaded, and even what percentage of the data came from any particular source for a start!


---

## Internal Feedback



### Feedback - the No Code option
Separation of Concerns - people who understand the data might not understand the code to get the data into the product to just write an uploader. Having a tool (more flushed out) like this will help.

The individual upload: fails every 50-100 records (paste full error). That's why there's a try catch. Should never need to sleep in the code; however, my experience with the bulk uploader was that it was even more finnikcy than that, so getting something working was paramount. (All the more reason for the ability to upload the code.)