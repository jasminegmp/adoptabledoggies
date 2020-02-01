import json
from flask import Flask, url_for
import flask
import pandas as pd
from flask_cors import CORS
import os
import requests

app = flask.Flask(__name__, static_folder="./build/static", template_folder="./build")
CORS(app, resources={r"/*": {"origins": "*"}})

@app.route("/", methods=['Get'])
def index():
    return flask.render_template("index.html")
    
port = int(os.environ.get('PORT', 33507))
app.run(host='0.0.0.0', port=port, debug = os.environ.get('DEV'))

