import pandas as pd
from pandas import DataFrame
from pandas.io.json import json_normalize
import pickle
import numpy as np
import os
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder

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
        
