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

            # print(self.node_name_list)
            self.link_full_list = data['networkTopology']['links']
            # print(self.link_full_list)
            link_list = [data['networkTopology']['links'][node_name]
                        for node_name in self.node_name_list 
                        if data['networkTopology']['links'][node_name] != []
                                                                        ]
            # print(link_list)
            for node in self.node_name_list:
                if self.link_full_list[node] != []:
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
                              self.input_cons.link_cap,
                            #   _list[self.input_cons.network_topology_link_cap],
                              _list[self.input_cons.network_topology_link_dis]
                                    )
                              for node in self.node_name_list
                              for _list in self.link_full_list[node]
                             ]
            self.node_list = [_Node(self.node_name_list[cnt],
                                self.input_cons.node_cpu, 
                                self.input_cons.node_mem
                                
                            #   data['networkTopology']['nodes'][cnt][self.input_cons.network_topology_node_cpu_cap],
                            #   data['networkTopology']['nodes'][cnt][self.input_cons.network_topology_node_memory_cap],
                              )
                              for cnt in range(len(self.node_name_list))]
            self.nodes_name = []
            for n in range(len(self.node_list)):
                self.nodes_name.append(self.node_list[n].name)
            # self.dist, self.hop =  self.__floydWarshall()
            self.name_num_node = {}
            for v in range(len(self.node_list)):
                self.name_num_node[self.node_list[v].name] = v
            self.name_num_link = {}
            for l in range(len(self.link_list)):
                self.name_num_link[self.link_list[l].name] = l
    ###############################################################
    # "__function_cpu_usage": returns cpu usage of each nodes
    #               --->input: fun >>> functions name
    #               --->output: CPU usage
    ###############################################################    
    # def function_cpu_usage(self, fun):
    #     return(self.funs[fun][self.input_cons.cpu_usage])

    # def function_memory_usage(self, fun):
    #     return (self.funs[fun][self.input_cons.memory_usage])
    def name_to_num_link(self, link):
        return self.name_num_link[link]
    def name_to_num_node(self, node):
        return self.name_num_node[node]
    # number of nodes in the network    
    def nodes_num(self):
        return len(self.node_list)
    # Number of links in the network
    def links_num(self):
        return len(self.link_list)
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
        pass

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
       # print(self.node_list[node].cons_cpu, self.node_list[node].cons_mem)
        if  self.node_list[node].cons_cpu <= 1.0 and \
                 self.node_list[node].cons_mem <= 1.0:
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
        #print( self.link_list[l].cons)
        if  self.link_list[l].cons <= 1.0:
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
    
    def k_path(self, source, destination, k):
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
        #if (source, destination) in self.k_paths:
        #    return self.k_paths[(source, destination)]
        #else:
        #   self.k_paths[(source, destination)] = []
        #    for path in list(nx.shortest_simple_paths(G, source, destination))[0: k]:
        #        if self._path_cap_checker(path):
        #            self.k_paths[(source, destination)].append(path)
        k_paths = []
        for path in list(nx.shortest_simple_paths(G, source, destination)):
            if (len(path)-1)<=k:
                if 1==1:
                # if self._path_cap_checker(path):
                    k_paths.append(path)
            else:
                break
            # self.k_paths[(source, destination)] = list(nx.shortest_simple_paths(G, source, destination))[0: num]
        #return self.k_paths[(source, destination)]
       # print(k_paths)
        return k_paths
        
