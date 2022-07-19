#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 27 01:02:30 2022

@author: fatima-zahrabanani
"""

import heapq
import wget

class Heap:
    def __init__(self, debug=False, minHeap = True):
        self.debug = debug
        # the list containing the array containing the elements of the heap
        self.heap = []
        self.minHeap = minHeap
        self.n_elements = 0
        
    def get_root(self):
        return self.heap[0]
        
    def parent_of(self,element_index):
        #if self.debug:
        #print("parent of: ",element_index,"is: ",((element_index+1)//2)-1)
        return ((element_index+1)//2)-1
    
    def children_of(self,element_index):
        return 2*(element_index+1)-1, 2*(element_index+1)
    
    def restore_heap_property_insertion(self,element_index,minHeap):
        if element_index == 0:
            return None
        else:
            parent_index = self.parent_of(element_index)
            if minHeap == True:
                condition = self.heap[parent_index] > self.heap[element_index]
            else: 
                condition = self.heap[parent_index] < self.heap[element_index]
                
            if condition:
                a = self.heap[element_index]
                self.heap[element_index] = self.heap[parent_index]
                self.heap[parent_index] = a
                self.restore_heap_property_insertion(parent_index,minHeap)
            else:
                return None
            
    def restore_heap_property_deletion(self,element_index,minHeap):
        children_indices = self.children_of(element_index)
        n_children = 2
        if (children_indices[0]>=self.n_elements):
            n_children = 0
        elif (children_indices[1]>=self.n_elements):
            n_children = 1
            
        if n_children == 0:
            return None
        else:
            if n_children == 1:
                cond_index = children_indices[0]
                cond_element = self.heap[children_indices[0]]
            else:
                if minHeap == True:
                    cond_element = min(self.heap[children_indices[0]],self.heap[children_indices[1]])
                else:
                    cond_element = max(self.heap[children_indices[0]],self.heap[children_indices[1]])
                    
                cond_index = children_indices[0] if (self.heap[children_indices[0]] == cond_element) else children_indices[1]   

            if minHeap:
                condition = self.heap[element_index] <= cond_element
            else:
                condition = self.heap[element_index] >= cond_element
            
            
            if condition:
                return None
            else:
                a = self.heap[element_index]
                self.heap[element_index] = self.heap[cond_index]
                self.heap[cond_index] = a
                self.restore_heap_property_deletion(cond_index,minHeap)
            
                    
        
    def insert(self, element):
        """
        Function to insert an element to the heap while ensuring the heap's property
        """
        self.heap.append(element)
        self.n_elements += 1
        self.restore_heap_property_insertion(self.n_elements-1,self.minHeap)
        
        
    def delete(self, element_index):
        """
        Function to delete an element from the heap while ensuring the heap's property
        """
        self.heap[element_index] = self.heap[-1]
        del self.heap[-1]
        self.n_elements -= 1
        self.restore_heap_property_deletion(element_index,self.minHeap)
        

        
class Median:
    def __init__(self, url , debug = False):
        self.debug = debug
        
        filename = wget.download(url)
        f = open(filename, 'r')
        self.lines = list(map(int,f.readlines()))
        
        
        
    def execute(self):
        heap_low = Heap(debug=self.debug, minHeap = False)
        heap_high = Heap(debug=self.debug, minHeap = True)
        lines = self.lines
        median = lines[0]
        medians_sum = median
        if self.debug:
            count = 0
        for element in lines[1:]:
            if element > median:
                heap_high.insert(element)
            else:
                heap_low.insert(element)
            
        
            if (heap_low.n_elements == heap_high.n_elements+1):
                max_heap = heap_low.get_root()
                heap_low.delete(0)
                heap_high.insert(median)
                median = max_heap
            elif (heap_low.n_elements == heap_high.n_elements-2):
                min_heap = heap_high.get_root()
                heap_high.delete(0)
                heap_low.insert(median)
                median = min_heap
                
            #if self.debug:
            #print(median)
            
            medians_sum += median
            #if self.debug:
            #count+=1
            #print("Iteration ",count)
        print("medians'sum is:",medians_sum)
            
        
        
if __name__ == '__main__':
    debug = True
    M = Median(url = "https://d3c33hcgiwev3.cloudfront.net/_6ec67df2804ff4b58ab21c12edcb21f8_Median.txt?Expires=1658361600&Signature=Xq1zX5YOQ~a6mCspx~BJFIxrvn73ySKLh9MHREJojcjFDo9UvDQ~TogksD1886Nj-VISDGBKqzv11V3jZJfJ-PvO63pEcqk2~XRJ3oY1-z2ZE61QNluxVR3MUBubbauCqDzhf3~31U1KK8DNfFpnyllKgbrc3WsEIWkeFl3PacM_&Key-Pair-Id=APKAJLTNE6QMUY6HBC5A"  ,debug = debug)
    M.execute()

    
    