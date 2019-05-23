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
import numpy as np
import matplotlib.pyplot as plt
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
heu_info = []
ILP_info = []
funs = Functions()
funs.generate()
funs.read(input_cons.functions_random_path + input_cons.functions_random_name) 
labels = []
results_links = []
results_nodes = []
for u, user_num in enumerate(input_cons.user_num):
    print('##############')
    print('number of users: {}'.format(user_num))
    for i in range(input_cons.run_num):
        graph = Graph(input_cons.network_path + input_cons.network_name, 
                    funs, u)
        chain = Chains(graph, funs)
        chain.generate(user_num)
        chain.read(input_cons.chains_random_path + input_cons.chains_random_name)
        graph.make_empty_network()
        algorithm = Two_step_algorithm()
        heu_info.append(algorithm.run(graph, chain, funs))
        ILP = ILP_Model()
        graph.make_empty_network()
        ILP_info.append(ILP.run(graph, chain, funs))
        print('epoch: {} / {}'.format(i+1, input_cons.run_num))
    # print(ILP_loads)
    # print(heuristic_loads)
    # spread = range(0, 100)
    # center = sum(map(lambda x: x[1], ILP_loads)) / len(ILP_loads)
    # flier_high = max(map(lambda x: x[0], ILP_loads))
    # flier_low = min(map(lambda x: x[0], ILP_loads))
    # print(np.percentile(ILP_loads, 50))
    cpu_heu = list(map(lambda x: x[0], heu_info))
    time_heu = list(map(lambda x: x[2], heu_info))
    link_heu = list(map(lambda x: x[1], heu_info))
    cpu_ILP = list(map(lambda x: x[0], ILP_info))
    time_ILP = list(map(lambda x: x[2], ILP_info))
    link_ILP = list(map(lambda x: x[1], ILP_info))
    # print(cpu_list)
    # data = np.concatenate((100, center, flier_high, flier_low))
    results_nodes.append((
                 max(cpu_ILP),
                 np.percentile(cpu_ILP, 75),
                 np.percentile(cpu_ILP, 50), 
                 np.percentile(cpu_ILP, 25), 
                 min(cpu_ILP)
                 )
    )
    results_nodes.append((
                 max(cpu_heu),
                 np.percentile(cpu_heu, 75),
                 np.percentile(cpu_heu, 50), 
                 np.percentile(cpu_heu, 25), 
                 min(cpu_heu))
                 )
    results_links.append((
                 max(link_ILP),
                 np.percentile(link_ILP, 75),
                 np.percentile(link_ILP, 50), 
                 np.percentile(link_ILP, 25), 
                 min(link_ILP)
                 )
    )
    results_links.append((
                 max(link_heu),
                 np.percentile(link_heu, 75),
                 np.percentile(link_heu, 50), 
                 np.percentile(link_heu, 25), 
                 min(link_heu))
                 )
                 
    labels.append((str(user_num)+ ':I' ))
    labels.append((str(user_num)+ ':H' ))
    
    # print("max load node ILP: {}".format(max(map(lambda x: x[0], ILP_loads))))
    # print("max load link ILP: {}".format(max(map(lambda x: x[1], ILP_loads))))
    # print("avg load node ILP: {}".format(sum(map(lambda x: x[0], ILP_loads)) / len(ILP_loads)))
    # print("avg load link ILP: {}".format(sum(map(lambda x: x[1], ILP_loads)) / len(ILP_loads)))
    # print("avg time ILP: {}".format(sum(map(lambda x: x[2], ILP_loads)) / len(ILP_loads)))

    # print("max load node heuristic: {}".format(max(map(lambda x: x[0], heuristic_loads))))
    # print("max load link heuristic: {}".format(max(map(lambda x: x[1], heuristic_loads))))
    # print("avg load node heuristic: {}".format(sum(map(lambda x: x[0], heuristic_loads)) / len(heuristic_loads)))
    # print("avg load link heuristic {}".format(sum(map(lambda x: x[1], heuristic_loads)) / len(heuristic_loads)))
    # print("avg time heuristic: {}".format(sum(map(lambda x: x[2], heuristic_loads)) / len(heuristic_loads)))
fig1, ax1 = plt.subplots()
ax1.set_title('nodes load')
plt.xlabel('number of users: I(MILP) / H(Heuristic)')
plt.ylabel('cpu usage(%)')
ax1.boxplot(results_nodes, labels=labels)
plt.savefig('nodes_cap.pdf')
plt.show()
plt.close()
fig2, ax2 = plt.subplots()
ax2.set_title('links load')
plt.xlabel('number of users: I(MILP) / H(Heuristic)')
plt.ylabel('bandwidth usage(%)')
ax1.boxplot(results_links, labels=labels)
plt.savefig('links_cap.pdf')
plt.show()
plt.close()
        