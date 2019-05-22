#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 27 17:58:40 2019

@author: ali
"""
class Inputs:
########################################
#  Path and name of input files   
########################################
    network_path = "./Data/"
    network_name = "nsf_14_network.json"
    chains_path = "./Data/"
    chains_name = "chains.json"
    chains_random_name = "chains_random.json"
    chains_random_path = "./Data/"
    functions_random_name = 'functions_random.json'
    functions_random_path = './Data/'
########################################
# Network topology parameters
########################################
    network_topology_node_name = 0
    network_topology_node_cpu_cap = 1
    network_topology_node_memory_cap = 2
    network_topology_link_name = 0
    network_topology_link_dis = 1
    network_topology_link_cap = 2
    function_name = 0
    function_usage = 1
    cpu_usage = 0
    mem_usage = 1

########################################
# Creat chains parameters
########################################

    ban_range = [1, 2]
    cpu_range = [1, 2]
    mem_range = [1, 2]
    run_num = 40
    user_num = 15

    functions = ["NAT", "FW", "TM", "WOC", "IDPS", "VOC"]

    chains = {'WebService': ["NAT","FW","TM","WOC","IDPS"],
                'VoIP': ["NAT", "FW", "TM", "FW", "NAT"],
                'VideoStreaming' : ["NAT","FW","TM","VOC","IDPS"],
                'OnlineGaming': ["NAT","FW","VOC","WOC","IDPS"]
             }

    k_path_num = 3
    alpha = 0.9
