#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 27 16:44:41 2019

@author: ali

@email: zamaniali1995@gmail.com
"""
###############################################################
# Import packages
###############################################################
import sys
sys.path.insert(0, './PaperFunctions')
sys.path.insert(1, './Given')
sys.path.insert(1, './Model')
from Models import ILP_Model, CG_Model
import InputConstants
from PaperFunctions import Graph, Chains
import time

#import matplotlib.pyplot as plt
###############################################################
# Reading input files
###############################################################
input_cons = InputConstants.Inputs()
_chain = Chains()
functions = _chain.read_funcions(input_cons.chains_path + input_cons.chains_name)

graph = Graph(input_cons.network_path + input_cons.network_name, 
              functions)
chains = _chain.read_chains(input_cons.chains_path + input_cons.chains_name, 
                     graph)
k_path = graph.k_path(input_cons.k_path_num)
# print(k_path["1", "3"])
# print(graph.node_list[0].cap)
# print(chains[0].fun)
# for v in k_path[('1', '14')][0]:
#     print(v)
# print(len(chains[0].fun))
ILP = ILP_Model()
start = time.time()
# ILP.create(graph, functions, chains, k_path)
end = time.time()
print("ILP run time = ", end - start)
CG = CG_Model()
CG.create(graph, functions, chains, k_path)
# for i in range(14*14):
#     print(chains[0].users[i])

