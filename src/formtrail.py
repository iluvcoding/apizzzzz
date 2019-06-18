#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat May 18 16:15:42 2019

@author: vignesh
"""


from flask import Flask, redirect, url_for, request,render_template
app = Flask(__name__, template_folder='template')

# =============================================================================
# @app.route('/success')
# =============================================================================
def process_request(d1, d2, loc, prod):
    import pandas as pd
    from datetime import datetime
    fl = loc.lower().capitalize()+ "_" +prod.lower() +".csv"
   
    df = pd.read_csv(r'/home/vignesh/Projects/1000/apizzzzz/inp/'+fl, delimiter = ",")
    date_1 = datetime.strptime(d1, "%Y%m%d")
    date_2 = datetime.strptime(d2, "%Y%m%d")
    
    df = df[df['Date'] >= date_1.strftime("%Y-%m-%d")]
    df = df[df['Date'] <= date_2.strftime("%Y-%m-%d")]
    df = df.reset_index(drop=True)
    jsData = df.to_json()
    print(jsData)
    
    return render_template("table.html",produceList = jsData)

# =============================================================================
# @app.route('/success/<fromDate><ToDate><loc><prod>')
# def success(fromDate,ToDate,loc,prod):
#    print(fromDate) 
# # =============================================================================
# #    req_sts = process_request(fromDate,ToDate,loc,prod)
# # =============================================================================
#    return 'fromDate %'% fromDate
# =============================================================================
@app.route('/login',methods = ['POST', 'GET'])
def login():
   if request.method == 'POST':
      FromDate = request.form['fromDate']
      ToDate = request.form['ToDate']
      loc = request.form['loc']
      prod = request.form['prod']
      result = process_request(FromDate,ToDate,loc,prod)
      return result
# =============================================================================
#    else:
#       user = request.args.get('nm')
#       return redirect(url_for('success',name = user))
# =============================================================================

if __name__ == '__main__':
   app.run(host = "0.0.0.0",debug = True)