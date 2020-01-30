import json
from flask import Flask, url_for
import flask
import requests 
from math import sqrt
from flask import request
import numpy as np
import pandas as pd
from flask_cors import CORS
import os
app = flask.Flask(__name__, static_folder="./build/static", template_folder="./build")
CORS(app, resources={r"/*": {"origins": "*"}})

@app.route("/")
def index():
    return flask.render_template("index.html")
    

# Data comes in as [makeup category, color]
@app.route('/query', methods = ['POST'])
def get_data_query():
        
    #df = pd.read_csv('90001_90083_test/90001_90083_breed_count.csv')
    df = pd.read_csv('90001_90083_test/90001_90083_breed_count.csv')
    chart_data = df.to_dict(orient='records')
    chart_data = json.dumps(chart_data, indent=2)
    data = {'chart_data': chart_data}
    df =  df.to_json(orient='records' )
    return df

# https://gist.github.com/threestory/ed0f322d7bb2e3be8ded
@app.route("/counties", methods=['POST'])
def get_zipcode_query():
    filename = os.path.join(app.static_folder, 'storage', 'cb_2014_us_county_5m.json')	
    df = pd.read_json(filename)	
    df =  df.to_json(orient='records' )	
    return df

# https://gist.github.com/threestory/ed0f322d7bb2e3be8ded
@app.route("/counties_data", methods=['POST'])
def get_county_query():
    filename = os.path.join(app.static_folder, 'storage', 'counties_data.json')	
    df = pd.read_json(filename)	
    df =  df.to_json(orient='records' )	
    return df


port = int(os.environ.get('PORT', 33507))
app.run(host='0.0.0.0', port=port, debug = os.environ.get('DEV'))

