#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Jun  6 18:49:38 2019

@author: rishu
"""

from Crypto.Cipher import AES
import base64

def encrypt(user_name, password, product):
    msg_text = (user_name+"_"+password+"_"+product).rjust(32)
    secret_key = '12123569723567455667123a' 
    cipher = AES.new(secret_key,AES.MODE_ECB)
    encoded = base64.b64encode(cipher.encrypt(msg_text))
    return encoded

def decrypt_info(key):
    secret_key = '12123569723567455667123a' 
    cipher = AES.new(secret_key,AES.MODE_ECB)
    decoded = cipher.decrypt(base64.b64decode(key))
    info_arr = decoded.strip().split("_")
    return info_arr[0], info_arr[1], info_arr[2]    


key = "ww8s/AxVARsgSzJj/0oHbMKyiCTA0L4jiw/N2vHEP6E="

d = decrypt_info(key)
