#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 20 01:02:30 2022

@author: fatima-zahrabanani
"""

import wget

class Hash_table:
    def __init__(self, debug=False):
        self.debug = debug
        
        
class Two_sum:
    def __init__(self, url , debug = False):
        self.debug = debug
        
        filename = wget.download(url)
        f = open(filename, 'r')
        self.lines = list(map(int,f.readlines()))
        
        
        
    def execute(self):
        pass
        
            
        
        
if __name__ == '__main__':
    debug = True
    S = Two_sum(url = "https://d3c33hcgiwev3.cloudfront.net/_6ec67df2804ff4b58ab21c12edcb21f8_Median.txt?Expires=1658361600&Signature=Xq1zX5YOQ~a6mCspx~BJFIxrvn73ySKLh9MHREJojcjFDo9UvDQ~TogksD1886Nj-VISDGBKqzv11V3jZJfJ-PvO63pEcqk2~XRJ3oY1-z2ZE61QNluxVR3MUBubbauCqDzhf3~31U1KK8DNfFpnyllKgbrc3WsEIWkeFl3PacM_&Key-Pair-Id=APKAJLTNE6QMUY6HBC5A"  ,debug = debug)
    S.execute()

    
    