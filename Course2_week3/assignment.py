#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 27 01:02:30 2022

@author: fatima-zahrabanani
"""

import heapq
import wget


class Median:
    def __init__(self, url , debug = False):
        self.debug = debug
        
        filename = wget.download(url)
        f = open(filename, 'r')
        file = f.readlines()
        
        
if __name__ == '__main__':
    debug = False
    M = Median(url = "https://d3c33hcgiwev3.cloudfront.net/_dcf1d02570e57d23ab526b1e33ba6f12_dijkstraData.txt?Expires=1633219200&Signature=ZLOZIZDiLuw~ij~MGRZg~ev91mDeU5-Npn463-up40bf7ox41C3BUjN9G3J5yVd~QgLpCzkJaNq-UiQXid5E0alza7UepqcANOLgB7c6lZRGVPkazAM9azM9M8i5Mk8Q7waqQPUFJhM~Hus7YNt7U5y-AKjTwQu5O2eADiVoY7U_&Key-Pair-Id=APKAJLTNE6QMUY6HBC5A"  ,debug = debug)
    
    
    