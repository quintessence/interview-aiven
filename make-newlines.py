import os
import json

document1 = {
    "title": "Moneyball",
    "director": "Bennett Miller",
    "year": "2011"
}

document2 = {
    "title": "Apollo 13",
    "director": "Richie Cunningham",
    "year": "1994"
}

data = [document1, document2]

index = "test_index"

action={
    "index": {
        "_index": index
    }
}

def payload_constructor(data,action):
    # "All my own work"

    action_string = json.dumps(action) + "\n"

    payload_string=""

    for datum in data:
        payload_string += action_string
        this_line = json.dumps(datum) + "\n"
        payload_string += this_line
        print(payload_string,"\n")
    return payload_string

payload_constructor(data,action)
#print(payload_constructor(data,action))