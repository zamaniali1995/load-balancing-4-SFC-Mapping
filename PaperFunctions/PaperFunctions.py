#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 27 19:24:24 2019

@author: ali

"""

###############################################################
# Import packages
###############################################################
from typing import List

import numpy as np
import InputConstants
import json
import random as rd
import networkx as nx
###############################################################
# Node features class
###############################################################
class _Node:
    def __init__(self, name, cap_cpu, cap_mem):
        self.name = name
        self.cap_cpu = cap_cpu
        self.cap_mem = cap_mem
        self.fun = {}
###############################################################
# Link features class
###############################################################
class _Link:
    def __init__(self, name, cap, bandwidth, length):
        self.cap = cap
        self.ban = bandwidth
        self.length = length
        self.name = name

###############################################################
# Chain features class
###############################################################
class _Chain:
    def __init__(self, name, function, traffic, users):
        self.name = name
        self.fun = function
        self.tra = traffic
        self.users = users
        
###############################################################
# Graph class:|
#             |__>functions:-->
#                           -->  
###############################################################
class Graph:

    def __init__(self, path, funs):
        self.funs = funs
        self.rev_to_cost_val = 0
        self.input_cons = InputConstants.Inputs()
        link_list = []
        node_ban = []
        links = []
        with open(path, "r") as data_file:
            data = json.load(data_file)
            self.node_name_list = [data['networkTopology']['nodes']
                [node_num][self.input_cons.network_topology_node_name] 
                    for node_num in range(len(data['networkTopology']['nodes']))]

            self.link_full_list = data['networkTopology']['links']
            link_list = [data['networkTopology']['links'][node_name]
                        for node_name in self.node_name_list]
            for node in self.node_name_list:
                for _list in self.link_full_list[node]:
                    links.append((node, _list[self.input_cons.network_topology_link_name]))
            # print(links)
            # for cnt_node in range(len(self.node_name_list)):
            #     ban_sum = 0
            #     for cnt_link in range(len(link_list[cnt_node])):
            #         ban_sum += link_list[cnt_node][cnt_link][self.input_cons.network_topology_link_cap]
            #     node_ban.append(ban_sum)
            self.link_list = [_Link((node,  _list[self.input_cons.network_topology_link_name]),
                              0,
                              _list[self.input_cons.network_topology_link_cap],
                              _list[self.input_cons.network_topology_link_dis]
                                    )
                              for node in self.node_name_list
                              for _list in self.link_full_list[node]
                             ]
            self.node_list = [_Node(self.node_name_list[cnt],
                              data['networkTopology']['nodes'][cnt][self.input_cons.network_topology_node_cpu_cap],
                              data['networkTopology']['nodes'][cnt][self.input_cons.network_topology_node_memory_cap],
                              )
                              for cnt in range(len(self.node_name_list))]

            # self.dist, self.hop =  self.__floydWarshall()

    ###############################################################
    # "__function_cpu_usage": returns cpu usage of each nodes
    #               --->input: fun >>> functions name
    #               --->output: CPU usage
    ###############################################################    
    def function_cpu_usage(self, fun):
        return(self.funs[fun][self.input_cons.cpu_usage])

    def function_memory_usage(self, fun):
        return (self.funs[fun][self.input_cons.memory_usage])
    ###############################################################
    # "__function_placement": placement of function "fun" of chain
    #                                               "ser" in "node"  
    #               --->input:  fun >>> functions name
    #                           ser >>> name of chain
    #                           node >> node's number
    #               --->output: none
    ###############################################################        
    def function_placement(self, node, ser, fun):
        self.node_list[node].fun[ser].append(fun)

    ###############################################################
    # "batch_function_placement": placement batch of function "fun" 
    #                                      of chain "ser" in "node"  
    #               --->input:  ser_list >>> list of service
    #                           node_fun_list >>> list of pair of
    #                                              nodes and funs    
    #               --->output: none
    ###############################################################        
    def batch_function_placement(self, ser_list, node_fun_list):
        for node_fun, ser in zip(node_fun_list, ser_list): 
            for node, fun in node_fun:
                self.__function_placement(node, ser, fun)

    ###############################################################
    # "make_empty_nodes": this functins remove all functions that were
    #                                      place in the nodes 
    #               --->input:  none   
    #               --->output: none
    ###############################################################        
    def make_empty_nodes(self):
        for v in range(len(self.node_list)):
            self.node_list[v].fun = {}
                # for j in range(len(self.data['chains'])):
                #     self.node_list[i].fun[self.data['chains'][j]['name']] = []
    
    ###############################################################
    # "k_path": reading functions 
    #               --->input:  path >>> path of json chain file
    #                           chain_num >>> number of chains you 
    #                                           want to be generated
    #                           fun_num >>> maximum number of functions
    #                                           of each chain
    #                           ban >>> maximum bandwidth of each chain
    #                           cpu >>> maximum requered cpu core of each
    #                                       chain.
    #               --->output: none
    ############################################################### 
    def k_path(self, num):
        k_path = {}
        links = []
        G = nx.DiGraph()
        # Generating all links with length
        for node in self.node_name_list:
            for _list in self.link_full_list[node]:
                links.append((node, _list[self.input_cons.network_topology_link_name], 
                _list[self.input_cons.network_topology_link_dis]))
        G.add_nodes_from(self.node_name_list)
        G.add_weighted_edges_from(links)
        # k_path = nx.floyd_warshall_predecessor_and_distance(G)
        # paths = list(nx.shortest_simple_paths(G, '1', '3'))
        for node_1 in self.node_name_list:
            for node_2 in self.node_name_list:
                k_path[(node_1, node_2)] =  list(nx.shortest_simple_paths(G, node_1, node_2))[0: num]
        return k_path
        
###############################################################
# Ghains class:|
#             |__>functions:-->
#                           -->  
###############################################################        
class Chains:
    def __init__(self):
        self.input_cons = InputConstants.Inputs()
    
    ###############################################################
    # "read_chains": reading chains 
    #               --->input:  path >>> path of json chain file
    #                           graph >> object of Graph class
    #               --->output: none
    ###############################################################            
    def read_chains(self, path, graph):
        user = []
        users = []

        with open(path, "r") as data_file:
            data = json.load(data_file)
            for i in range(len(graph.node_list)):
                for j in range(len(data["chains"])):
                    graph.node_list[i].fun[data["chains"][j]['name']] = []
            for c in range(len(data["chains"])):
                for u in range(len(data["chains"][c]["users"])):
                    for node_name in graph.node_name_list:
                        if node_name in data["chains"][c]["users"][u].keys():
                            for k in data["chains"][c]["users"][u][node_name]:
                                user.append((node_name, k))
                users.append(user)
                user = []
        return([_Chain(data["chains"][i]['name'],
                        data["chains"][i]['functions'], 
                        data["chains"][i]['traffic%'],
                        users[i]) 
                        for i in range(len(data["chains"]))])
    ###############################################################
    # "read_funcions": reading functions 
    #               --->input:  path >>> path of json chain file
    #               --->output: functions list
    ###############################################################            
    def read_funcions(self, path):
         with open(path, "r") as data_file:
            data = json.load(data_file)
         return(data["functions"])

    ###############################################################
    # "creat_chains_functions": reading functions 
    #               --->input:  path >>> path of json chain file
    #                           chain_num >>> number of chains you 
    #                                           want to be generated
    #                           fun_num >>> maximum number of functions
    #                                           of each chain
    #                           ban >>> maximum bandwidth of each chain
    #                           cpu >>> maximum requered cpu core of each
    #                                       chain.
    #               --->output: none
    ###############################################################            
    def creat_chains_functions(self, path, chain_num, fun_num, ban, cpu):
         chains = {}
         chains["chains"] = []
         chains["functions"] = {}
         for f in range(fun_num):
             chains["functions"][str(f)] = rd.randint(1, cpu)
         for c in range(chain_num):
             chain = {}
             rand_fun_num = rd.randint(1, fun_num)         
             chain['name'] = str(c)
             chain['functions'] = [str(f) 
                                for f in range(rand_fun_num)]
             chain['bandwidth'] = rd.randint(1, ban)
             chains["chains"].append(chain)
         with open(path, 'w') as outfile:  
             json.dump(chains, outfile)
