from petfinderapi import DogFinder
from zipcodeapi import ZipcodeExtractor
from featuremining import *
from featureselectiontransformation import *
from featurecleaningandintegration import *
import pandas as pd
from pandas import DataFrame
from pandas.io.json import json_normalize
import pickle
import numpy as np
from time import sleep
import os

def read_pkl(r_filename, columns):
    # Pull data from .pkl files
    df = pd.read_pickle(r_filename + ".pkl")
    df = df[columns]
    return df    

def write_pkl(df, w_filename):
    df.to_pickle(w_filename + '.pkl')

def write_csv(df, w_filename):
     df.to_csv(w_filename + '.csv', index=False, encoding='utf-8')

def get_breed_count(r_filename, w_filename):
    print "Getting breed count..."

    # Pull data from .pkl files
    breed_df = read_pkl(r_filename, ['breeds.mixed','breeds.primary', 'breeds.secondary', 'contact.address.postcode', 'age', 'gender', 'size', 'published_at', 'status_changed_at'])
    unpickled_breeds = pd.read_pickle("breeds.pkl")

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

    write_pkl(unpickled_breeds, w_filename)

    unpickled_breeds = unpickled_breeds.sort_values(by=['count'], ascending=False)

    write_csv(unpickled_breeds, w_filename)
   
def get_gender_count(r_filename, w_filename):
    print "Getting gender count..."

    # Pull data from .pkl file
    gender_df = read_pkl(r_filename, ['gender'])

    # create dataframe for gender
    gender_initial = [['Female', 0], ['Male', 0]] 
    gender_count_df = DataFrame(gender_initial, columns=['gender', 'count'])

    gender_count_df["count"] = 0
    #print gender_count_df
    for i, row_value in gender_df['gender'].iteritems():
        #print row_value
        gender_count_df['count'] += gender_count_df['gender'].str.contains(row_value).astype(int)
    
    write_pkl(gender_count_df, w_filename)
    write_csv(gender_count_df, w_filename)

def get_age_count(r_filename, w_filename):
    print "Getting age count..."

    # Pull data from .pkl file
    age_df = read_pkl(r_filename, ['age'])

    # create dataframe for gender
    age_initial = [['Senior', 0], ['Adult', 0], ['Young', 0], ['Baby', 0]] 
    age_count_df = DataFrame(age_initial, columns=['age', 'count'])

    age_count_df["count"] = 0
    #print gender_count_df
    for i, row_value in age_df['age'].iteritems():
        #print row_value
        age_count_df['count'] += age_count_df['age'].str.contains(row_value).astype(int)
    
    write_pkl(age_count_df, w_filename)
    write_csv(age_count_df, w_filename)

def get_size_count(r_filename, w_filename):
    print "Getting size count..."

    # Pull data from .pkl file
    size_df = read_pkl(r_filename, ['size'])

    # create dataframe for gender
    size_initial = [['Small', 0], ['Medium', 0], ['Large', 0], ['Extra Large', 0]] 
    size_count_df = DataFrame(size_initial, columns=['size', 'count'])

    size_count_df["count"] = 0
    #print gender_count_df
    for i, row_value in size_df['size'].iteritems():
        #print row_value
        size_count_df['count'] += size_count_df['size'].str.contains(row_value).astype(int)
    
    write_pkl(size_count_df, w_filename)
    write_csv(size_count_df, w_filename)

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
    
    df.to_pickle(w_filename + ".pkl")
    print df
    return df

    
def input_script():
    option = input("1. Grab Data\n2. get count\n3. Random forest\n")
    print(option)
    if (option == 1):
        zipcode = input("Starting zipcode?\n")
        print zipcode
        get_data_zipcode(zipcode)
    if (option == 2):
        get_count_opt = input("21. breed count \n22. gender count \n23. age count \n24.size_count\n")
        print(get_count_opt)
        if (get_count_opt ==  21):
            get_breed_count("./90001_90083_test/90001_90083", "./90001_90083_test/90001_90083_breed_count")
        if (get_count_opt == 22):
            get_gender_count("./90001_90083_test/90001_90083", "./90001_90083_test/90001_90083_gender_count")
        if (get_count_opt == 23):
            get_age_count("./90001_90083_test/90001_90083", "./90001_90083_test/90001_90083_age_count")
        if (get_count_opt == 24):
            get_size_count("./90001_90083_test/90001_90083", "./90001_90083_test/90001_90083_size_count")
    if (option == 3):
        random_forest_feature_importance("./90001_90083_test/90001_90083_nominal", "./90001_90083_test/90001_90083_nominal_results")



#get_data_specific_zipcode(90015)
#df = append_dataframes("90001_90083")
#get_categorical_data("./90001_90083_test/90001_90083", "./90001_90083_test/90001_90083_categorical")
#get_data("./90001_90083_test/90001_90083", "./90001_90083_test/90001_90083_nominal")


#get_data_zipcode(92106)
#
input_script()


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

