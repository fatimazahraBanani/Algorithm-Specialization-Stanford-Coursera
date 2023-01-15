#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 22 22:27:28 2022

@author: fatima-zahrabanani
"""

import wget
import numpy as np
import sys

import random

class Knapsack:
    def __init__(self, url = None, debug = False):
        self.debug = debug
        filename = wget.download(url)
        f = open(filename, 'r')
        lines = f.readlines()
        self.capacity,self.nvalues = tuple(map(int,lines[0].strip('\n').split()))
        self.value_weight_list = [tuple(map(int,x.strip('\n').split())) for x in lines[1:]]
        self.hashtable = dict()
    
    def execute(self,index,capacity):
        
        v_i = self.value_weight_list[self.nvalues-index][0] 
        w_i = self.value_weight_list[self.nvalues-index][1] 
        #Base case
        if index == 1 :
            condition = capacity >= w_i
            value = v_i if condition else 0
            self.hashtable[(index,capacity)] = value
            return value
        
        if (index-1,capacity) in self.hashtable:
            value_index_1_capacity = self.hashtable[(index-1,capacity)]
        else:
            value_index_1_capacity = self.execute(index-1,capacity)
        if capacity < w_i:
            value = value_index_1_capacity
            
        else:
            if (index-1,capacity-w_i) in self.hashtable:
                value_index_1_capacity_w_i = self.hashtable[(index-1,capacity-w_i)]
            else:
                value_index_1_capacity_w_i = self.execute(index-1,capacity-w_i)
            
            value = max( value_index_1_capacity ,(value_index_1_capacity_w_i+v_i))
            
        self.hashtable[(index,capacity)] = value
        return value 

       
if __name__ == "__main__":
    debug = False
    M = Knapsack(url = "https://d3c33hcgiwev3.cloudfront.net/_6dfda29c18c77fd14511ba8964c2e265_knapsack1.txt?Expires=1660953600&Signature=ZL-p4mu7BTIeFbT-jYplvb1Xe1HAHBVTrZ7ebivfq3WW6WTwQ80Ou~BJT6F~41pUUKkSgxr7lZs~WbPnN~sTsMzq5KOZfRDA4Pc-mg-byBPBABN3iOEpEZjnAZB2I-DQE5URUJOSXRjEqKYKOlmHWgr1qKZsczKFQ0Woe-E6b3g_&Key-Pair-Id=APKAJLTNE6QMUY6HBC5A" ,debug = False)
    print(M.execute(M.nvalues,M.capacity))
    
    
    
    

    
    