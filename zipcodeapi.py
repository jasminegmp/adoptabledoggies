import pandas as pd
import numpy as np

# Created class based on https://github.com/aschleg/petpy/blob/master/petpy/
class ZipcodeExtractor(object):
    def __init__(self):
        df = pd.read_csv('zip_code_database.csv')
        # Only need zipcode, city name, state, and county
        df = df[['zip','primary_city', 'state', 'county']]
        self.df = df

    def get_california(self):
        return self.df.loc[self.df['state'] == 'CA']
