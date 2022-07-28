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
    
    def restore_heap_property_insertion(self,element_index,minHeap,swapList):
        if element_index == 0:
            return swapList
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
                swapList.append((element_index,parent_index))
                return self.restore_heap_property_insertion(parent_index,minHeap,swapList)
            else:
                return swapList
            
    def restore_heap_property_deletion(self,element_index,minHeap,swapList):
        children_indices = self.children_of(element_index)
        n_children = 2
        if (children_indices[0]>=self.n_elements):
            n_children = 0
        elif (children_indices[1]>=self.n_elements):
            n_children = 1
            
        if n_children == 0:
            return swapList
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
                return swapList
            else:
                a = self.heap[element_index]
                self.heap[element_index] = self.heap[cond_index]
                self.heap[cond_index] = a
                swapList.append((element_index,cond_index))
                return self.restore_heap_property_deletion(cond_index,minHeap,swapList)
            
    def insert(self, element):
        """
        Function to insert an element to the heap while ensuring the heap's property
        """
        self.heap.append(element)
        self.n_elements += 1
        swapList = []
        return self.restore_heap_property_insertion(self.n_elements-1,self.minHeap,swapList)
        
        
    def delete(self, element_index):
        """
        Function to delete an element from the heap while ensuring the heap's property
        """
        self.heap[element_index] = self.heap[-1]
        del self.heap[-1]
        self.n_elements -= 1
        swapList = []
        return self.restore_heap_property_deletion(element_index,self.minHeap,swapList)
 
