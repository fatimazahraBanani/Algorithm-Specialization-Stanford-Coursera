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

class UnionFind:
    def __init__(self, debug=False, nodes = None):
        self.debug = debug
        self.nodes = nodes
        self.node_leader_dict = {node : node for node in self.nodes}
        self.leader_cluster_dict = {node: [node] for node in self.nodes}
        
    def check_if_same_cluster(self,u,v):
        return (self.node_leader_dict[u] == self.node_leader_dict[v])
    
    def fuse_clusters(self,u,v):
        if self.debug:
            print("fuse ",u,v)
        leader_u = self.node_leader_dict[u]
        leader_v = self.node_leader_dict[v]
        
        cluster_u = self.leader_cluster_dict[leader_u]
        cluster_v = self.leader_cluster_dict[leader_v]
        
        if self.debug:
            print("before fusion") 
            for k,val in self.leader_cluster_dict.items():
                print("leader ",k," is associated with cluster ",val)
               
        if len(cluster_u) <= len(cluster_v):
            selected_cluster, selected_leader = cluster_u, leader_v
            not_selected_leader = leader_u
        else:
            selected_cluster, selected_leader = cluster_v, leader_u
            not_selected_leader = leader_v
            
        for node in selected_cluster:
            self.node_leader_dict[node] = selected_leader
        del self.leader_cluster_dict[not_selected_leader]
        self.leader_cluster_dict[selected_leader].extend(selected_cluster)
        
        if self.debug:
            print("after fusion") 
            for k,val in self.leader_cluster_dict.items():
                print("leader ",k," is associated with cluster ",val)

class MaxSpacingClustering:
    def __init__(self,url=None,debug=False,k=1):
        self.debug = debug
        filename = wget.download(url)
        f = open(filename, 'r')
        lines = f.readlines()
        self.nnodes = int(lines[0].strip('\n'))
        self.lines = [list(map(int, x.strip('\n').split())) for x in lines[1:]]
        self.distance_node_node_dict = dict()
        self.distances = []
        self.k = k
        self.unionfind = None
        self.initialize_attributes()
        
    def initialize_attributes(self):
        nodes = set()
        for i in range(len(self.lines)):
            #node1,node2,cost = tuple(map(int,self.lines[i].split()))
            node1,node2,distance = self.lines[i]
            nodes.add(node1)
            nodes.add(node2)
            self.distances.append(distance)
            if self.debug:
                print(node1,node2,distance)
            if distance in self.distance_node_node_dict :
                self.distance_node_node_dict[distance].append((node1,node2))
            else:
                self.distance_node_node_dict[distance] = [(node1,node2)]
        self.unionfind = UnionFind(nodes = list(nodes))
       
    def execute(self):
        # sort distances ascendently
        self.distances.sort()
        if self.debug:
            print(self.distances)
        # check current number of clusters from unionfind 
        index = 0
        while len(self.unionfind.leader_cluster_dict)>=self.k:
            # select next minimum distance of separated points
            separated = False
            while not separated:
                distance = self.distances[index]
                if self.debug:
                    print("Current distance",distance)
                node1,node2 = self.distance_node_node_dict[distance][0]
                separated = not self.unionfind.check_if_same_cluster(node1, node2)
                index += 1
                del self.distance_node_node_dict[distance][0]
             
            # merge the two clusters
            if len(self.unionfind.leader_cluster_dict)>self.k:
                self.unionfind.fuse_clusters(node1, node2)
            else:
                index -= 1
                break
        
        # return next minimum distance
        return self.distances[index]
        
class ClusteringBig:
    def __init__(self, url = None, debug = False):
        self.debug = debug
        filename = wget.download(url)
        f = open(filename, 'r')
        lines = f.readlines()
        self.nnodes,self.nbits = tuple(map(int,lines[0].strip('\n').split()))
        #if self.debug:
            #print("Number of nodes ",self.nnodes," Number of bits ",self.nbits)
        self.nodes = [list(map(int,x.strip('\n').split())) for x in lines[1:]]
        #if self.debug:
            #print("Number of nodes in nodes list ",len(self.nodes),len(self.nodes[0]))
        self.unionfind = UnionFind(nodes= list(map(self.binary_digit,self.nodes)))
        self.code_vertice_dict = dict()
        
    def create_distance_1(self,node):
        """
        create all possible values at distance 1 of node 
        output list of values + node
        """
        values = []
        for i in range(self.nbits):
            values.append(tuple(node[:i]+[1-node[i]]+node[i+1:]))
        return values
    
    def create_distance_1_2(self,node):
        """
        create all possible values at distance 2 of node
        """
        values = set()
        values.update(self.create_distance_1(node))
        list_values = list(values)
        for val in list_values:
            values.update(self.create_distance_1(list(val)))
        values.update([tuple(node)])
        return list(values)
    
    def binary_digit(self,node):
        return int("".join(str(bit) for bit in node), 2) 
    
    def execute(self):
        n_cluster = self.nnodes
        previous_possible_values = set()
        self.unionfind
        for node in self.nodes:
            if tuple(node) in previous_possible_values:
                n_cluster -= 1
                for v in self.code_vertice_dict[self.binary_digit(tuple(node))]:
                    u = self.binary_digit(tuple(node))
                    if not self.unionfind.check_if_same_cluster(u, v):
                        self.unionfind.fuse_clusters(u, v)
            values = self.create_distance_1_2(node)
            previous_possible_values.update(values)
            for v in values:
                if self.binary_digit(v) in self.code_vertice_dict:
                    self.code_vertice_dict[self.binary_digit(v)].append(self.binary_digit(tuple(node)))
                else:
                    self.code_vertice_dict[self.binary_digit(v)] = [self.binary_digit(tuple(node))]
        
        return len(self.unionfind.leader_cluster_dict)
        
                
        
if __name__ == "__main__":
    debug = False
    M = MaxSpacingClustering(url = "https://d3c33hcgiwev3.cloudfront.net/_fe8d0202cd20a808db6a4d5d06be62f4_clustering1.txt?Expires=1659571200&Signature=Gth7H1oD4kfYSUL4ypQfMOdgjMJTu1cqgNc0sSH8s1iWnYUZiHfepdP7bsI8ahZJLIMwVr5bSGsSC1muMRafnhjGIIl8JTDWJaTtkSzEE4I8GkuSUvWSdPAApMOHQhOxRRZiV2dg7ed65XGS-PgCMe2CfEetISMyYdnQpw5Kl8c_&Key-Pair-Id=APKAJLTNE6QMUY6HBC5A" ,debug = False, k=4)
    print(M.execute())
    C = ClusteringBig(url="https://d3c33hcgiwev3.cloudfront.net/_fe8d0202cd20a808db6a4d5d06be62f4_clustering_big.txt?Expires=1659830400&Signature=F~i7h6yBJT~uHaOG6jmQ3nJ~ZO5V9gr7M-dM3InrDhSC0X1qR2SN-Wv6ZGHOWcXtXYJpuDqAYvJKUpeh5sFMpqzkLb2do9zGP2sOu6XriEEH2ZxIzNjqsB-~X2U1ha67xtUlhkCjOGtyKud5O87w6x-Lev3y2KW4o4T~vDQ1AVQ_&Key-Pair-Id=APKAJLTNE6QMUY6HBC5A",debug=True)
    print(C.execute())
    
    
    

    
    