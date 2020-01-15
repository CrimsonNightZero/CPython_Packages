# -*- coding: utf-8 -*-
"""
Created on Tue Jul 17 13:46:55 2018

@author: foryou
"""

import shutil
import os
import hashlib
import json

def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def data_move(data_path):
    for path in os.listdir(r'F:\\'):
        if 'core_aaa' in path:
            file_path = os.path.join(r'F:\\', path, 'output', 'data', 'data.txt')
            file_path2 = os.path.join(data_path, path + '.txt')
            debug_path = os.path.join(r'F:\\', path, 'output', 'data', 'debug.txt')
            debug_path2 = os.path.join(data_path, path + '_debug.txt')
            shutil.copyfile(file_path, file_path2)
            shutil.copyfile(debug_path, debug_path2)
            
    txt = save_md5sum(data_path)
            
    with open(r'F:\data\localmd5sum.txt', 'w') as file:
        json.dump(txt, file)
      
        
def save_md5sum(data_path):
    txt = dict()
    for path in os.listdir(data_path):
        file_path = os.path.join(data_path, path)
        if 'core_aaa' in path and (not 'debug' in path):
            md5sum = md5(os.path.join(file_path))
            txt[md5sum] = os.path.splitext(path)[0]
    return txt
            
      
def load_md5sum():
    md5sum = dict()
    with open(r'F:\data\md5sum.txt', 'r') as file:
        for file in file.readlines():
            name = file.split('  ')[0]
            md5sum[name] = file.split('  ')[1].strip('\n')
            
    return md5sum
        

def compare_md5sum(md5sum):
    successful = True
    result = dict()
    with open(r'F:\data\localmd5sum.txt', 'r') as file:
        localmd5sum = json.load(file)
        for localmd5sum_key, localmd5sum_item in localmd5sum.items():
            for md5sum_key, md5sum_item in md5sum.items():
                if localmd5sum_key == md5sum_key and localmd5sum_item == md5sum_item:
                    break
                    
            if localmd5sum_key == md5sum_key and localmd5sum_item == md5sum_item:
                result[localmd5sum_item] = 'True'
            else:
                result[localmd5sum_item] = 'False'
                successful = True
                
    with open(r'F:\data\result.txt', 'w') as file:
        print("Work Successful:" + str(successful))
        file.write("Work Successful: " + str(successful) + "\n\n")
        json.dump(result, file)
        
        