class Jobs:
    def __init__(self,filename=None,debug=False):
        self.debug = debug
        #filename = wget.download("https://d3c33hcgiwev3.cloudfront.net/_6ec67df2804ff4b58ab21c12edcb21f8_algo1-programming_prob-2sum.txt?Expires=1658448000&Signature=JDlP12oCUhkGRLzrQ-BvaP44B6APq1IwyzBIwQue7p9gQPjNYaCwrwhMsjgLQGqYPWiTvozezwzKpuEkkwtlnerzQynEDnVagMsYKcF71UlSo3n0xpdJc1bAiYD5U140twbqwNWHk8ecZT8DjgNxFmm0BkoHlk4KQE9UEznZmoQ_&Key-Pair-Id=APKAJLTNE6QMUY6HBC5A")
        f = open(filename, 'r')
        lines = f.readlines()
        self.njobs = int(lines[0].strip('\n'))
        if self.debug:
            print(self.njobs)
        self.lines = [tuple(map(int, x.strip('\n').split())) for x in lines[1:]]
        if self.debug:
            print("Number of lines", len(lines))
        
    def job_score_1(self,weight,length):
        return weight-length
    
    def job_score_2(self,weight,length):
        return weight/length
        
    def execute(self, score_number = 1):
        heap = Heap(minHeap=False)
        # dictionary mapping the index of a job in the heap with its weight and length
        index_weight_length_dict = dict()
        score_index_dict = dict()
        score_weight_length = dict()
        
        if self.debug:
            print("Number of lines", len(self.lines))
        # Populate the maximum Heap
        for w,l in self.lines:
            if score_number == 1:
                score = self.job_score_1(w,l)
            else:
                score = self.job_score_2(w,l)
            if score in score_weight_length:
                score_weight_length[score].append((w,l))
            else:
                score_weight_length[score] = [(w,l)]
            heap.insert(score)
            
        if self.debug:
            print("score index dict")
            for k,v in score_weight_length.items():
                print("score ",k," :weight, length ",v)
        
        if self.debug:
            print("heap length", heap.n_elements)
            
        for i in range(heap.n_elements):
            heapList = heap.heap
            score = heapList[i]
            index_weight_length_dict[i] = score_weight_length[score][0]
            if self.debug:
                print("iteration ",i,"weight, length",index_weight_length_dict[i])
            if score in score_index_dict:
                score_index_dict[score].append(i)
            else:
                score_index_dict[score] = [i]
            del score_weight_length[score][0]
            
        if self.debug:
            print("score index dict")
            for k,v in score_index_dict.items():
                print("score ",k," :index ",v)

        if self.debug:
            print("index weight length dict")
            for k,v in index_weight_length_dict.items():
                print("index ",k," :weight,length ",v)
            
            
        completion_times = []
        for i in range(self.njobs):
            score = heap.get_root()
            if self.debug:
                print("maximum score", score)
                """There is a problem in swapList or index list update"""
            index_list = score_index_dict[score]
            if self.debug:
                print("index list of score", score,'is: ',index_list)
            weight_length_list = [index_weight_length_dict[index] for index in index_list]
            
            weights = [w for w,_ in weight_length_list]
            index_max = np.argmax(weights)
            _max = np.max(weights)
            if self.debug:
                print("max weight ",_max)
                print("index of max",index_max)
            w,l = _max, weight_length_list[index_max][1]
            
            
            
            if i == 0:
                completion_times.append((w,l))
            else:
                completion_times.append((w,completion_times[i-1][1]+l))
                
            # We should restore the indices 
            if self.debug:
                print("minimum index to delete ",index_list[index_max])
            swapList = heap.delete(index_list[index_max])
            index_to_delete = index_list[index_max]
            
            if index_to_delete != heap.n_elements:
                index_weight_length_dict[heap.n_elements],index_weight_length_dict[index_list[index_max]] = index_weight_length_dict[index_list[index_max]],index_weight_length_dict[heap.n_elements]
                
            del index_weight_length_dict[heap.n_elements]
            
            if self.debug:
                print("index to delete", index_to_delete)
                print(heap.n_elements)
            if len(score_index_dict[score]) == 1:
                del score_index_dict[score]
            else:
                
                del score_index_dict[score][index_max]
                
            if index_to_delete != heap.n_elements:
                if score_number == 1:
                    
                    score_index_dict[self.job_score_1(*index_weight_length_dict[index_to_delete])].append(index_to_delete)
                    score_index_dict[self.job_score_1(*index_weight_length_dict[index_to_delete])].remove(heap.n_elements)
                    
                else:
                    score_index_dict[self.job_score_2(*index_weight_length_dict[index_to_delete])].append(index_to_delete)
                    score_index_dict[self.job_score_2(*index_weight_length_dict[index_to_delete])].remove(heap.n_elements)
                    
            if self.debug:
                print("swapList",swapList)
            if self.debug:
                print("score index dict")
                for k,v in score_index_dict.items():
                    print("score ",k," :index ",v)
                
        
            if swapList:
                for idx1,idx2 in swapList:
                    index_weight_length_dict[idx1],index_weight_length_dict[idx2] = index_weight_length_dict[idx2],index_weight_length_dict[idx1]
                    if score_number==1:
                        
                        score_index_dict[self.job_score_1(*index_weight_length_dict[idx2])].append(idx2)
                        
                        score_index_dict[self.job_score_1(*index_weight_length_dict[idx2])].remove(idx1)
                        
                        score_index_dict[self.job_score_1(*index_weight_length_dict[idx1])].append(idx1)
                        
                        score_index_dict[self.job_score_1(*index_weight_length_dict[idx1])].remove(idx2)
                        
                    else:
                        score_index_dict[self.job_score_2(*index_weight_length_dict[idx2])].append(idx2)
                        score_index_dict[self.job_score_2(*index_weight_length_dict[idx2])].remove(idx1)
                        score_index_dict[self.job_score_2(*index_weight_length_dict[idx1])].append(idx1)
                        score_index_dict[self.job_score_2(*index_weight_length_dict[idx1])].remove(idx2)
                if self.debug:
                    print("score index dict")
                    for k,v in score_index_dict.items():
                        print("score ",k," :index ",v)
                    print("heap number of elements: ",heap.n_elements)
        completion_times_sum = 0
        for w,c in completion_times:
            completion_times_sum += w*c
        return completion_times_sum

    def execute_2(self):
        pass

