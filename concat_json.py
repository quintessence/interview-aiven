import json
#import pandas as pd

document1 = {
    "source": "a data source"
}

document2 = {
    "title": "Apollo 13",
    "director": "Richie Cunningham",
    "year": "1994"
}

MergeJSON = document2 | document1

print(MergeJSON)