###############################################################
# Ghains class:|
#             |__>functions:-->
#                           -->  
###############################################################        
class Chains:
    def __init__(self, graph, functions):
        self.input_cons = InputConstants.Inputs()
        self. graph = graph
        self.functions = functions
    def read(self, path):
        user = []
        users = []
        with open(path, "r") as data_file:
            data = json.load(data_file)
            for i in range(len(self.graph.node_list)):
                for j in range(len(data["chains"])):
                    self.graph.node_list[i].fun[data["chains"][j]['name']] = []
            for c in range(len(data["chains"])):
                for u in range(len(data["chains"][c]["users"])):
                    for node_name in self.graph.node_name_list:
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
                cpu += self.functions.cpu_usage(f)
                mem += self.functions.mem_usage(f)
            cpu_list.append(cpu)
            mem_list.append(mem)
            cpu = 0
            mem = 0
        self.chains_list = ([_Chain(data["chains"][i]['name'],
                        data["chains"][i]['functions'], 
                        data["chains"][i]['traffic%'],
                        users[i],
                        cpu_list[i],
                        mem_list[i]
                       )
                        for i in range(len(data["chains"]))])
        self.name_num = {}
        for c in range(len(self.chains_list)):
            self.name_num[self.chains_list[c].name] = c
    # Return number of chain in chain_list
    def name_to_num(self, chain):
        return self.name_num[chain]
    # Number of functoins of each chain
    def funs_num(self, chain):
        return len(self.chains_list[self.name_to_num(chain)].fun)
    # Number of users
    def users_num(self, chain):
        self.user_num = {}
        if chain in self.user_num.keys():
            return self.user_num[chain]
        else:
            self.user_num[chain] = 0
            for _ in self.chains_list[self.name_to_number(chain)].users:
               self.user_num[chain] += 1
            return self.user_num[chain]
    # def funcs_number(self)
    ###############################################################
    # "read_chains": reading chains 
    #               --->input:  path >>> path of json chain file
    #                           graph >> object of Graph class
    #               --->output: none
    ###############################################################            
    # def read_chains(self, path, graph):
        
        # return self.chains_list
    # Number of chains
    def num(self):
        return len(self.chains_list)

    def generate(self, chain, funs, randomChain):
        chains = {}
        chains["chains"] = []
        if randomChain:
            chains_num = chain
        else:
            chains_num = len(self.input_cons.chains)
        for c in range(chains_num):
            chain = {}
            if randomChain:
                chain['name'] = str(c)
            else:
                chain['name'] = c

            funs_num = rd.randint(self.input_cons.chains_func_num[0], self.input_cons.chains_func_num[1])
            chain['functions'] = [funs.functions_name[rd.randint(0, funs.num()-1)] for _ in range(funs_num)]
            chain['users'] = []
            chain['traffic%'] = rd.randint(self.input_cons.ban_range[0], self.input_cons.ban_range[1])
            chains["chains"].append(chain)
        self.chains_tmp = chains
        # print(chains)
        
    def user_generatore(self, user, path, forEachChain):
        if forEachChain:
            user_num = [1] * len(self.chains_tmp['chains'])
        else:
            user_num = [0] * len(self.chains_tmp['chains'])
            for i in range(len(self.chains_tmp['chains'])):
                r = rd.randint(0, user)
                if user - r >= 0 and i < len(self.chains_tmp['chains']) - 1:
                    user -= r
                    user_num[i] = r
                elif i == len(self.chains_tmp['chains']) - 1:
                    tmp = user - sum(user_num)
                    if tmp > 0:
                        user_num[i] = tmp
        # print(user_num)
        for c, chain in enumerate(self.chains_tmp['chains']):
            tmp = {}
            for i in range(user_num[c]):
                s = 0
                d = 0
                while(s == d):
                    s = rd.randint(0, self.graph.nodes_num()-1)
                    d = rd.randint(0, self.graph.nodes_num()-1)
                if self.graph.node_name_list[s] in tmp.keys():
                    tmp[self.graph.node_name_list[s]].append(self.graph.node_name_list[d])
                else:
                    tmp[self.graph.node_name_list[s]] = [self.graph.node_name_list[d]]
            chain['users'].append(tmp)
            # print(chain)
                
        with open(path, 'w') as outfile:
            # self.input_cons.chains_random_path + self.input_cons.chains_random_name, 'w'
            json.dump(self.chains_tmp, outfile)

    ###############################################################
    # "read_funcions": reading functions 
    #               --->input:  path >>> path of json chain file
    #               --->output: functions list
    ###############################################################  
class Functions:
    def __init__(self):
        self.input_cons = InputConstants.Inputs()
    def read(self, path):
        with open(path, "r") as data_file:
            data = json.load(data_file) 
        self.functions_list = data["functions"]
        self.functions_name = []
        for f in self.functions_list.keys():
            self.functions_name.append(f)
        self.name_num = {}
        for f_num, f_name in enumerate(self.functions_name):
            self.name_num[f_name] = f_num
    def generate(self, randomFunc):
        funs = {}
        funs["functions"] = {}
        if randomFunc:
            funcs_num = rd.randint(self.input_cons.fun_num_range[0], self.input_cons.fun_num_range[1])
            for f in range(funcs_num):
                funs["functions"][str(f)] = [rd.randint(self.input_cons.cpu_range[0], self.input_cons.cpu_range[1]),
                                        rd.randint(self.input_cons.mem_range[0], self.input_cons.mem_range[1])]
        else:
            for f in self.input_cons.functions:
                funs["functions"][f] = [rd.randint(self.input_cons.cpu_range[0], self.input_cons.cpu_range[1]),
                                        rd.randint(self.input_cons.mem_range[0], self.input_cons.mem_range[1])]
        with open(self.input_cons.functions_random_path + self.input_cons.functions_random_name, 'w') as outfile:
            json.dump(funs, outfile)

    def name_to_num(self, fun):
        return self.name_num[fun]
    # Number of functions
    def num(self):
        return len(self.functions_list)
    # cpu usage of each function
    def cpu_usage(self, f):
        return self.functions_list[f][self.input_cons.cpu_usage]
    # mem usage of each function
    def mem_usage(self, f):
        return self.functions_list[f][self.input_cons.mem_usage]
    def names(self):
        return self.functions_name
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
    # def creat_chains_functions(self, path, chain_num, fun_num, ban, cpu):
    #      chains = {}
    #      chains["chains"] = []
    #      chains["functions"] = {}
    #      for f in range(fun_num):
    #          chains["functions"][str(f)] = rd.randint(1, cpu)
    #      for c in range(chain_num):
    #          chain = {}
    #          rand_fun_num = rd.randint(1, fun_num)         
    #          chain['name'] = str(c)
    #          chain['functions'] = [str(f) 
    #                             for f in range(rand_fun_num)]
    #          chain['bandwidth'] = rd.randint(1, ban)
    #          chains["chains"].append(chain)
    #      with open(path, 'w') as outfile:  
    #          json.dump(chains, outfile)
