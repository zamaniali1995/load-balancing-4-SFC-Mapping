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
from Heuristic import Two_step_algorithm
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
print(k_path[('1', '4')][0])
# print(graph.link_list[0].ban)
# algorithm = Two_step_algorithm()
# start = time.time()
# algorithm.create(graph, chains, k_path, functions)
# end = time.time()
# print("Heuristic time", end - start)
# print(len(functions))
# print(k_path["1", "3"])
# print(graph.node_list[0].cap)
# print(chains[0].fun)
# for v in k_path[('1', '14')][0]:
#     print(v)
# print(len(chains[0].fun))
ILP = ILP_Model()
# graph.link_list[0].cap = 1
# graph.link_list[0].cap = graph.link_list[0].cap + 1
# print(graph.link_list[0].cap)

# print("ILP run time = ", end - start)
print(graph.node_list[0].fun)
graph.make_empty_nodes()
start = time.time()
ILP.create(graph, functions, chains, k_path)
end = time.time()
print("ILP run time = ", end - start)
# CG = CG_Model()
# CG.create(graph, functions, chains, k_path)
# for i in range(14*14):
#     print(chains[0].users[i])

# //					{"2":[ "1","3","4","5","6","7","8","9","10","11","12","13","14"] },
# //					{"3":[ "1","2","4","5","6","7","8","9","10","11","12","13","14"] },
# //					{"4":[ "1","2","3","5","6","7","8","9","10","11","12","13","14"] },
# //					{"5":[ "1","2","3","4","6","7","8","9","10","11","12","13","14"] },
# //					{"6":[ "1","2","3","4","5","7","8","9","10","11","12","13","14"] },
# //					{"7":[ "1","2","3","4","5","6","8","9","10","11","12","13","14"] },
# //					{"8":[ "1","2","3","4","5","6","7","9","10","11","12","13","14"] },
# //					{"9":[ "1","2","3","4","5","6","7","8","10","11","12","13","14"] },
# //					{"10":[ "1","2","3","4","5","6","7","8","9","11","12","13","14"] },
# //					{"11":[ "1","2","3","4","5","6","7","8","9","10","12","13","14"] },
# //					{"12":[ "1","2","3","4","5","6","7","8","9","10","11","13","14"] },
# //					{"13":[ "1","2","3","4","5","6","7","8","9","10","11","12","14"] },
# //					{"14":[ "1","2","3","4","5","6","7","8","9","10","11","12","13"] }