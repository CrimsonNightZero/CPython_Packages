# -*- coding: utf-8 -*-
"""
Created on Tue Jul 17 13:46:55 2018

@author: foryou
"""

from data_move import *
import hashlib


if __name__ == '__main__':
    data_path = r'F:\data'
    data_move(data_path)
    
    md5sum = load_md5sum()
    compare_md5sum(md5sum)
#    # 建立 MD5 物件
#    m = hashlib.md5()
#    
#    # 要計算 MD5 雜湊值的資料
#    data = "G. T. Wang"
#    
#    # 更新 MD5 雜湊值
#    m.update(path)
#    
#    # 取得 MD5 雜湊值
#    h = m.hexdigest()
#    print(h)
