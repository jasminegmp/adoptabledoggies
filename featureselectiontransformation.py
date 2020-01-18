import pandas as pd
from pandas import DataFrame
from pandas.io.json import json_normalize
import pickle
import numpy as np
import os

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

def categorical_to_numeric(x):
    if x==True:
        return 1
    if x==False:
        return 0

def get_data(r_filename, w_filename):
    df = read_pkl(r_filename, ['attributes.house_trained', 'attributes.shots_current', 'attributes.spayed_neutered', 'attributes.special_needs', 'age', 'gender', 'size', 'status'])
    df = read_pkl(r_filename, ['attributes.house_trained', 'attributes.shots_current', 'attributes.spayed_neutered', 'attributes.special_needs', 'status'])
    # modify data so all categorical attributes are nominal using One Hot Encoding
    # https://datascience.stackexchange.com/questions/32622/how-to-make-a-decision-tree-when-i-have-both-continous-and-categorical-variables
    # https://towardsdatascience.com/categorical-encoding-using-label-encoding-and-one-hot-encoder-911ef77fb5bd
  
    df['attributes.house_trained'] = df['attributes.house_trained'].apply(categorical_to_numeric)
    df['attributes.shots_current'] = df['attributes.shots_current'].apply(categorical_to_numeric)
    df['attributes.spayed_neutered'] = df['attributes.spayed_neutered'].apply(categorical_to_numeric)
    df['attributes.special_needs'] = df['attributes.special_needs'].apply(categorical_to_numeric)
    '''
    for i, row_value in df['gender'].iteritems():
        if row_value == 'Male':
            df.at[i, 'gender'] = 1
        if row_value == 'Female':
            df.at[i, 'gender'] = 0

    for i, row_value in df['status'].iteritems():
        if row_value == 'adopted':
            df.at[i, 'status'] = 0
        if row_value == 'adoptable':
            df.at[i, 'status'] = 1 

    for i, row_value in df['size'].iteritems():
        if row_value == 'Small':
            df.at[i, 'size'] = 1
        if row_value == 'Medium':
            df.at[i, 'size'] = 2
        if row_value == 'Large':
            df.at[i, 'size'] = 3
        if row_value == 'Extra Large':
            df.at[i, 'size'] = 4  
    

    for i, row_value in df['age'].iteritems():
        if row_value == 'Baby':
            df.at[i, 'age'] = 1
        if row_value == 'Young':
            df.at[i, 'age'] = 2
        if row_value == 'Adult':
            df.at[i, 'age'] = 3 
        if row_value == 'Senior':
            df.at[i, 'age'] = 4  
    
    # remove unknowns
    df['gender'] = pd.to_numeric(df['gender'], errors='coerce')
    df['status'] = pd.to_numeric(df['status'], errors='coerce')
    df['size'] = pd.to_numeric(df['size'], errors='coerce')
    df['age'] = pd.to_numeric(df['age'], errors='coerce')
    '''
    for i, row_value in df['status'].iteritems():
        if row_value == 'adopted':
            df.at[i, 'status'] = False
        if row_value == 'adoptable':
            df.at[i, 'status'] = True
    df['attributes.house_trained'] = pd.to_numeric(df['attributes.house_trained'], errors='coerce')
    df['attributes.shots_current'] = pd.to_numeric(df['attributes.shots_current'], errors='coerce')
    df['attributes.spayed_neutered'] = pd.to_numeric(df['attributes.spayed_neutered'], errors='coerce')
    df['attributes.special_needs'] = pd.to_numeric(df['attributes.special_needs'], errors='coerce')

    

    #print nominal_df
    write_pkl(df, w_filename)
    write_csv(df, w_filename)

