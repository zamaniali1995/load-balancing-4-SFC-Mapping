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
from PaperFunctions import Graph, Chains, Functions
from Heuristic import Two_step_algorithm
import time

#import matplotlib.pyplot as plt
###############################################################
# Reading input files
###############################################################
input_cons = InputConstants.Inputs()
heuristic_loads = []
ILP_loads = []
funs = Functions()
funs.generate()
funs.read(input_cons.functions_random_path + input_cons.functions_random_name) 
for i in range(input_cons.run_num):
    graph = Graph(input_cons.network_path + input_cons.network_name, 
                funs)
    chain = Chains(graph, funs)
    chain.generate()
    chain.read(input_cons.chains_random_path + input_cons.chains_random_name)
    graph.make_empty_network()
    algorithm = Two_step_algorithm()
    heuristic_loads.append(algorithm.run(graph, chain, funs))
    ILP = ILP_Model()
    graph.make_empty_network()
    ILP_loads.append(ILP.run(graph, chain, funs))
    print('epoch: {} / {}'.format(i+1, input_cons.run_num))
# print(ILP_loads)
# print(heuristic_loads)
print("max load node ILP: {}".format(max(map(lambda x: x[0], ILP_loads))))
print("max load link ILP: {}".format(max(map(lambda x: x[1], ILP_loads))))
print("avg load node ILP: {}".format(sum(map(lambda x: x[0], ILP_loads)) / len(ILP_loads)))
print("avg load link ILP: {}".format(sum(map(lambda x: x[1], ILP_loads)) / len(ILP_loads)))
print("avg time ILP: {}".format(sum(map(lambda x: x[2], ILP_loads)) / len(ILP_loads)))

print("max load node heuristic: {}".format(max(map(lambda x: x[0], heuristic_loads))))
print("max load link heuristic: {}".format(max(map(lambda x: x[1], heuristic_loads))))
print("avg load node heuristic: {}".format(sum(map(lambda x: x[0], heuristic_loads)) / len(heuristic_loads)))
print("avg load link heuristic {}".format(sum(map(lambda x: x[1], heuristic_loads)) / len(heuristic_loads)))
print("avg time heuristic: {}".format(sum(map(lambda x: x[2], heuristic_loads)) / len(heuristic_loads)))
