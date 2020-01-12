
import requests
import os
from dotenv import load_dotenv
import pandas as pd
from urlparse import urljoin
from pandas import DataFrame
from pandas.io.json import json_normalize
import numpy as np

# Created class based on https://github.com/aschleg/petpy/blob/master/petpy/
class DogFinder(object):
    def __init__(self):
        load_dotenv(dotenv_path='petfinder.env')
        self.key = os.environ.get('KEY')
        self.secret = os.environ.get('SECRET')
        self._host = "http://api.petfinder.com/v2/"
        self._auth = self._authenticate()

    def _authenticate(self):
        print "Authenticating..."
        endpoint = 'oauth2/token'

        url = urljoin(self._host, endpoint)

        data = {
            'grant_type': 'client_credentials',
            'client_id': self.key,
            'client_secret': self.secret
        }
        
        r = requests.post(url, data=data)
        #print r.json()
        return r.json()['access_token']


    def _parameters(self, breed=None, size=None, gender=None, color=None, coat=None, animal_type=None, location=None,
                    distance=None, state=None, country=None, query=None, sort=None, name=None, age=None,
                    animal_id=None, organization_id=None, status=None, results_per_page=None, page=None):
   
        args = {
            'breed': breed,
            'size': size,
            'gender': gender,
            'age': age,
            'color': color,
            'coat': coat,
            'animal_type': animal_type,
            'location': location,
            'distance': distance,
            'state': state,
            'country': country,
            'query': query,
            'sort': sort,
            'name': name,
            'animal_id': animal_id,
            'organization_id': organization_id,
            'status': status,
            'limit': results_per_page,
            'page': page
        }

        args = {key: val for key, val in args.items() if val is not None}

        return args

    def _check_pages_api_limit(self, max_pages):
        if max_pages > 10000: # Limit for api calls per day
            ans = input('''Total pages requested is {} which exceeds the daily API requests quota by PetFinder,
                            do you want to limit the pages to 10,000 only? y|n '''.format(max_pages))
            if ans.lower() in ['y', 'yes']:
                max_pages = 10000
            elif ans.lower() not in ['n', 'no']:
                raise ValueError('Only y|n accepted as answers')

        return max_pages

    def _coerce_to_dataframe(self, results):
        key = list(results.keys())[0]
        results_df = json_normalize(results[key])
        results_df['_links.organization.href'] = results_df['_links.organization.href']\
            .str.replace('/v2/organizations/', '')
        results_df['_links.self.href'] = results_df['_links.self.href'].str.replace('/v2/animals/', '')
        results_df['_links.type.href'] = results_df['_links.type.href'].str.replace('/v2/types/', '')

        results_df.rename(columns={'_links.organization.href': 'organization_id',
                                   '_links.self.href': 'animal_id',
                                   '_links.type.href': 'animal_type'}, inplace=True)

        return results_df

    def get_breeds(self):
        print "Getting breeds..."
        breeds = []

        url = urljoin(self._host, 'types/dog/breeds')

        r = requests.get(url,
                        headers={
                            'Authorization': 'Bearer ' + str(self._auth)
                        })
                        
        result = r.json()
        df_results = DataFrame()
        
        df_results = df_results.append(json_normalize(result['breeds']))

        df_results.rename(columns={'_links.type.href': 'breed'}, inplace=True)
        df_results['breed'] = df_results['breed'].str.replace('/v2/types/', '').str.capitalize()

        result = df_results
       # print result
        return result
    
    def adoptable_pets(self, breed = None, size = None, gender = None, age = None, 
                        status = None, location = None, distance = None, sort=None):

        """
        breed: str, tuple or list of str, optional
            String or tuple or list of strings of desired animal type breed to search. Available animal breeds in
            the Petfinder database can be found using the :code:`breeds()` method.
        size: {'small', 'medium', 'large', 'xlarge'}, str, tuple or list of str, optional
            String or tuple or list of strings of desired animal sizes to return. The specified size(s) must be one
            of 'small', 'medium', 'large', or 'xlarge'.
        gender : {'male', 'female', 'unknown'} str, tuple or list of str, optional
            String or tuple or list of strings representing animal genders to return. Must be of 'male', 'female',
            or 'unknown'.
        age : {'baby', 'young', 'adult', 'senior'} str, tuple or list of str, optional
            String or tuple or list of strings specifying animal age(s) to return from search. Must be of 'baby',
            'young', 'adult', 'senior'.
        status : {'adoptable', 'adopted', 'found'} str, optional
            Animal status to filter search results. Must be one of 'adoptable', 'adopted', or 'found'.
        location : str, optional
            Returns results by specified location. Must be in the format 'city, state' for city-level results,
            'latitude, longitude' for lat-long results, or 'postal code'.
        distance : int, optional
            Returns results within the distance of the specified location. If not given, defaults to 100 miles.
            Maximum distance range is 500 miles.
        sort : {'recent', '-recent', 'distance', '-distance'}, optional
            Sorts by specified attribute. Leading dashes represents a reverse-order sort. Must be one of 'recent',
            '-recent', 'distance', or '-distance'.
        """

        print "Finding based on your criteria: ", breed, size, gender, age, location, distance

        url = urljoin(self._host, 'animals/?type=dog')

        params = self._parameters(breed=breed, size=size, gender=gender,
                                 age=age, status=status,
                                 location=location, distance=distance)
    
        params['limit'] = 100
        params['page'] = 1

        r = requests.get(url,
                        headers={
                            'Authorization': 'Bearer ' + self._auth
                        },
                        params=params)

        max_pages = r.json()['pagination']['total_pages']
        print max_pages
        animals = r.json()['animals']
        max_pages = self._check_pages_api_limit(max_pages)

        for page in range(2, max_pages + 1):

            params['page'] = page

            r = requests.get(url,
                            headers={
                                'Authorization': 'Bearer ' + self._auth
                            },
                            params=params)
            if isinstance(r.json(), dict):
                        if 'animals' in r.json().keys():
                            for i in r.json()['animals']:
                                animals.append(i)
        animals = {
            'animals': animals
        }
        animals = self._coerce_to_dataframe(animals)
        #print r
        return animals