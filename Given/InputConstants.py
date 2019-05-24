#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 27 17:58:40 2019

@author: ali
"""
class Inputs:
    def __init__(self):
    ########################################
    #  Path and name of input files   
    ########################################
        self.network_path = "./Data/"
        self.network_name = "nsf_14_network.json"
        self.chains_path = "./Data/"
        self.chains_name = "chains.json"
        self.chains_random_name = "chains_random.json"
        self.chains_random_path = "./Data/"
        self.functions_random_name = 'functions_random.json'
        self.functions_random_path = './Data/'
    ########################################
    # Network topology parameters
    ########################################
        self.network_topology_node_name = 0
        self.network_topology_node_cpu_cap = 1
        self.network_topology_node_memory_cap = 2
        self.network_topology_link_name = 0
        self.network_topology_link_dis = 1
        self.network_topology_link_cap = 2
        self.function_name = 0
        self.function_usage = 1
        self.cpu_usage = 0
        self.mem_usage = 1

    ########################################
    # Creat chains parameters
    ########################################
        self.ban_range = [1, 2]
        self.cpu_range = [1, 2]
        self.mem_range = [1, 2]
        self.run_num = 20
        self.user_num = [i for i in range(1, 3, 1)]
        # print(self.user_num)
        self.node_cpu = list(map(lambda x: x * 5 * self.cpu_range[1] , self.user_num))
        self.node_mem = [self.user_num[i] * self.mem_range[1] * 5  for i in range(len(self.user_num))] 
        self.link_cap = [self.user_num[i] * self.ban_range[1]  for i in range(len(self.user_num))]
        
        self.functions = ["NAT", "FW", "TM", "WOC", "IDPS", "VOC"]

        self.chains = {'WebService': ["NAT","FW","TM","WOC","IDPS"],
                    'VoIP': ["NAT", "FW", "TM", "FW", "NAT"],
                    'VideoStreaming' : ["NAT","FW","TM","VOC","IDPS"],
                    'OnlineGaming': ["NAT","FW","VOC","WOC","IDPS"]
                }

        self.k_path_num = [1, 2, 3]
        self.alpha = [round(i*0.1, 1) for i in range(1, 10)]
