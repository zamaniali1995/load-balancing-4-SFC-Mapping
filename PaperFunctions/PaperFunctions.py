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
        self.cons_cpu = 0
        self.cons_mem = 0
###############################################################
# Link features class
###############################################################
class _Link:
    def __init__(self, name, consumed, bandwidth, length):
        self.cons = consumed
        self.ban = bandwidth
        self.length = length
        self.name = name

###############################################################
# Chain features class
###############################################################
class _Chain:
    def __init__(self, name, function, traffic, users, cpu, mem):
        self.name = name
        self.fun = function
        self.tra = traffic
        self.users = users
        self.cpu_usage = cpu
        self.mem_usage = mem
###############################################################
# Graph class:|
#             |__>functions:-->
#                           -->  
###############################################################
class Graph:

    def __init__(self, path, funs):
        self.k_paths = {}
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
    def make_empty_network(self):
        for v in range(len(self.node_list)):
            self.node_list[v].fun = {}
            self.node_list[v].cons_mem = 0
            self.node_list[v].cons_cpu = 0
        for l in range(len(self.link_list)):
            self.link_list[l].cons = 0

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
    def _node_cap_checker(self, node):
        if self.node_list[node].cap_cpu >= self.node_list[node].cons_cpu and \
                self.node_list[node].cap_mem >= self.node_list[node].cons_mem:
            return True
        else:
            return False
    def _node_name_to_seq(self, name):
        for n in range(len(self.node_list)):
            if name == self.node_list[n].name:
                return n
    def _link_name_to_seq(self, link):
        for l in range(len(self.link_list)):
            if link == self.link_list[l].name:
                return l
    def _link_cap_checker(self, l):
        if self.link_list[l].ban >= self.link_list[l].cons:
            return True
        else:
            return False
    def _path_cap_checker(self, path):
        flag = 0
        for n in path:
            if not self._node_cap_checker(self._node_name_to_seq(n)):
                flag = 1
        for l in range(len(path)-1):
            if not self._link_cap_checker(self._link_name_to_seq((path[l], path[l+1]))):
                flag = 1
        if flag == 0:
            return True
        else:
            return False
    def k_path(self, num, source, destination):
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
        # for node_1 in self.node_name_list:
        #     for node_2 in self.node_name_list:
        if (source, destination) in self.k_paths:
            return self.k_paths[(source, destination)]
        else:
            self.k_paths[(source, destination)] = []
            for path in list(nx.shortest_simple_paths(G, source, destination))[0: num]:
                if self._path_cap_checker(path):
                    self.k_paths[(source, destination)].append(path)

            # self.k_paths[(source, destination)] = list(nx.shortest_simple_paths(G, source, destination))[0: num]
            return self.k_paths[(source, destination)]

        
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
        mem = 0
        cpu = 0
        cpu_list = []
        mem_list = []
        for c in range(len(data["chains"])):
            for f in data["chains"][c]["functions"]:
                cpu += graph.function_cpu_usage(f)
                mem += graph.function_memory_usage(f)
            cpu_list.append(cpu)
            mem_list.append(mem)
            cpu = 0
            mem = 0
        return([_Chain(data["chains"][i]['name'],
                        data["chains"][i]['functions'], 
                        data["chains"][i]['traffic%'],
                        users[i],
                        cpu_list[i],
                        mem_list[i]
                       )
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
