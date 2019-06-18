#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 10 13:33:41 2019

@author: rishu
"""

from flask import Flask, request, Response, send_file
# =============================================================================
# from flask_restful import Resource, Api
# =============================================================================

app = Flask(__name__)
# =============================================================================
# api = Api(app)
# =============================================================================

def validate_user_in_database(user_name, password):
# =============================================================================
#     print "hello "+ user_name +" password " + password
#     import MySQLdb
#     db = MySQLdb.connect("localhost", "rishu", "rishu123", "Ambhas")
#     cursor = db.cursor()
#     user_sql = "SELECT * FROM UserBasicInfo WHERE user_name = '"+user_name + "'"
#     cursor.execute(user_sql)
#     user_details = cursor.fetchall()[0]
#     cursor.close()
#     if user_details[6] == 1:
#         return 1
#     else:
#         return 0
# =============================================================================
    return 1

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
    
    return df
    
    
    


# =============================================================================
# api.add_resource(do_something, '/Hello/<int:todo_id>')
# =============================================================================
@app.route('/post', methods=['POST'])
def post_route():
    if request.method == 'POST':
        data = request.get_json(force=True)
        param_list = [str(x) for x in data.keys()]
        if len(data) == 0:
            print "No data has been parsed"
            return "Request not processed\n give parameters u, p, d1, d2, loc and prod in a json all of these are must parameters"
        elif not 'u' in param_list:
            return "No user name has been specified.\n"
        elif not 'p' in param_list:
            return "No password has been specified.\n"
        elif not 'd1' in param_list:
            return "No start date is given.\n"
        elif not 'd2' in param_list:
            return "No end date is given.\n"
        elif not 'loc' in param_list:
            return "No location is specified.\n You can choose from Plot1, Plot2, Plot3, Plot4.\n"
        elif not 'prod' in param_list:
            return "No product has been specified"
        else:            
            print('Data Received: "{data}"'.format(data=data))
            print "Helllllllllllllllppppppppp"
            user_name = str(data[u'u'])
            password = str(data[u'p'])
            d1 = str(data[u'd1'])
            d2 = str(data[u'd2'])
            loc = str(data[u'loc'])
            prod = str(data[u'prod']).lower()
            print "I wass herreeeeeeeeee"
            validate_user = validate_user_in_database(user_name, password)
            if validate_user == 1:
                req_sts = process_request(d1, d2, loc, prod)
                out_file = "/home/vignesh/Projects/1000/apizzzzz/out/"+loc+"_"+prod+"_"+d1+"_"+d2+".csv"
                #return Response(output.getvalue(), mimetype="text/csv")
                req_sts.to_csv(out_file, index = False)                
                return send_file(out_file, as_attachment = True)
            else:
                return "User is not registered.\n"
    elif request.method == 'GET':
        data = request.get_json(force=True)
        #param_list = [str(x) for x in data.keys()]
        #if len(data) == 0:
            #print "No data has been parsed"
            #return "Request not processed\n give parameters u, p, d1, d2, loc and prod in a json all of these are must parameters"
        return "<h1>Distant Reading Archive</h1><p>This site is a prototype API for distant reading of science fiction novels.</p>"                
# =============================================================================
# app.run(host = '0.0.0.0')
# =============================================================================
def home():
    return "<h1>Distant Reading Archive</h1><p>This site is a prototype API for distant reading of science fiction novels.</p>"                
            
app.run(host='0.0.0.0',debug = True)
