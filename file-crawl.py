# import required module
from genericpath import isfile
import os
# assign directory
startpath = 'data/steam_dataset/'

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
         value_with_source = f'{value} {name_of_source_file}'
         #print(key, "value is:\n", value_with_source)
         ## now need to make newline delimited JSON payload
         payload = json.dumps(create_or_replace) + "\n" + json.dumps(value_with_source) + "\n"
         print(payload)
         f.close()
   #for name in dirs:
      #LEAVE-IN: troubleshooting
      #print(os.path.join(root, name))
