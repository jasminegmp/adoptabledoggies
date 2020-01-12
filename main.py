from petfinderapi import DogFinder
from zipcodeapi import ZipcodeExtractor
import pandas as pd
from pandas import DataFrame
from pandas.io.json import json_normalize
import pickle
import numpy as np

def datamine():
    # Pull data from .pkl files
    df = DogFinder()
    unpickled_df = pd.read_pickle("50miles.pkl")
    unpickled_breeds = pd.read_pickle("breeds.pkl")
    #print unpickled_df
    #print unpickled_breeds

    # simplify df to only have columns: breeds.mixed, breeds.primary, breeds.secondary, contact.address.postcode, age, gender, size, published_at, status_changed_at
    breed_df = unpickled_df[['breeds.mixed','breeds.primary', 'breeds.secondary', 'contact.address.postcode', 'age', 'gender', 'size', 'published_at', 'status_changed_at']]

    # add a count to breeds df
    unpickled_breeds["count"] = 0

    for col in breed_df:
        if col == 'breeds.mixed':
            continue # for now
        if (col == 'breeds.primary' or col == 'breeds.secondary'):
            for i, row_value in breed_df[col].iteritems():
                if not(pd.isnull(row_value)):
                    #print row_value
                    unpickled_breeds['count'] += unpickled_breeds['name'].str.contains(row_value).astype(int)
                
        if col == 'contact.address.postcode':
            continue # for now

    unpickled_breeds.to_pickle('breedcount_50miles.pkl')
    unpickled_breeds = unpickled_breeds.sort_values(by=['count'], ascending=False)
    unpickled_breeds.to_csv(r'breedcount.csv', index=False, encoding='utf-8')

# Count number of primary breeds and add count to breeds


# Find all dogs within 50 miles of zipcode 92620
#zipcode = 92620
#distance = 50
#df = DogFinder()
#animals = df.adoptable_pets(location = '92620', distance = 2)
#animals.to_pickle('test.pkl')
#print animals

# get list of breeds
#breeds = df.get_breeds()
#breeds.to_pickle('breeds.pkl')
#print breeds

zipcode = ZipcodeExtractor()
z_df = zipcode.get_california()
z_df.to_pickle('z_df.pkl')
print z_df





