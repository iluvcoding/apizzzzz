#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed May 22 13:10:41 2019

@author: vignesh
"""

from api_ready_cloud_cover import get_the_cloud_cover
import flask
from flask import request, jsonify
import os
import numpy
import pandas as pd
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
app = flask.Flask(__name__)
app.config["DEBUG"] = True

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


@app.route('/', methods=['GET'])
def home():
    return '''<h1>Satyukt Analytics API</h1>
<p>API to access data.</p>'''




@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404



@app.route('/cloudapi/v1/data', methods=['GET'])
def api_filter():
    query_parameters = request.args
    locationName = query_parameters.get('loc')
    print(locationName)
    loc = get_the_cloud_cover(locationName)
    return jsonify(loc)


app.run(host='0.0.0.0', port = 5000)
 