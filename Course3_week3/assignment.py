#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug  5 20:02:45 2022

@author: fatima-zahrabanani
"""

import wget
import numpy as np
import sys

import random

    
class Tree:
    def __init__(self, debug=False,root = None, leftTree = None, rightTree = None):
        self.debug = debug
        self.root = root
        self.leftTree = leftTree
        self.rightTree = rightTree
        

class HuffmanCode:
    def __init__(self,url=None,debug=False):
        self.debug = debug
        filename = wget.download(url)
        f = open(filename, 'r')
        lines = f.readlines()
        self.nelements = int(lines[0])
        self.frequencies = list(map(int,lines[1:]))
        self.max_depth = None
        self.min_depth = None
        
       
    def buildTree(self, frequencies, elements):
        if len(frequencies) == 2:
            T = [elements[0],elements[1]]
            if self.debug:
                print(T)
            return T
            
        else:
            a = min(frequencies)
            index_a = frequencies.index(a)
            element_a = elements[index_a]
            del frequencies[index_a]
            del elements[index_a]
            
            b = min(frequencies)
            index_b = frequencies.index(b)
            element_b = elements[index_b]
            del frequencies[index_b]
            del elements[index_b]
            
            frequencies.append(a+b)
            elements.append([element_a,element_b])
            
            return self.buildTree(frequencies, elements)
        
    def extendTree(self,T, optimalTree, count):
        leftTreeElements = T[0]
        if self.debug:
            print("left tree elements ",leftTreeElements)
        rightTreeElements = T[1]
        if self.debug:
            print("right tree elements ",rightTreeElements)
            
        
        if len(leftTreeElements) == 1:
            optimalTree.leftTree = leftTreeElements[0]
            if (self.min_depth==None):
                self.min_depth = count
            if (self.max_depth != None):
                self.max_depth = max(self.max_depth,count)
            else:
                self.max_depth = count
            if self.debug:
                print("min_depth ",self.min_depth)
                print("max_depth ",self.max_depth)
        else:
            optimalTree.leftTree = Tree()
            self.extendTree(leftTreeElements,optimalTree.leftTree, count+1)
        if len(rightTreeElements) == 1:
            optimalTree.rightTree = rightTreeElements[0]
            if (self.min_depth==None):
                self.min_depth = count
            if (self.max_depth != None):
                self.max_depth = max(self.max_depth,count)
            else:
                self.max_depth = count
            if self.debug:
                print("min_depth ",self.min_depth)
                print("max_depth ",self.max_depth)
            
        else:
            optimalTree.rightTree = Tree()
            self.extendTree(rightTreeElements,optimalTree.rightTree,count+1)
            
    def execute(self):
        T = self.buildTree(self.frequencies,[[i] for i in range(self.nelements)])
        count = 1
        optimalTree = Tree()
        self.extendTree(T,optimalTree,count)
        return self.max_depth, self.min_depth
        
        
        
        
            
            
            
            
        
class MaximumWeightIndependentSet:
    def __init__(self, url = None, debug = False):
        self.debug = debug
        filename = wget.download(url)
        f = open(filename, 'r')
        lines = f.readlines()
        self.nvertices = int(lines[0])
        self.weights = list(map(int,lines[1:]))
        
        
    def greedy(self):
        A = []
        A.append(0)
        A.append(self.weights[0])
        path_1 = [0]
        path_2 = []
        for i in range(2,self.nvertices+1):
            maxi = max(A[i-1],A[i-2]+self.weights[i-1])
            A.append(maxi)
            if maxi == A[i-2]+self.weights[i-1]:
                path_1, path_2 = path_2 + [i-1], path_1
                if self.debug:
                    print("path 2",path_2)
                if self.debug:
                    print("path 1",path_1)
            else:
                path_2 = path_1
        return path_1
            
                
    def execute(self):
        path = self.greedy()
        vertices = [0, 1, 2, 3, 16, 116, 516, 996]
        result = [str(int(vertice in path)) for vertice in vertices]
        return "".join(result)
                
        
if __name__ == "__main__":
    debug = False
    H = HuffmanCode(url = "https://d3c33hcgiwev3.cloudfront.net/_eed1bd08e2fa58bbe94b24c06a20dcdb_huffman.txt?Expires=1659830400&Signature=kRD1Zp-cWwdBGAme9XWVJ7FYFJDEodAVtJXrJXMja0w4q3IalcdE~-ryBl6a7PjkpnU8dV1DIg~Km9AKF2ACzPGEZkuJ1F-qlvrxot6l~Whn4j1QfrVEq~RaYPjfW9slhVPgq1NvGIg3o6VM8uvf6HJzd8ftqPqMA1qhZ54UUKQ_&Key-Pair-Id=APKAJLTNE6QMUY6HBC5A" ,debug = False)
    print(H.execute())
    
    M = MaximumWeightIndependentSet(url = "https://d3c33hcgiwev3.cloudfront.net/_790eb8b186eefb5b63d0bf38b5096873_mwis.txt?Expires=1659916800&Signature=esgegxaQ5i51E5I~lpk~HH411sj3-EsSTHK5xtzSG6qujr6EVS55gyY1IoITkSTIuBNacXgwEn114X-QtjXLJzUdcLZt3cjUXpvVXA5KUMkulpfziTijNh5TKEyL~k2A-px40UFO-rrAtAnyvF7E0yIU9NJLPzdk19~u4ih9III_&Key-Pair-Id=APKAJLTNE6QMUY6HBC5A",debug = False)
    print(M.execute())
    
    
    
    
    
    

    
    