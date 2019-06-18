#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri May 24 12:39:13 2019

@author: rishu
"""

import os
import sys
import time
import glob
import shutil
import MySQLdb
import datetime
import pandas as pd







def validate_user_prod(user_name, password, product):
    db = MySQLdb.connect("localhost", "VATI_database",
        	             "database_VATI", "dummy_api")
    print("database connected")
    cursor = db.cursor()
    get_user_det = "SELECT * FROM user_info where user_name = '"+user_name+"'"
    cursor.execute(get_user_det)    
    user_det = cursor.fetchall()[0]
    db.close()
    print("user details is taken")
    d_pass = str(user_det[3])
    
# =============================================================================
#     d_api_key = user_det[1]
# =============================================================================
    d_group = user_det[2]
    
    if str(password) == d_pass:
        db = MySQLdb.connect("localhost", "VATI_database",
            	             "database_VATI", "dummy_api")
        cursor = db.cursor()
        get_user_det = "SELECT user_group FROM user_info where user_name = '"+user_name+"'"
        print(get_user_det)
        cursor.execute(get_user_det)
        prodId = cursor.fetchall()
        print(prodId)
        productId = ','.join(map(str, prodId[0]))
        return productId
        if product == group_dets[1]:
            return True
        else:
            return "Error: Product not available for you. Kindly contact the us at 'vati.satyukt.com'"   
    else:
        return "Error: Wrong password or key"
    
    
    