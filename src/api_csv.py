#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon May 20 22:57:35 2019

@author: thiyaku
"""

import flask
from flask import request, jsonify,render_template,send_file
import os
import pandas as pd
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
from api_ready_cloud_cover import get_the_cloud_cover
import glob
import datetime
from datetime import date,timedelta
import encrypt_and_decrypt as ed
from user_validation import validate_user_prod

app = flask.Flask(__name__,template_folder='template')
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



@app.route('/api/v1',methods=['GET'])
def api_base():
    return render_template("base.html")


# =============================================================================
# auth = HTTPBasicAuth()
# 
# users = {
#     "john": generate_password_hash("hello"),
#     "susan": generate_password_hash("bye")
# }
# 
# @auth.verify_password
# def verify_password(username, password):
#     if username in users:
#         return check_password_hash(users.get(username), password)
#     return False
# =============================================================================

csvDir = '../inp'
@app.route('/api/v1/data', methods=['GET'])
# =============================================================================
# @auth.login_required
# =============================================================================
def api_filter():    
    query_parameters = request.args
    product = query_parameters.get('product')
    if product == "cloud":
        locationName = query_parameters.get('loc')
        print(locationName)
        allData = get_the_cloud_cover(locationName)
        return jsonify(allData)
    elif product == "ndvi" or product == "sm":
        startDate = query_parameters.get('startDate')
        endDate = query_parameters.get('endDate')
        print(endDate)
        plotName = query_parameters.get('plotName')
        csvFile = os.path.join(csvDir, '%s.csv' % plotName)
        if not os.path.exists(csvFile):
            return page_not_found(404)
        df = pd.read_csv(csvFile)
        if startDate:
            df = df[df.Date >= startDate]
        if endDate:
            df = df[df.Date <= endDate]
        if product:
            df = df.loc[:, df.columns.isin(['Date', product])]
        df.reset_index(drop=True, inplace=True)
        allData = df.to_dict()
        return jsonify(allData)
    else:
        return render_template("data.html") 
   

#the below function helps to download the file using get request 
@app.route('/api/v1/downloads', methods=['GET'])
def download():
    base_path = "/home/vignesh/Projects/1000/apizzzzz/src/trail_ground/vaari/"
    query_parameters = request.args
    key = query_parameters.get('key')
    decrypt_key = ed.decrypt_info(key)
    print(decrypt_key)
    product = decrypt_key[2]
#validate_user_prod return product ID from database    
    productId = validate_user_prod(decrypt_key[0],decrypt_key[1],product)
    print(productId)  
    if productId != "":
         print('authendicated')   
         if request.method == 'GET':
            print("Entred DownloadFile")
            FromDate = request.values['startDate']
            print(FromDate)
            ToDate = request.values['endDate']
            print(FromDate,ToDate)
            product = request.values['product']
            print(product)
            format_Prj = request.values['format']
            print(format_Prj)
#below 20 Lines helps to search the file based on start date and end date and pass the list to the render template          
            d1 = datetime.datetime.strptime(FromDate,"%Y%m%d").date()
            d2 = datetime.datetime.strptime(ToDate,"%Y%m%d").date()
            delta = d2 - d1
            d6 = []        
            for i in range(delta.days + 1):
                d2 = d1 + timedelta(days=i)
                d4 = str(d2)
                d5 = d4.replace('-','')
                d6 += [d5]
            
            path = glob.glob(base_path + productId +"/"+ product +"/"+format_Prj+"/*")
            tifFile = path
            fileList = []        
            for j in range(0,len(d6)):
                for i in range(0,len(tifFile)):
                    if d6[j] in tifFile[i]:
                        k = tifFile[i]
                        fileList += [k]     
            
            print(fileList)
            return render_template("listdownload.html",downloadList = fileList)
    else:
        return render_template("data.html") 
         
   
    
#The handle data function is gets the URL and pass it to the send file function which return the file
@app.route('/<path:filename>', methods=['GET','POST'])
def handle_data(filename):
    print(filename)
    path = request.args.getlist(filename)
    print(path)
    return send_file(filename)
    
    

@app.route('/cloudapi/v1/data', methods=['GET'])
def api_fil():
    query_parameters = request.args
    locationName = query_parameters.get('loc')
    print(locationName)
    loc = get_the_cloud_cover(locationName)
    return jsonify(loc)    


app.run(host='0.0.0.0', port = 5010)
