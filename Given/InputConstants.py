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
        # "nsf_14_network.json"
        self.chains_path = "./Data/"
        self.chains_name = "chains.json"
        self.chains_random_name = "chains_random.json"
        self.chains_random_path = "./Data/"
        self.functions_random_name = 'functions_random.json'
        self.functions_random_path = './Data/'
        self.path_box_plot = 'Results/Plot/histogram/'
        self.path_curve_versus_chain = 'Results/Plot/curve/versus_chainNum/'
        self.path_curve_versus_user = 'Results/Plot/curve/versus_userNum/'
        self.path_text_box_plot = 'Results/Text/histogram/histogram.txt'
        self.path_text_curve_versus_chain = 'Results/Text/curve/versus_chainNum/curve.txt'
        self.path_curve_heu = 'Results/Text/curve/versus_chainNum/curve_heu.txt'
        self.path_curve_MILP = 'Results/Text/curve/versus_chainNum/curve_MILP.txt' 
        self.path_cplex =  "/home/zamani/CPLEX/cplex/bin/x86-64_linux/cplex"
        # "/home/zamani/Paper/cplex/cplex/bin/x86-64_linux/cplex"
        #  "/home/pervasive/Zamani/cplex/bin/x86-64_linux/cplex"
        # "/opt/ibm/ILOG/CPLEX_Studio128/cplex/bin/x86-64_linux/cplex"
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

        self.threads_num = 2
    ########################################
    # Creat chains parameters
    #######################################
        self.ban_range = [2, 5]
        #self.ban_range = [1, 2] 
        self.cpu_range = [2, 5]
        #self.cpu_range = [1, 2] 
        self.mem_range = [2, 5]
        #self.mem_range = [1, 2]
        self.run_num = 20
        #self.run_num = 20
        self.batch_size = [4]
        self.user_num = [5, 10]
        #self.chains_num = [50]
        self.chains_num = [50]
        #[i for i in range(50, 3, -4)]
        #[i for i in range(50, 4, -5)]
        self.chains_func_num = [2, 5]
        #self.chains_func_num = [1, 2]  
        # [i for i in range(100, 200, 10)]
        # [i for i in range(7, 12, 1)]
        # print(self.user_num)
        # self.node_cpu = [max(self.user_num) * 5 * self.cpu_range[1] * self.ban_range[1]]
        self.node_cpu = max(self.chains_num) * max(self.chains_func_num) * self.cpu_range[1] * self.ban_range[1] /17
        #self.node_cpu = max(self.chains_num) * max(self.chains_func_num) * self.cpu_range[1] * self.ban_range[1] /11
        self.node_mem = max(self.chains_num) * self.mem_range[1] * max(self.chains_func_num) * self.ban_range[1] /1
        self.link_cap = max(self.chains_num) * self.ban_range[1] /5.7
        #self.link_cap = max(self.chains_num) * self.ban_range[1] /4.5
        self.functions = ["NAT", "FW", "TM", "WOC", "IDPS", "VOC"]
        #self.fun_num_range = [2, 5]
        self.fun_num_range = [1, 2] 
        self.chains = {'WebService': ["NAT","FW","TM","WOC","IDPS"],
                    'VoIP': ["NAT", "FW", "TM", "FW", "NAT"],
                    'VideoStreaming' : ["NAT","FW","TM","VOC","IDPS"],
                    'OnlineGaming': ["NAT","FW","VOC","WOC","IDPS"]
                }
        
        self.k_path_num = [3, 4, 5, 6]
        self.alpha = [0.5]
        #[0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
        #self.approaches = ('MILPB', 'HF')
        self.approaches = ('MILPB', 'HF') 
        self.format = [ '.png']
        self.heu_full_tune_param = [0]
        # [round(i*0.1, 1) for i in range(1, 10)]
