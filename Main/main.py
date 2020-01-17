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
sys.path.insert(1, './Plot')
import InputConstants
from PaperFunctions import Graph, Chains, Functions
from Plot import Plot
import time

user_list = []
chain_list = []
#import matplotlib.pyplot as plt
###############################################################
# Reading input files
###############################################################
input_cons = InputConstants.Inputs()
funs = Functions()
funs.generate(randomFunc=True)
funs.read(input_cons.functions_random_path + input_cons.functions_random_name) 
graph = Graph(input_cons.network_path + input_cons.network_name, funs)
plot = Plot()                      
for k in input_cons.k_path_num:
    for alpha in input_cons.alpha:
        for batch_size in input_cons.batch_size:
            for chain_num in input_cons.chains_num:

                chain = Chains(graph, funs)
                print('##############')
                print('number of chains: {}/ number of users: {} / KSP: {} / alpha: {} / bathc size: {}'.format(chain_num, chain_num, k, alpha, batch_size))
                for i in range(input_cons.run_num):
                    print('*********')
                    print('epoch: {} / {}'.format(i+1, input_cons.run_num))
                    chain.generate(chain_num, funs, randomChain=True)
                    chain.user_generatore(0, forEachChain=True)
                    chain.read(input_cons.chains_random_path + input_cons.chains_random_name)
                    user_num = chain.num()
                
                    plot.run(input_cons.approaches, graph, chain, funs, k, alpha,
                     batch_size, user_num)
                user_list.append(user_num)
                chain_list.append(chain_num)

                plot.box_plot_save(input_cons.approaches, user_num, k, alpha, batch_size, versus_chain=True, versus_user=False, show=False, fomat_list=input_cons.format)
            plot.curve(input_cons.approaches, alpha, batch_size, k, user_list, chain_list, 0, 0, format_list=input_cons.format, show=False, versus_chain=True, versus_user=False)
            user_list = []
            chain_list = []
        