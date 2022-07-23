#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 20 01:02:30 2022

@author: fatima-zahrabanani
"""

import wget
import multiprocessing as mp
import numpy as np


class Node:
   def __init__(self, dataval=None):
      self.dataval = dataval
      # nextval is a the next Node object
      self.nextnode = None
      
   def showvalue(self):
       print(self.dataval)
       print(self.nextnode)

class SLinkedList:
   def __init__(self,debug =False):
      self.debug = debug
      self.headnode = None
      
   def insert(self,dataval):
       """
       Function to insert the element at the beginning of the linked list
       """
       new = Node(dataval)
       
       new.nextnode = self.headnode
       self.headnode = new
       if self.debug:
           self.headnode.showvalue()
       
   def lookup(self,dataval,currentnode):
       """
       Function that return True if data exists otherwise return False
       """
       if currentnode == None:
           return False
       elif currentnode.dataval == dataval:
           return True
       else:
           return self.lookup(dataval,currentnode.nextnode)
           
   def showvalues(self,node):
       if node == None:
           print('done')
       else:
           print(node.dataval)
           self.showvalues(node.nextnode)
            
class HashTable:
    def __init__(self, debug=False, nbuckets=999983):
        self.debug = debug
        # Should be a power of 10
        self.nbuckets = nbuckets
        self.hashtable = []
        # Each bucket contains a linked list
        for i in range(nbuckets):
            self.hashtable.append(SLinkedList())
            
    def hashfunction(self,x):
        """
        Function that outputs the corresponding bucket number for the particular x
        We're using Modulo method of a prime number 997 as a hash function
        """
        return x%self.nbuckets
    
    def insert(self,x):
        """
        Insert an element x into the hashTable
        """
        bucket = self.hashfunction(x)
        if self.debug:
            print("bucket for ",x," is :",bucket)
        self.hashtable[bucket].insert(x)
        
    def lookup(self,x):
        """
        Function to lookup for an element x
        """
        bucket = self.hashfunction(x)
        if self.debug:
            print("bucket for ",x," is :",bucket)
        return self.hashtable[bucket].lookup(x,self.hashtable[bucket].headnode)
        
    def showvalues(self):
        for i in [2,6,11,7,9,1,982,980,0]:
            print("values of bucket ",i)
            self.hashtable[i].showvalues(self.hashtable[i].headnode)
        
class TwoSum:
    def __init__(self,lines,hashtable,debug = False):
        self.debug = debug
        self.hashtable = hashtable
        self.lines = lines

    def execute(self,mini):
        hashtable = self.hashtable   
        result = 0
        add = 2000
        if mini == 8000:
            add = 2001
        for t in range(mini,mini+add):
            print("iteration :",t)
            for element in self.lines:
                elementtolookup = t - element
                if elementtolookup == element:
                    continue
                else:
                    if hashtable.lookup(elementtolookup):
                        result += 1
                        break
        return result
        
            
    
    
def program(mini,lines,hashtable):
    debug = False
    #filename = "RandomTest.txt"
    S = TwoSum(lines,hashtable,debug = debug)
    return S.execute(mini)
    
if __name__ == '__main__':
    pool = mp.Pool(mp.cpu_count())
    
    ranges = np.arange(-10000, 9000, 2000, dtype=int).tolist()
    print(ranges)
    
    filename = wget.download("https://d3c33hcgiwev3.cloudfront.net/_6ec67df2804ff4b58ab21c12edcb21f8_algo1-programming_prob-2sum.txt?Expires=1658448000&Signature=JDlP12oCUhkGRLzrQ-BvaP44B6APq1IwyzBIwQue7p9gQPjNYaCwrwhMsjgLQGqYPWiTvozezwzKpuEkkwtlnerzQynEDnVagMsYKcF71UlSo3n0xpdJc1bAiYD5U140twbqwNWHk8ecZT8DjgNxFmm0BkoHlk4KQE9UEznZmoQ_&Key-Pair-Id=APKAJLTNE6QMUY6HBC5A")
    f = open(filename, 'r')
    lines = list(map(int,f.readlines()))
    
    hashtable = HashTable()
    # populate the HashTable with the integers
    for element in lines:
        hashtable.insert(element)
        
    print('hashtable created')

    # Step 2: `pool.apply` the `howmany_within_range()`
    results = [pool.apply(program, args = (mini,lines,hashtable)) for mini in ranges]

    # Step 3: Don't forget to close
    pool.close()    

    print(sum(results))

    
    