class MST_heap:
    def __init__(self,filename=None,debug=False):
        self.debug = debug
        #filename = wget.download(url)
        f = open(filename, 'r')
        self.lines = f.readlines()
        self.n_nodes,self.n_edges = tuple(map(int,self.lines[0].split()))
        self.heap = Heap()
        print(len(self.lines))
        # dictionary of each node to another node with the cost of the edge
        self.node_node_cost_dict = dict()
        # dictionary of cost to nodes
        self.cost_node_dict = dict()
        # dictionary of each cost of corresponding index in heap
        self.node_index_dict = dict()
        self.index_node_dict = dict()
        self.V = set()
        self.populate_edge_cost_dict()
        self.s = random.choice(list(self.V))
        
        
        self.V.remove(self.s)
        self.populate_heap(self.s, self.V)

        
        
    def populate_edge_cost_dict(self):
        for i in range(1,len(self.lines)):
            node1,node2,cost = tuple(map(int,self.lines[i].split()))
            if self.debug:
                print(node1,node2,cost)
            if node1 in self.node_node_cost_dict:
                self.node_node_cost_dict[node1].append((node2,cost))
            else:
                self.node_node_cost_dict[node1] = [(node2,cost)]
            if node2 in self.node_node_cost_dict:
                self.node_node_cost_dict[node2].append((node1,cost))
            else:
                self.node_node_cost_dict[node2] = [(node1,cost)]
            self.V.add(node1)
            self.V.add(node2)
        if self.debug:
            for v in self.V:
                print("nodes adjacent to ",v," are :",[i for i,_ in self.node_node_cost_dict[v]])
            

            
                
    def populate_heap(self,s,V):
        
        adjacent_edges_cost = [cost for _,cost in self.node_node_cost_dict[s]]
        adjacent_nodes = [node for node,_ in self.node_node_cost_dict[s]]
        
        for node in V:
            if node in adjacent_nodes:
                cost = adjacent_edges_cost[adjacent_nodes.index(node)]  
            else:
                cost = float('inf')
                
            if cost in self.cost_node_dict:
                self.cost_node_dict[cost].append(node)
            else:
                self.cost_node_dict[cost]=[node]
                
            self.heap.insert(cost)
            
        for i in range(self.heap.n_elements):
            heapList = self.heap.heap
            cost = heapList[i]
            nodes = self.cost_node_dict[cost]
            for node in nodes:
                if node not in self.node_index_dict:
                    #print("Node ",node,"i",i)
                    self.node_index_dict[node] = i
                    self.index_node_dict[i] = node
                    break
        print(len(list(self.node_index_dict.keys())),self.n_nodes)
                
        if self.debug:
            print(self.heap.heap)
        if self.debug:
            print("populate heap")
            for k,v in self.index_node_dict.items():
                print("index ",k,"is associated with ",v)
            print(self.heap.heap)
            
            
            
                
            
        
    def update_heap(self):
        index_to_delete = 0
        swapList = self.heap.delete(index_to_delete)
        #if self.debug:
        #print("elements to swap after delete",self.index_node_dict[self.heap.n_elements],self.index_node_dict[index_to_delete] )
        self.index_node_dict[self.heap.n_elements],self.index_node_dict[index_to_delete] = self.index_node_dict[index_to_delete],self.index_node_dict[self.heap.n_elements]
        self.node_index_dict[self.index_node_dict[index_to_delete]] = index_to_delete
        #if self.debug:
            #print(self.index_node_dict[self.heap.n_elements])
            #print(self.index_node_dict[index_to_delete])
        del self.node_index_dict[self.index_node_dict[self.heap.n_elements]]
        u = self.index_node_dict[self.heap.n_elements]
        self.V.remove(u)
        del self.index_node_dict[self.heap.n_elements]
        if swapList:
            #if self.debug:
                #print(swapList)
            for i,j in swapList:
                self.index_node_dict[i],self.index_node_dict[j] = self.index_node_dict[j],self.index_node_dict[i]
                self.node_index_dict[self.index_node_dict[i]] = i
                self.node_index_dict[self.index_node_dict[j]] = j
        if self.debug:
            print("nodes adjacent to ",u ,[node for node,_ in self.node_node_cost_dict[u]])
            print("V", self.V)
        
        for node,newcost in self.node_node_cost_dict[u]:
            if node in self.V:
                if self.debug:
                    print("Node ",node)
                index_to_delete = self.node_index_dict[node]
                #print("index_to_delete",index_to_delete)
                #if not self.debug:
                    #print("heap",self.heap.heap)
                    #print("index_to_delete",index_to_delete)
                    #print("Node",node)
                
                cost = self.heap.heap[index_to_delete] 
                
                if newcost == min(cost,newcost):
                    swapList = self.heap.delete(index_to_delete)
                    #print("heap after deletion",self.heap.heap)
                    if self.debug:
                        print("###################################")
                        print("swapList",swapList)
                        print("###################################")
                    self.index_node_dict[self.heap.n_elements],self.index_node_dict[index_to_delete] = self.index_node_dict[index_to_delete],self.index_node_dict[self.heap.n_elements]
                    self.node_index_dict[self.index_node_dict[index_to_delete]] = index_to_delete
                    self.node_index_dict[node] = self.heap.n_elements
                    if swapList:
                        for i,j in swapList:
                            self.index_node_dict[i],self.index_node_dict[j] = self.index_node_dict[j],self.index_node_dict[i]
                            self.node_index_dict[self.index_node_dict[i]] = i
                            self.node_index_dict[self.index_node_dict[j]] = j
                    
                    swapList = self.heap.insert(newcost)
                    #print("heap after insertion of new cost",self.heap.heap)
                    #self.index_node_dict[self.heap.n_elements-1] = node
                    #self.node_index_dict[node] = self.heap.n_elements-1
                    if swapList:
                        if self.debug:
                            print("###################################")
                            print("swapList for insert",swapList)
                            print("###################################")
                        for i,j in swapList:
                            self.index_node_dict[i],self.index_node_dict[j] = self.index_node_dict[j],self.index_node_dict[i]
                            self.node_index_dict[self.index_node_dict[i]] = i
                            self.node_index_dict[self.index_node_dict[j]] = j
                if self.debug:
                    print("index of node",node,"is: ",self.node_index_dict[node])
                    
                    
        if  self.debug:
            print(self.heap.heap)
        
        if  self.debug:
            print("update heap")
            for k,v in self.index_node_dict.items():
                print("index ",k,"is associated with ",v)
            print(self.heap.heap)
        
    def execute(self):
        MST_cost = 0 
        while len(self.V)>0:
            # select the cheapest edge e that cross X and V/X
            cost = self.heap.get_root()
            MST_cost += cost
            self.update_heap()
        return MST_cost
            
