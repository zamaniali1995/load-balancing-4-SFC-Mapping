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
from decimal import Decimal, ROUND_DOWN
sys.path.insert(0, './PaperFunctions')
sys.path.insert(1, './Given')
sys.path.insert(1, './Models')
from MILP_offline import MILP_offline_model
from MILP_online import MILP_online_model
import InputConstants
from PaperFunctions import Graph, Chains, Functions
from Heuristic import heuristic_model
import time

#import matplotlib.pyplot as plt
###############################################################
# Reading input files
###############################################################
input_cons = InputConstants.Inputs()
heu_info = []
MILP_offline_info = []
MILP_online_info = []
funs = Functions()
funs.generate()
funs.read(input_cons.functions_random_path + input_cons.functions_random_name) 
labels = []
load_links = []
load_nodes = []
for u, user_num in enumerate(input_cons.user_num):
    for k in input_cons.k_path_num:
        for alpha in input_cons.alpha:
            print('##############')
            print('number of users: {} / KSP: {} / alpha: {}'.format(user_num, k, alpha))
            for i in range(input_cons.run_num):
                graph = Graph(input_cons.network_path + input_cons.network_name, 
                            funs, u)
                chain = Chains(graph, funs)
                chain.generate(user_num)
                chain.read(input_cons.chains_random_path + input_cons.chains_random_name)
                graph.make_empty_network()
                heu = heuristic_model(k, alpha)
                heu_info.append(heu.run(graph, chain, funs))
                graph.make_empty_network()
                MILP_online = MILP_online_model(k, alpha)
                MILP_online_info.append(MILP_online.run(graph, chain, funs))
                graph.make_empty_network()
                MILP_offline = MILP_offline_model(k, alpha)
                MILP_offline_info.append(MILP_offline.run(graph, chain, funs))
                print('epoch: {} / {}'.format(i+1, input_cons.run_num))
            # print(ILP_loads)
            # print(heuristic_loads)
            # spread = range(0, 100)
            # center = sum(map(lambda x: x[1], ILP_loads)) / len(ILP_loads)
            # flier_high = max(map(lambda x: x[0], ILP_loads))
            # flier_low = min(map(lambda x: x[0], ILP_loads))
            # print(np.percentile(ILP_loads, 50))
            cpu_heu = list(map(lambda x: x[0], heu_info))
            link_heu = list(map(lambda x: x[1], heu_info))
            time_heu = list(map(lambda x: x[2], heu_info))
            
            cpu_MILP_online = list(map(lambda x: x[0], MILP_online_info))
            link_MILP_online = list(map(lambda x: x[1], MILP_online_info))
            time_MILP_online = list(map(lambda x: x[2], MILP_online_info))
            
            cpu_MILP_offline = list(map(lambda x: x[0], MILP_offline_info))
            link_MILP_offline = list(map(lambda x: x[1], MILP_offline_info))
            time_MILP_offline = list(map(lambda x: x[2], MILP_offline_info))
            
            # print(cpu_list)
            # data = np.concatenate((100, center, flier_high, flier_low))
            load_nodes.append((
                        max(cpu_MILP_offline),
                        np.percentile(cpu_MILP_offline, 75),
                        np.percentile(cpu_MILP_offline, 50), 
                        np.percentile(cpu_MILP_offline, 25), 
                        min(cpu_MILP_offline)
                        )
            )
            load_nodes.append((
                        max(cpu_MILP_online),
                        np.percentile(cpu_MILP_online, 75),
                        np.percentile(cpu_MILP_online, 50), 
                        np.percentile(cpu_MILP_online, 25), 
                        min(cpu_MILP_online)
                        )
            )
            load_nodes.append((
                        max(cpu_heu),
                        np.percentile(cpu_heu, 75),
                        np.percentile(cpu_heu, 50), 
                        np.percentile(cpu_heu, 25), 
                        min(cpu_heu))
                        )
            load_links.append((
                        max(link_MILP_offline),
                        np.percentile(link_MILP_offline, 75),
                        np.percentile(link_MILP_offline, 50), 
                        np.percentile(link_MILP_offline, 25), 
                        min(link_MILP_offline)
                        )
            )
            load_links.append((
                        max(link_MILP_online),
                        np.percentile(link_MILP_online, 75),
                        np.percentile(link_MILP_online, 50), 
                        np.percentile(link_MILP_online, 25), 
                        min(link_MILP_online)
                        )
            )
            
            load_links.append((
                        max(link_heu),
                        np.percentile(link_heu, 75),
                        np.percentile(link_heu, 50), 
                        np.percentile(link_heu, 25), 
                        min(link_heu))
                        )
            labels.append((str(user_num)+ '/MOF/'+'t:'+str(round(sum(time_MILP_offline)/len(time_MILP_offline), 2)) ))
            labels.append((str(user_num)+ '/MON/'+'t:'+str(round(sum(time_MILP_online)/len(time_MILP_online), 2)) ))
            labels.append((str(user_num)+'/H/'+'t:'+str(round(sum(time_heu)/len(time_heu), 2))))
            
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
            ax1.set_title('nodes load'+'/'+'user num:'+str(user_num)+'/'+'K shortest path:'+str(k)+'/'+'alpha:'+str(alpha))
            plt.xlabel('number of users/ MOF(offline MILP) or MON(online MILP) or H(Heuristic)/ tiem')
            plt.ylabel('cpu usage(%)')
            ax1.boxplot(load_nodes, labels=labels)
            plt.savefig('Results/'+'nodescap_'+'usernum:'+str(user_num)+'_KSP:'+str(k)+'_alpah:'+str(alpha)+'.jpg')
            # plt.show()
            plt.close()
            fig2, ax2 = plt.subplots()
            ax2.set_title('links load'+'/'+'user num:'+'user num:'+str(user_num)+'/'+'K shortest path:'+str(k)+'/'+'alpha:'+str(alpha))
            plt.xlabel('number of users/ MOF(offline MILP) or MON(online MILP) or H(Heuristic)/time')
            plt.ylabel('bandwidth usage(%)')
            ax2.boxplot(load_links, labels=labels)
            plt.savefig('Results/'+'linkscap_'+'usernum:'+str(user_num)+'_KSP:'+str(k)+'_alpah:'+str(alpha)+'.jpg')
            # plt.show()
            plt.close()
            load_links = []
            load_nodes = []
            labels = []