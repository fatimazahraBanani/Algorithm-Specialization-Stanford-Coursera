# -*- coding: utf-8 -*-
"""
Created on Thu Sep 23 13:22:04 2021

@author: Banani Fatima-Zahra
"""
from collections import OrderedDict
import random

class MinCut:
    def __init__(self,filename,debug):
        file = open(filename, 'r')
        adjacency_dict = OrderedDict()
        number_edges = 0
        self.number_adjacents = OrderedDict()
        for line in file:
            array = list(map(int,line.strip().split()))
            adjacency_dict[array[0]] = array[1:]
            number_edges += len(array) - 1
            self.number_adjacents[array[0]] = len(array) - 1
        self.adjacency_dict = adjacency_dict
        self.number_vertices = len(self.adjacency_dict.keys())
        self.initial_number_vertices = len(self.adjacency_dict.keys())
        self.number_edges = number_edges/2
        self.debug = debug
        
        
    def randomMinCut(self,seed):
        # Apply the Randomized Min Cut Algorithm
        i = 1
        random.seed(seed)
        while self.number_vertices > 2 :
            #Randomly pick an edge from the remaining edges
            randomNumber = random.randrange(1, 2*self.number_edges + 1)
            u,v = self.chooseEdge(randomNumber)
            if self.debug:
                print("u,v are: ",u,v)
                print(v in self.adjacency_dict[u])
                
            #Apply the edge contraction
            i += 1
            self.edgeContraction(u, v, i)
        return 0
    
    def chooseEdge(self,randomNumber):
        # given the random number we choose the corresponding edge
        
        #if self.debug:
            #for vertex in self.number_adjacents:
                #print(vertex,self.number_adjacents[vertex])
        keys = list(self.number_adjacents.keys())
        values = list(self.number_adjacents.values())
        
        L = []
        s = 0
        for value in values:
            s += value
            L.append(s)
        
        if self.debug: 
            print("This should be true", (L[-1] == self.number_edges*2))
            
        for i in range(len(L)):
            if randomNumber <= L[i]:
                break
        
        # i corresponds to the key
        chosen_u = keys[i]
        choices_v = list(self.adjacency_dict[chosen_u])
        chosen_v = choices_v[randomNumber - L[i] - 1]
        
        return chosen_u,chosen_v
        
        
            
        
    def edgeContraction(self,u,v,i):
        #Modify the adjacency dictionary after an edge contraction
        adjacent_vertices = list(self.adjacency_dict[u])+(list(self.adjacency_dict[v]))
        
        # substract the number of self loops from the number of edges
        number_self_loop = sum([1 for vertex in adjacent_vertices if (vertex == u)])
        self.number_edges -= number_self_loop
        
        
        adjacent_vertices = set(adjacent_vertices).difference({u,v})
        #if self.debug:
            #print(adjacent_vertices)
        
        # add the list of adjacent vertices to the new contracted vertex
        self.adjacency_dict[self.initial_number_vertices + i] = [] 
        
        for vertex in adjacent_vertices:
            array = self.adjacency_dict[vertex]
            indices = [j for j, x in enumerate(array) if (x == u) or (x == v)]
            for index in indices:
                array[index] = self.initial_number_vertices + i
                self.adjacency_dict[self.initial_number_vertices + i].append(vertex)
            self.adjacency_dict[vertex] = array
        
        self.number_adjacents[self.initial_number_vertices + i] = len(self.adjacency_dict[self.initial_number_vertices + i])
        # delete u and v from the adjacency dictionary
        del self.adjacency_dict[u]
        del self.adjacency_dict[v]
        del self.number_adjacents[u]
        del self.number_adjacents[v]
            
        self.number_vertices -= 1
    

if __name__ == "__main__":
    debug = False
    MC = MinCut(filename = "kargerMinCut.txt",debug = False)
    if debug:
        print(MC.adjacency_dict.keys())
    mini = MC.number_edges
    for i in range(1,1000,10):
        MC = MinCut(filename = "kargerMinCut.txt",debug = False)
        MC.randomMinCut(seed = i)
        mini = min(mini, MC.number_edges)
    print(mini)
    