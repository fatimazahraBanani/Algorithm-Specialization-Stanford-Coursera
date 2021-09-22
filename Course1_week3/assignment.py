# -*- coding: utf-8 -*-
"""
Created on Wed Sep 22 09:04:24 2021

@author: Banani Fatima-Zahra
"""

class QuickSort:
    def __init__(self,filename):
        file = open(filename, 'r')
        array = list(map(lambda x: int(x.strip()),file.readlines()))
        self.array = array
        
        
    def first_element_pivot(self,b,e):
        "return the number of comparisons if we always choose the first element as pivot"
        arr = self.array
        if (len(arr[b:e]) == 1) or (len(arr[b:e]) == 0):
            return 0
        else:
            pivot = arr[b]
            j = b+1
            for i in range(b+1,e,1):
                if (arr[i]< pivot):
                    if i != j:
                        arr[i],arr[j] = arr[j],arr[i]
                    j += 1
            arr[b],arr[j-1] = arr[j-1],arr[b]
            return e-b-1 + self.first_element_pivot(b,j-1) + self.first_element_pivot(j,e)
                    
    
    def final_element_pivot(self,b,e):
        "return the number of comparisons if we always choose the final element as pivot"
        arr = self.array
        if (len(arr[b:e]) == 1) or (len(arr[b:e]) == 0):
            return 0
        else:
            arr[b],arr[e-1] = arr[e-1],arr[b]
            pivot = arr[b]
            j = b+1
            for i in range(b+1,e,1):
                if (arr[i]< pivot):
                    if i != j:
                        arr[i],arr[j] = arr[j],arr[i]
                    j += 1
            arr[b],arr[j-1] = arr[j-1],arr[b]
            return e-b-1 + self.final_element_pivot(b,j-1) + self.final_element_pivot(j,e)
        
    def median(self,lst,b,e):
        median = sorted(lst)[1]
        indices_map = {0 : b , 1 : (e-1+b)//2 , 2 : e-1}
        return indices_map[lst.index(median)]
    
    def median_of_three_pivot(self,b,e):
        "return the number of comparisons if we use the median-of-three rule to choose the pivot"
        arr = self.array
        if (len(arr[b:e]) == 1) or (len(arr[b:e]) == 0):
            return 0
        else:
            median_index = self.median([arr[b] ,arr[(b+e-1)//2] ,arr[e-1]],b,e)
            arr[b],arr[median_index] = arr[median_index],arr[b]
            pivot = arr[b]
            j = b+1
            for i in range(b+1,e,1):
                if (arr[i]< pivot):
                    if i != j:
                        arr[i],arr[j] = arr[j],arr[i]
                    j += 1
            arr[b],arr[j-1] = arr[j-1],arr[b]
            return e-b-1 + self.median_of_three_pivot(b,j-1) + self.median_of_three_pivot(j,e)
        

if __name__ == '__main__':
    debug = False
    quickSort = QuickSort("QuickSort.txt")
    if debug:
        print(quickSort.array)
    #first element pivot
    print(quickSort.first_element_pivot(0,len(quickSort.array)))
    #last element pivot
    print(quickSort.final_element_pivot(0,len(quickSort.array)))
    #median-of-three element pivot
    print(quickSort.median_of_three_pivot(0,len(quickSort.array)))
    