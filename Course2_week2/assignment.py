#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 29 12:42:40 2021

@author: fatima-zahrabanani
"""
import heapq
import wget


class Dijkstra:
    def __init__(self, url , debug = False):
        self.debug = debug
        self.V_X = list(range(2,201))
        
        self.VPath = {i:1000000 for i in range(2,201)}
        self.VPath[1] = 0
        
        self.heap = [1000000]*199
        
        self.dict_ = dict()
        
        filename = wget.download(url)
        f = open(filename, 'r')
        file = f.readlines()
        
        for line in file:
            lst = line.strip().split()
            self.dict_[int(lst[0])] = {int(u.split(',')[0]) : int(u.split(',')[1]) for u in lst[1:]}
        
        # initialize the path of vertices connected the start vertex 1
        for i,k in enumerate(list(self.dict_[1].keys())):
            self.VPath[k] = self.dict_[1][k]
            self.heap[i] = self.dict_[1][k]
            
        heapq.heapify(self.heap)
        
        
    
    def Shortest_path(self):
        cond = True
        while cond:
            #choose the key of vertex w minimizing the greedy dijkstra score
            
            #if list is empty break loop
            if not self.heap:
                cond = False
                continue
            
            mini = heapq.heappop(self.heap)
            if mini == 1000000:
                cond = False
                continue
            
            #find w and remove it from V_X
            w = None
            for v_x in self.V_X:
                if self.VPath[v_x] == mini:
                    w = v_x
                    self.V_X.remove(w)
                    break
                
            
            # update the heap 
            st = set(list(self.dict_[w].keys())).intersection(set(self.V_X))
            for v_x in st:
                self.heap_delete_insert(w, v_x)
            
        
            
            
            
    
    
    def heap_delete_insert(self, vertex_X , vertex_V_X):
        key = min(self.VPath[vertex_V_X],self.VPath[vertex_X]+self.dict_[vertex_X][vertex_V_X])
        if key != self.VPath[vertex_V_X]:
            self.heap.remove(self.VPath[vertex_V_X])
            heapq.heapify(self.heap)
            heapq.heappush(self.heap, key)
            self.VPath[vertex_V_X] = key
            
    
    
    
if __name__ == '__main__':
    debug = False
    D = Dijkstra(url = "https://d3c33hcgiwev3.cloudfront.net/_dcf1d02570e57d23ab526b1e33ba6f12_dijkstraData.txt?Expires=1633219200&Signature=ZLOZIZDiLuw~ij~MGRZg~ev91mDeU5-Npn463-up40bf7ox41C3BUjN9G3J5yVd~QgLpCzkJaNq-UiQXid5E0alza7UepqcANOLgB7c6lZRGVPkazAM9azM9M8i5Mk8Q7waqQPUFJhM~Hus7YNt7U5y-AKjTwQu5O2eADiVoY7U_&Key-Pair-Id=APKAJLTNE6QMUY6HBC5A"  ,debug = True)
    D.Shortest_path()
    keys = [7,37,59,82,99,115,133,165,188,197]
    for k in keys:
        print(D.VPath[k],end=',')
    
    