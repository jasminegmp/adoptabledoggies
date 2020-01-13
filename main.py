from petfinderapi import DogFinder
from zipcodeapi import ZipcodeExtractor
import pandas as pd
from pandas import DataFrame
from pandas.io.json import json_normalize
import pickle
import numpy as np
from time import sleep
import os

def get_breed_count(r_filename, w_filename):
    # Pull data from .pkl files
    unpickled_df = pd.read_pickle(r_filename + ".pkl")
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

    unpickled_breeds.to_pickle(w_filename + '.pkl')
    unpickled_breeds = unpickled_breeds.sort_values(by=['count'], ascending=False)
    unpickled_breeds.to_csv(w_filename + '.csv', index=False, encoding='utf-8')


def get_data_zipcode(zp):
    zipcode = ZipcodeExtractor()
    z_df = zipcode.get_california()
    z_df.to_pickle('z_df.pkl')
    #print z_df
    df = DogFinder()
    for index, row in z_df.iterrows():
        if row['zip'] >= zp:
            print(row['zip'])
            zipcode = row['zip']
            animals = df.adoptable_pets(location = str(zipcode), distance = 3)
            pkl_folder_path = './zipcode_pkl/' + str(zipcode) + '.pkl'
            csv_folder_path = './zipcode_csv/' + str(zipcode) + '.csv'
            animals.to_pickle(pkl_folder_path)
            animals.to_csv(csv_folder_path, index=False, encoding='utf-8')
            sleep(5)


def get_data_specific_zipcode(zipcode):
    print zipcode

    df = DogFinder()
    animals = df.adoptable_pets(location = str(zipcode), distance = 3)
    animals.to_pickle(str(zipcode) + '.pkl')
    animals.to_csv(str(zipcode)+ '.csv', index=False, encoding='utf-8')

def append_dataframes(w_filename):
    df = DataFrame()
    for filename in os.listdir("./test_pkl"):
        if filename.endswith(".pkl"):
            print filename
            read_df = pd.read_pickle("./test_pkl/" + filename)
            df = df.append([read_df])
    # Removing all duplicate rows
    df = df.drop_duplicates(subset ="animal_id", keep = 'first')
    #df.to_pickle("cleaned.pkl")
    df.to_pickle(w_filename + ".pkl")
    print df
    return df


#get_data_specific_zipcode(90015)
#get_data_zipcode(90074)

df = append_dataframes("90001_90083")
get_breed_count("90001_90083", "90001_90083_breed_count")





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





