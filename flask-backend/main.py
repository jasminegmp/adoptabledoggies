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
import json


def read_pkl(r_filename, columns):
    # Pull data from .pkl files
    df = pd.read_pickle(r_filename + ".pkl")
    df = df[columns]
    return df    

def write_pkl(df, w_filename):
    df.to_pickle(w_filename + '.pkl')

def write_csv(df, w_filename):
     df.to_csv(w_filename + '.csv', index=False, encoding='utf-8')

def list_of_breeds(pkl_filename, w_filename):
    print "Getting list of available breeds according to data mined..."

    # Pull data from .pkl files
    breed_df = read_pkl(pkl_filename, ['breeds.primary', 'breeds.secondary'])

    # append breed primary and secondary
    breed_df['breeds.primary'].append(breed_df['breeds.secondary']).reset_index(drop=True)
    del breed_df['breeds.secondary']

    # Removing all duplicate rows
    breed_df = breed_df.drop_duplicates(subset ="breeds.primary", keep = 'first')

    #sort by breed
    breed_df = breed_df.sort_values(by=['breeds.primary'], ascending=True)

    write_pkl(breed_df, w_filename)
    write_csv(breed_df, w_filename)

def list_of_zipcodes(pkl_filename, w_filename):
    print "Getting list of availalbe zipcodes according to data mined..."

    # Pull data from .pkl files
    zipcode_df = read_pkl(pkl_filename, ['contact.address.postcode'])

    # Removing all duplicate rows
    zipcode_df = zipcode_df.drop_duplicates(subset ="contact.address.postcode", keep = 'first')

    #sort by zipcode
    zipcode_df = zipcode_df.sort_values(by=['contact.address.postcode'], ascending=True)

    write_pkl(zipcode_df, w_filename)
    write_csv(zipcode_df, w_filename)

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
    for filename in os.listdir("./zipcode_pkl"):
        if filename.endswith(".pkl"):
            print filename
            read_df = pd.read_pickle("./zipcode_pkl/" + filename)
            df = df.append([read_df])

    # Removing all duplicate rows
    df = df.drop_duplicates(subset ="animal_id", keep = 'first')
    
    df.to_pickle(w_filename + ".pkl")
    print df
    return df

def datamine_zipcode(zipcode):
    print "Getting df for " + zipcode

    # Pull data from main pkl file
    df = read_pkl("./storage/socal_pkl", ['breeds.primary', 'breeds.secondary', 'age', 'size', 'contact.address.postcode', 'gender'])

    df = df.loc[df['contact.address.postcode'] == zipcode]

    write_pkl(df, "./storage/" + zipcode)
    write_csv(df,  "./storage/" + zipcode)
    
def iterate_zipcodes():
    print "Getting zipcodes."

    # Pull data from .pkl files
    zipcode_df = read_pkl('./storage/zipcodes', ['contact.address.postcode'])
    
    for index, row in zipcode_df.iterrows():
        print(row['contact.address.postcode'])
        datamine_zipcode(str(row['contact.address.postcode']))
    
def input_script():
    option = input("1. Grab Data\n2. get count\n3. Random forest\n4. Test for D3")
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

# map zipcodes to counties and create csv for each county
def map_zipcode_to_county(r_folder, w_folder):
    print "Getting zipcodes available."

    # Pull data from .pkl files
    zipcode_df = read_pkl(r_folder+'/zipcodes', ['contact.address.postcode'])
    
    # grab just california zipcodes and its county name
    data = pd.read_csv(r_folder + "/uszips.csv")
    df = data[['zip','state_id', 'county_name']]
    ca_df = df.loc[df['state_id'] == 'CA']
    #print ca_df

    # loop through each zipcode_df and map a county_name
    for col in zipcode_df:
        if (col == 'contact.address.postcode'):
            for i, row_value in ca_df['zip'].iteritems():
                print row_value, ca_df['county_name'][i]
                # find open matching pkl file
                if os.path.isfile(r_folder + "/" + str(row_value)+ ".pkl"):
                    match_zipcode_df = read_pkl(r_folder + "/" + str(row_value), ['breeds.primary', 'breeds.secondary', 'age', 'size', 'contact.address.postcode', 'gender'])
                    # add a county_name to match_zipcode_df
                    match_zipcode_df["county_name"] = ca_df['county_name'][i]
                    write_pkl(match_zipcode_df, w_folder + "/" + str(ca_df['county_name'][i]) + "/" + str(row_value))
                    write_csv(match_zipcode_df, w_folder + "/" + str(ca_df['county_name'][i]) + "/" + str(row_value))



def integrate_counties(folder_location, county_name):
    print "Getting all zipcodes in county."
    pkl_files = [f for f in os.listdir(folder_location) if f.endswith('.pkl')]
    county_df = pd.DataFrame()
    for f in pkl_files:
        print f
        df = pd.read_pickle(folder_location + f)
        county_df = pd.concat([county_df, df])
    #print county_df
    write_csv(county_df, folder_location + county_name)
    





#get_data_specific_zipcode(90015)
#df = append_dataframes("socal_pkl")
#get_categorical_data("./90001_90083_test/90001_90083", "./90001_90083_test/90001_90083_categorical")
#get_data("./90001_90083_test/90001_90083", "./90001_90083_test/90001_90083_nominal")

#list_of_zipcodes("./storage/socal_pkl", "./storage/zipcodes")
#list_of_breeds("./storage/socal_pkl", "./storage/breeds")

#unpickled_zipcodes = pd.read_pickle("zipcodes.pkl")
#console.log(unpickled_zipcodes)
#input_script()

#datamine_zipcode(90001)
#iterate_zipcodes()
#map_zipcode_to_county("./cleaned_zipcode_pkl", "./cleaned_county_csv")

integrate_counties("./cleaned_county_csv/Ventura/", "Ventura")