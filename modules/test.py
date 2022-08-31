from functools import reduce
import pandas as pd
import time
import re

t0 = time.time()

categories = {
    "food": [
        "Lupa",
        "Mercadona",
        "Mcdonald",
        "Bazar"
    ],
    "transfers": [
        "Bizum"
    ],
    "credit_card": [
        "Contactless"
    ],
    "parking": [
        "Parking"
    ],
    "suscriptions": [
        "HBO Max"
    ]
}


_list = pd.read_csv('./lol/yago.csv')['description']
category = "Mercadona"

def dict_walker(_dict: dict, pre = None):
    pre = pre if pre else []
    
    if isinstance(_dict, dict):
        for key, value in _dict.items():
            if isinstance(value, dict):
                for d in dict_walker(value, pre + [key]):
                    yield d
                
            elif isinstance(value, list) or isinstance(value, tuple):
                for i, v in enumerate(value):
                    for d in dict_walker(v, pre + [key, i]):
                        yield d
                
            else:
                yield pre + [key, value]
                
    else:
        yield pre + [_dict]

# Gets a tree of paths of the dict and chooses the one that we need
# It uses a generator for better performance
for i in dict_walker(categories):
    if category in i:
        if category == i[-1]:
            category = i[:-1]
        
        else:
            idx = i.index(category)
            category = i[:idx + 1]
        break

# Now we create a copy of the categories to remove every key / value
# that we don't need
_dict = categories.copy()

for i in range(len(category)):
    sub_dict = reduce(lambda x, y: x[y], category[:i], _dict)
    if isinstance(sub_dict, dict):
        keys = list(sub_dict.keys())
        keys.remove(category[i])
        for key in keys:
            sub_dict.pop(key)
            
    elif isinstance(sub_dict, list) or isinstance(sub_dict, tuple):   
        items = sub_dict.copy()     
        items.pop(category[i])
        for item in items:
            sub_dict.remove(item)
        
# Finally we perform a regular expression search using the terms
for path in dict_walker(_dict):
    path, sub_string = path[:-1], path[-1]
    matches = []
    
    sub_dict = reduce(lambda x, y: x[y], path[:-1], _dict)
    sub_dict[sub_dict.index(sub_string)] = {sub_string: matches}

    for item in _list:
        match = re.search(f'(?i){sub_string}', item)
        
        if match:
            matches.append(item)

t1 = time.time()
print(_dict)
print(t1 - t0)