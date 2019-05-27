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
from heuristic_offline import heuristic_offline_model
from heuristic_online import heuristic_online_model
from MILP_online_batch import MILP_online_batch_model
from heuristic_online_batch import heuristic_online_batch_model
from heuristic_fully_online_batch import heuristic_fully_batch_model
import time

#import matplotlib.pyplot as plt
###############################################################
# Reading input files
###############################################################
input_cons = InputConstants.Inputs()
heu_online_info = []
heu_online_batch_info = []
heu_offline_info = []
heu_fully_info = []
MILP_offline_info = []
MILP_online_info = []
MILP_online_batch_info = []
# funs = Functions()
# funs.generate()
# funs.read(input_cons.functions_random_path + input_cons.functions_random_name) 
labels = []
load_links = []
load_nodes = []
for u, user_num in enumerate(input_cons.user_num):
    for k in input_cons.k_path_num:
        for alpha in input_cons.alpha:
            for batch_size in input_cons.batch_size:
                print('##############')
                print('number of users: {} / KSP: {} / alpha: {}'.format(user_num, k, alpha))
                for i in range(input_cons.run_num):
                    funs = Functions()
                    funs.generate()
                    funs.read(input_cons.functions_random_path + input_cons.functions_random_name) 
                    graph = Graph(input_cons.network_path + input_cons.network_name, 
                                funs, u)
                    chain = Chains(graph, funs)
                    chain.generate(user_num)
                    chain.read(input_cons.chains_random_path + input_cons.chains_random_name)
                    graph.make_empty_network()
                    
                    heu_online = heuristic_online_model(k, alpha)
                    heu_online_info.append(heu_online.run(graph, chain, funs))
                    graph.make_empty_network()
                    
                    heu_online_batch = heuristic_online_batch_model(k, alpha, user_num, batch_size)
                    heu_online_batch_info.append(heu_online_batch.run(graph, chain, funs))
                    graph.make_empty_network()
                    
                    heu_offline = heuristic_offline_model(k, alpha)
                    heu_offline_info.append(heu_offline.run(graph, chain, funs))
                    graph.make_empty_network()
                    
                    heu_fully = heuristic_fully_batch_model(k, alpha, user_num, batch_size)
                    heu_fully_info.append(heu_fully.run(graph, chain, funs))
                    graph.make_empty_network()
                    
                    MILP_online = MILP_online_model(k, alpha)
                    MILP_online_info.append(MILP_online.run(graph, chain, funs))
                    graph.make_empty_network()
                    
                    MILP_online_batch = MILP_online_batch_model(k, alpha, user_num, batch_size)
                    MILP_online_batch_info.append(MILP_online_batch.run(graph, chain, funs))
                    graph.make_empty_network()
                    ##############
                    # MILP_offline = MILP_offline_model(k, alpha)
                    # MILP_offline_info.append(MILP_offline.run(graph, chain, funs))
                    # graph.make_empty_network()
                    ######################
                    print('epoch: {} / {}'.format(i+1, input_cons.run_num))
                # print(ILP_loads)
                # print(heuristic_loads)
                # spread = range(0, 100)
                # center = sum(map(lambda x: x[1], ILP_loads)) / len(ILP_loads)
                # flier_high = max(map(lambda x: x[0], ILP_loads))
                # flier_low = min(map(lambda x: x[0], ILP_loads))
                # print(np.percentile(ILP_loads, 50))
                cpu_heu_offline = list(map(lambda x: x[0], heu_offline_info))
                link_heu_offline = list(map(lambda x: x[1], heu_offline_info))
                time_heu_offline = list(map(lambda x: x[2], heu_offline_info))
                
                cpu_heu_online = list(map(lambda x: x[0], heu_online_info))
                link_heu_online = list(map(lambda x: x[1], heu_online_info))
                time_heu_online = list(map(lambda x: x[2], heu_online_info))
                
                cpu_heu_online_batch = list(map(lambda x: x[0], heu_online_batch_info))
                link_heu_online_batch = list(map(lambda x: x[1], heu_online_batch_info))
                time_heu_online_batch = list(map(lambda x: x[2], heu_online_batch_info))
                
                cpu_heu_fully_batch = list(map(lambda x: x[0], heu_fully_info))
                link_heu_fully_batch = list(map(lambda x: x[1], heu_fully_info))
                time_heu_fully_batch = list(map(lambda x: x[2], heu_fully_info))
                
                cpu_MILP_online = list(map(lambda x: x[0], MILP_online_info))
                link_MILP_online = list(map(lambda x: x[1], MILP_online_info))
                time_MILP_online = list(map(lambda x: x[2], MILP_online_info))
                
                cpu_MILP_batch_online = list(map(lambda x: x[0], MILP_online_batch_info))
                link_MILP_batch_online = list(map(lambda x: x[1], MILP_online_batch_info))
                time_MILP_batch_online = list(map(lambda x: x[2], MILP_online_batch_info))
                ###############
                # cpu_MILP_offline = list(map(lambda x: x[0], MILP_offline_info))
                # link_MILP_offline = list(map(lambda x: x[1], MILP_offline_info))
                # time_MILP_offline = list(map(lambda x: x[2], MILP_offline_info))
                ##############

                # print(cpu_list)
                # data = np.concatenate((100, center, flier_high, flier_low))
                ################
                # load_nodes.append((
                #             max(cpu_MILP_offline),
                #             np.percentile(cpu_MILP_offline, 75),
                #             np.percentile(cpu_MILP_offline, 50), 
                #             np.percentile(cpu_MILP_offline, 25), 
                #             min(cpu_MILP_offline)
                #             )
                # )
                #################
                
                load_nodes.append((
                            max(cpu_MILP_online),
                            np.percentile(cpu_MILP_online, 75),
                            np.percentile(cpu_MILP_online, 50), 
                            np.percentile(cpu_MILP_online, 25), 
                            min(cpu_MILP_online)
                            )
                )
                
                load_nodes.append((
                            max(cpu_MILP_batch_online),
                            np.percentile(cpu_MILP_batch_online, 75),
                            np.percentile(cpu_MILP_batch_online, 50), 
                            np.percentile(cpu_MILP_batch_online, 25), 
                            min(cpu_MILP_batch_online)
                            )
                )
                
                load_nodes.append((
                            max(cpu_heu_offline),
                            np.percentile(cpu_heu_offline, 75),
                            np.percentile(cpu_heu_offline, 50), 
                            np.percentile(cpu_heu_offline, 25), 
                            min(cpu_heu_offline))
                            )
                
                load_nodes.append((
                            max(cpu_heu_online),
                            np.percentile(cpu_heu_online, 75),
                            np.percentile(cpu_heu_online, 50), 
                            np.percentile(cpu_heu_online, 25), 
                            min(cpu_heu_online))
                            )
                
                
                load_nodes.append((
                            max(cpu_heu_online_batch),
                            np.percentile(cpu_heu_online_batch, 75),
                            np.percentile(cpu_heu_online_batch, 50), 
                            np.percentile(cpu_heu_online_batch, 25), 
                            min(cpu_heu_online_batch))
                            )
                
                load_nodes.append((
                            max(cpu_heu_fully_batch),
                            np.percentile(cpu_heu_fully_batch, 75),
                            np.percentile(cpu_heu_fully_batch, 50), 
                            np.percentile(cpu_heu_fully_batch, 25), 
                            min(cpu_heu_fully_batch))
                            )
                
                #################
                # load_links.append((
                #             max(link_MILP_offline),
                #             np.percentile(link_MILP_offline, 75),
                #             np.percentile(link_MILP_offline, 50), 
                #             np.percentile(link_MILP_offline, 25), 
                #             min(link_MILP_offline)
                #             )
                # )
                ###################
                load_links.append((
                            max(link_MILP_online),
                            np.percentile(link_MILP_online, 75),
                            np.percentile(link_MILP_online, 50), 
                            np.percentile(link_MILP_online, 25), 
                            min(link_MILP_online)
                            )
                )
                
                load_links.append((
                            max(link_MILP_batch_online),
                            np.percentile(link_MILP_batch_online, 75),
                            np.percentile(link_MILP_batch_online, 50), 
                            np.percentile(link_MILP_batch_online, 25), 
                            min(link_MILP_online)
                            )
                )
                
                load_links.append((
                            max(link_heu_offline),
                            np.percentile(link_heu_offline, 75),
                            np.percentile(link_heu_offline, 50), 
                            np.percentile(link_heu_offline, 25), 
                            min(link_heu_offline))
                            )
                load_links.append((
                            max(link_heu_online),
                            np.percentile(link_heu_online, 75),
                            np.percentile(link_heu_online, 50), 
                            np.percentile(link_heu_online, 25), 
                            min(link_heu_online))
                            )
                load_links.append((
                            max(link_heu_online_batch),
                            np.percentile(link_heu_online_batch, 75),
                            np.percentile(link_heu_online_batch, 50), 
                            np.percentile(link_heu_online_batch, 25), 
                            min(link_heu_online_batch))
                            )
                load_links.append((
                            max(link_heu_fully_batch),
                            np.percentile(link_heu_fully_batch, 75),
                            np.percentile(link_heu_fully_batch, 50), 
                            np.percentile(link_heu_fully_batch, 25), 
                            min(link_heu_fully_batch))
                            )
                
                # labels.append(('MOF/'+'t:'+str(round(sum(time_MILP_offline)/len(time_MILP_offline), 2)) ))
                labels.append(('MON/'+'t:'+str(round(sum(time_MILP_online)/len(time_MILP_online), 2)) ))
                labels.append(('MONB/'+'t:'+str(round(sum(time_MILP_batch_online)/len(time_MILP_batch_online), 2)) ))
                labels.append(('HON/'+'t:'+str(round(sum(time_heu_online)/len(time_heu_online), 2))))
                labels.append(('HOF/'+'t:'+str(round(sum(time_heu_offline)/len(time_heu_offline), 2))))
                labels.append(('HONB/'+'t:'+str(round(sum(time_heu_online_batch)/len(time_heu_online_batch), 2))))
                labels.append(('HFB/'+'t:'+str(round(sum(time_heu_fully_batch)/len(time_heu_fully_batch), 2))))
                
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
                ax1.set_title('nodes load'+'/'+'user num:'+str(user_num)+'/'+'K shortest path:'+str(k)+'/'+'alpha:'+str(alpha)+'/batchSize:'+str(batch_size))
                plt.xlabel('MOF|MON|MONB(offline|online|online_batch MILP) or HOF|HON|HONB(offline|online|online batch Heuristic)/ tiem')
                plt.ylabel('cpu usage(%)')
                ax1.boxplot(load_nodes, labels=labels)
                plt.savefig('Results/'+'nodescap_'+'usernum:'+str(user_num)+'_KSP:'+str(k)+'_alpah:'+str(alpha)+'_batchSize:'+str(batch_size)+'.png')
                # plt.show()
                plt.close()
                fig2, ax2 = plt.subplots()
                ax2.set_title('links load'+'/'+'user num:'+'user num:'+str(user_num)+'/'+'K shortest path:'+str(k)+'/'+'alpha:'+str(alpha)+'/batchSize:'+str(batch_size))
                plt.xlabel('MOF|MON|MONB(offline|online|online_batch MILP) or HOF|HON|HONB(offline|online|online batch Heuristic)/time')
                plt.ylabel('bandwidth usage(%)')
                ax2.boxplot(load_links, labels=labels)
                plt.savefig('Results/'+'linkscap_'+'usernum:'+str(user_num)+'_KSP:'+str(k)+'_alpah:'+str(alpha)+'_batchSize:'+str(batch_size)+'.png')
                # plt.show()
                plt.close()
                load_links = []
                load_nodes = []
                labels = []