class MST_list:
    def __init__(self,url=None,debug=False):
        self.debug = debug
        filename = wget.download(url)
        f = open(filename, 'r')
        self.lines = f.readlines()
        self.n_nodes,self.n_edges = tuple(map(int,self.lines[0].split()))
        self.cost_list = []
        # dictionary of each node to another node with the cost of the edge
        self.node_node_cost_dict = dict()
        # dictionary of cost to nodes
        #self.cost_node_dict = dict()
        # dictionary of each cost of corresponding index in heap
        #self.node_index_dict = dict()
        #self.index_node_dict = dict()
        self.V = set()
        self.populate_edge_cost_dict()
        self.s = random.choice(self.V)
        self.V.remove(self.s)
        self.populate_cost_list()     
        
    def populate_edge_cost_dict(self):
        print("populate")
        for i in range(1,len(self.lines)):
            node1,node2,cost = tuple(map(int,self.lines[i].split()))
            if self.debug:
                print(node1,node2,cost)
            if node1 in self.node_node_cost_dict:
                self.node_node_cost_dict[node1].append((node2,cost))
            else:
                self.node_node_cost_dict[node1] = [(node2,cost)]
            if node2 in self.node_node_cost_dict:
                self.node_node_cost_dict[node2].append((node1,cost))
            else:
                self.node_node_cost_dict[node2] = [(node1,cost)]
            self.V.add(node1)
            self.V.add(node2)
        self.V = list(self.V)
        
    def populate_cost_list(self):
        adjacent_edges_cost = [cost for _,cost in self.node_node_cost_dict[self.s]]
        adjacent_nodes = [node for node,_ in self.node_node_cost_dict[self.s]]
        self.cost_list = [0]*len(self.V)
        for node in self.V:
            if node in adjacent_nodes:
                cost = adjacent_edges_cost[adjacent_nodes.index(node)]  
            else:
                cost = float('inf')
                
            self.cost_list[self.V.index(node)] = cost
            
    def update_cost_list(self):
        minCost = min(self.cost_list)
        minIndex = self.cost_list.index(minCost)
        minNode = self.V[minIndex]
        del self.V[minIndex]
        del self.cost_list[minIndex]
        
        for node,newcost in self.node_node_cost_dict[minNode]:
            if node in self.V:
                cost = self.cost_list[self.V.index(node)]
                if newcost == min(newcost,cost):
                    self.cost_list[self.V.index(node)] = newcost
        return minCost
                    
    def execute(self):
        print("execute")
        MST_cost = 0 
        while len(self.V)>0:
            # select the cheapest edge e that cross X and V/X
            MST_cost += self.update_cost_list()
        print("MST_cost",MST_cost)
        return MST_cost
        
        
        
if __name__ == "__main__":
    debug = False
    J = Jobs(filename ="jobs.txt",debug = debug)
    print(J.execute(score_number=1))
    print(J.execute(score_number=2))
    M = MST_list(url = "https://d3c33hcgiwev3.cloudfront.net/_d4f3531eac1d289525141e95a2fea52f_edges.txt?Expires=1659052800&Signature=NlE9jRyY3WhpkcEwlcNtxH9pBMtlOLzSpeCv3Y5M16TtIzEu74lP1NVTdjCklyM0YYosVzl6AJL-ttfk5vppoSTwDS4mhEAbVARRYCiq6-ecK1a7dceZL007qSfIpBFO4l5OYGsaZH88wZzgv-~217qbhk6LfEEkNDuVGwcn3T0_&Key-Pair-Id=APKAJLTNE6QMUY6HBC5A"  ,debug = False)
    print(M.execute())

    
    