#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed May 22 11:45:32 2019

@author: rishu
"""
import csv
import glob
import json
import requests
import numpy as np
import pandas as pd
from subprocess import call
from matplotlib import pyplot as plt
from datetime import datetime, timedelta


def get_the_values(cmd):
    import datetime as dt
    resp = requests.get(cmd)        
    foo = resp.json()
    arr_cloud = np.nan*np.zeros(48)
    for i in range(6):
        n = len(resp.json()['Days'][i]['Timeframes'])
        for j in range(n):
            tmp = resp.json()['Days'][i]['Timeframes'][j]
            cur_time = dt.datetime.strptime("%s%04d"%(tmp['date'],tmp['time']),"%d/%m/%Y%H%M")
            if (i==0) and (j==0):                
                ini_time = cur_time            
            d_time = cur_time - ini_time
            ii = int(d_time.total_seconds()/10800.0)            
            arr_cloud[ii] = tmp['cloudtotal_pct']    
    return arr_cloud

def get_new_arr(arr, imd_csv, d1, delt, dist):
   imd_excl = imd_csv[imd_csv.DISTRICT == dist].iloc[3][(d1+timedelta(days=delt)).strftime("%d%m%Y")]*12.5
   sum_arr = arr.mean()
   if not sum_arr == 0:            
       fact = imd_excl/sum_arr    
       new_arr = arr*fact
       new_str_arr = [str(x) for x in new_arr]
       return (", ").join(new_str_arr),(d1+timedelta(days=delt)).strftime("%Y%m%d")
   else:
       return '0, 0, 0, 0, 0, 0, 0, 0',(d1+timedelta(days=delt)).strftime("%Y%m%d")

def get_the_cloud_cover(location_name):
    state_list = [u'andaman-nicobar.txt', u'andhra-pradesh.txt', u'arunachal-prades.txt', u'assam.txt', u'bihar.txt', u'chandigarh.txt', u'chhattisgarh.txt', u'delhi.txt', u'diu.txt',              u'dnh-daman.txt', u'goa.txt', u'gujarat.txt', u'haryana.txt', u'himachal-pradesh.txt',              u'jammu-kashmir.txt', u'jharkhand.txt', u'karnataka.txt', u'kerala.txt', u'lakshadweep.txt',              u'madhya-pradesh.txt', u'maghalaya.txt', u'maharashtra.txt', u'manipur.txt', u'mizoram.txt',              u'nagaland.txt', u'orissa.txt', u'pondicherry.txt', u'punjab.txt', u'rajasthan.txt', u'sikkim.txt',              u'tamilnadu.txt', u'telangana.txt', u'tripura.txt', u'uttar-pradesh.txt', u'uttaranchal.txt', u'west-bengal.txt']
    today_dt = datetime.today().strftime("%Y-%m-%d")
    for state in state_list:
        cmd = 'wget -P /home/vignesh/Projects/1000/apizzzzz/out/' + today_dt + ' "'+'http://nwp.imd.gov.in/'+ str(state) + '"'
        call(cmd, shell = True)
    d1 = datetime.today()
    d2 = d1 + timedelta(5)
    delta = d2 - d1
    dates = [(d1 + timedelta(days=i)).strftime("%d%m%Y") for i in range(delta.days + 1)][1:]
    ac_dates = []
    today_dt = datetime.today().strftime("%Y-%m-%d")
    main_arr = []
    header = ['STATE', 'DISTRICT', 'VARIABLE']
    for in_file in glob.glob('/home/vignesh/Projects/1000/apizzzzz/out/'+today_dt+'/*'):
        with open(in_file, "r") as lines:          
            for line in lines:
                row = []
                for dt in dates:
                   if dt in line and len(header) <= 7:
                       header.append(dt)               
                if "STATE" in line:
                    state = line.rstrip().split(":")[1].strip()                          
                if "DISTRICT" in line and "PREDICTION" not in line:
                    dis = line.rstrip().split(":")[1].strip()                             
                if "(" in line and ")" in line:    
                    foo = line.rstrip().split(")")
                    var = foo[0].split()[0] + " " + foo[0].split()[1]        
# =============================================================================
#                     print(in_file)
#                     print(foo[1].split())
# =============================================================================
                    values =[float(x) for x in foo[1].split()]
                    
                    row.append(state)
                    row.append(dis)
                    row.append(var)
                    for val in values:
                        row.append(val)
                    main_arr.append(row)
    main_arr.insert(0, header)    
    with open("/home/vignesh/Projects/1000/apizzzzz/out/"+d1.strftime("%Y-%m-%d")+".csv","w+") as my_csv:
        csvWriter = csv.writer(my_csv,delimiter=',')
        csvWriter.writerows(main_arr)
    imd_csv = pd.read_csv('/home/vignesh/Projects/1000/apizzzzz/out/'+d1.strftime("%Y-%m-%d")+'.csv')
    if location_name == "KOTA":
        cmd = "http://api.weatherunlocked.com/api/forecast/23.845,75.801?app_id=bdb9c61f&app_key=82732a87e5a3b158d072e1f30afd67e9"
    elif location_name == "LALITPUR":
        cmd = "http://api.weatherunlocked.com/api/forecast/24.7,78.4?app_id=bdb9c61f&app_key=82732a87e5a3b158d072e1f30afd67e9"
    else:
        return {"Error":"No Such Location Specified"}    
    arr = get_the_values(cmd)
    a1,da1 = get_new_arr(arr[1:9], imd_csv, d1, 1, location_name)
    a2,da2 = get_new_arr(arr[9:17], imd_csv, d1, 2, location_name)
    a3,da3 = get_new_arr(arr[17:25], imd_csv, d1, 3, location_name)
    a4,da4 = get_new_arr(arr[25:33], imd_csv, d1, 4, location_name)
    a5,da5 = get_new_arr(arr[33:41], imd_csv, d1, 5, location_name)
    ret_dict = {}
    ret_dict[da1] = a1
    ret_dict[da2] = a2
    ret_dict[da3] = a3
    ret_dict[da4] = a4
    ret_dict[da5] = a5
    return ret_dict
    
