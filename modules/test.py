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


df = pd.read_csv('./lol/yago.csv')

df['date'] =  pd.to_datetime(df['date'], format='%Y-%m-%d')

print()