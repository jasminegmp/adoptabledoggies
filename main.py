from petfinderapi import DogFinder
from zipcodeapi import ZipcodeExtractor
import pandas as pd
from pandas import DataFrame
from pandas.io.json import json_normalize
import pickle
import numpy as np
from time import sleep
import os
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder

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

def get_categorical_data(r_filename, w_filename):
    categorical_df = read_pkl(r_filename, ['attributes.house_trained', 'attributes.shots_current', 'attributes.spayed_neutered', 'attributes.special_needs', 'breeds.mixed', 'breeds.unknown', 'gender', 'status'])
    
    # modify data so that everything is true and false

    # Female - false, Male - true
    for i, row_value in categorical_df['gender'].iteritems():
        if row_value == 'Female':
            categorical_df.at[i, 'gender'] = False
        if row_value == 'Male':
            categorical_df.at[i, 'gender'] = True

    # adopted - false, adoptable - true
    for i, row_value in categorical_df['status'].iteritems():
        if row_value == 'adopted':
            categorical_df.at[i, 'status'] = 0
        if row_value == 'adoptable':
            categorical_df.at[i, 'status'] = 1

    #print categorical_df
    write_pkl(categorical_df, w_filename)
    write_csv(categorical_df, w_filename)

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

def get_ratio(df):
    print "Getting ratio to oversample adopted data..."
    [adoptable_ratio, adopted_ratio] = df['status'].value_counts()
    return adopted_ratio, adoptable_ratio

def random_forest_feature_importance(r_filename, w_filename):
    print "Finding important features..."

    # Pull data from .pkl file with just categorical data
    df = pd.read_pickle(r_filename + ".pkl")

    adopted_ratio, adoptable_ratio = get_ratio(df)
    #print adopted_ratio, adoptable_ratio

    #print categorical_df
    # x - attributes, y labels
    X = df.iloc[:, df.columns != 'status'].values
    y = df.iloc[:, df.columns == 'status'].values


    # split data into training and testing set
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)
    print X_train, y_train

    X_train = X_train.astype('int')
    X_test = X_test.astype('int')
    y_train = y_train.astype('int')
    y_test = y_test.astype('int')

    # train algorithm
    ## This line instantiates the model. 
    #rf = RandomForestClassifier()
    rf = RandomForestClassifier(bootstrap=True,
            class_weight= dict({False:adopted_ratio, True:adoptable_ratio}), 
            criterion='gini',
            max_depth=4, max_features='auto', max_leaf_nodes=None,
            min_impurity_decrease=0.0, min_impurity_split=None,
            min_samples_leaf=4, min_samples_split=10,
            min_weight_fraction_leaf=0.0, n_estimators=300,
            oob_score=False,
            verbose=0, warm_start=False)

    ## Fit the model on your training data.
    rf.fit(X_train, y_train.ravel())

    feature_names = list(df.columns.values)
    for feature in zip(feature_names, rf.feature_importances_):
        print(feature)
        


#get_data_specific_zipcode(90015)
#get_data_zipcode(92106)
#df = append_dataframes("90001_90083")
#get_breed_count("./90001_90083_test/90001_90083", "./90001_90083_test/90001_90083_breed_count")
#get_gender_count("./90001_90083_test/90001_90083", "./90001_90083_test/90001_90083_gender_count")
#get_age_count("./90001_90083_test/90001_90083", "./90001_90083_test/90001_90083_age_count")
#get_size_count("./90001_90083_test/90001_90083", "./90001_90083_test/90001_90083_size_count")
#get_categorical_data("./90001_90083_test/90001_90083", "./90001_90083_test/90001_90083_categorical")
#get_data("./90001_90083_test/90001_90083", "./90001_90083_test/90001_90083_nominal")
random_forest_feature_importance("./90001_90083_test/90001_90083_nominal", "./90001_90083_test/90001_90083_nominal_results")
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

