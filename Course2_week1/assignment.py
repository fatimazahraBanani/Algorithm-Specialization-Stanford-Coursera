# -*- coding: utf-8 -*-
"""
Created on Mon Sep 27 14:08:18 2021

@author: Banani Fatima-Zahra
"""
import sys
import threading
import wget



class TwoPass:
    def __init__(self,url,debug,number_nodes):
        self.number_nodes = number_nodes
        self.debug = debug
        filename = wget.download(url)
        file = open(filename, 'r')
        
        self.ordering = [0]*self.number_nodes
        self.rev_graph = {i: [[], False] for i in range(1,self.number_nodes+1)} #reversed graph node: [list of next nodes , explored boolean]
        
        self.leader = dict() # leader node : number of nodes
        self.graph = {i: [[], False] for i in range(1,self.number_nodes+1)} #original graph node: [list of next nodes , explored boolean]
        
        self.current_timing = -1
        self.current_leader = None
        
        for line in file:
            u, v  = tuple(map(int,line.strip().split()))
            self.graph[u][0].append(v)
            self.rev_graph[v][0].append(u)
        
    def DFS_Loop(self,order):
        '''
        Create the Depth First Search loop
        '''
        if order == 1:
            for u in range(self.number_nodes,0,-1):
                if not self.rev_graph[u][1]:
                    self.DFS(order = 1 , node = u)
            
        else:
            for i in range(self.number_nodes-1,-1,-1):
                u = self.ordering[i]
                if not self.graph[u][1]:
                    self.current_leader = u
                    self.leader[u] = 0
                    self.DFS(order = 2 , node = u)
        
    
    def DFS(self, order, node):
        '''
        Create the Depth First Search iteration
        '''
        if order == 1:
            self.rev_graph[node][1] = True
            for node_next in self.rev_graph[node][0]:
                if not self.rev_graph[node_next][1]:
                    self.DFS(order = 1, node = node_next)
            self.current_timing += 1
            self.ordering[self.current_timing] = node
        else:
            self.graph[node][1] = True
            self.leader[self.current_leader] += 1
            for node_next in self.graph[node][0]:
                if not self.graph[node_next][1]:
                    self.DFS(order = 2, node = node_next)
def main():
    TP = TwoPass(url = 'https://d3c33hcgiwev3.cloudfront.net/_410e934e6553ac56409b2cb7096a44aa_SCC.txt?Expires=1632873600&Signature=Vu2PHqNLk-KddLRyc~Bc1kVJZ0zIyVxNeo7CLTbVIjhimXBo2LYqrb~pu516x0jWKiPu6ZscVn0U0QWyjybKCMjeFxb9SXIRVc5OjyobmGy6Rrms91eJkfYz0c694vOpznS3U1U9nwmlIgud-rhXjjfq8VPEfs~XPDk1T25ZLy8_&Key-Pair-Id=APKAJLTNE6QMUY6HBC5A', debug = False, number_nodes= 875714)
    # First loop on the reversed graph to compute the finishing time.
    TP.DFS_Loop(1)
    # Second loop to determine the leaders of each strongly connected component.
    TP.DFS_Loop(2)
    maxi = [v for _, v in sorted(TP.leader.items(), key=lambda item: item[1], reverse=True)][:5]
    print(maxi)

if __name__ == "__main__":
    
    threading.stack_size(67108864)        
    sys.setrecursionlimit(2 ** 20)        
    thread = threading.Thread(target=main)        
    thread.start()

    
    
    
    
    