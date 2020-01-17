#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Siun Jan 27 16:44:41 2019
@author: ali(zamaniali1995@gmail.com)
"""
from coopr.pyomo import *
import time
import InputConstants
import matplotlib.pyplot as plt


class MILP_online_model:
    def __init__(self):
        self.input_cons = InputConstants.Inputs()

    def run(self, graph, chains, functions, k, alpha):
        start_time =time.time()
        chains_sorted = []
        for c in chains.chains_list:
            for u in c.users:
                chains_sorted.append([c, u, c.cpu_usage * c.tra, c.tra])
        chains_sorted.sort(key=lambda x: x[3], reverse=True)
        chains_sorted.sort(key=lambda x: x[2], reverse=True)
        
        for chain, u,_ , _ in chains_sorted:
            M = 100000
        
            ##########################################
            # Define concrete model
            ###########################################
            model = ConcreteModel()
        
            ###########################################
            # Sets
            ###########################################
            # k paths
            model.k_path = graph.k_path(u[0], u[1], k)
            # Set of nodes: v
            for path in model.k_path:
                try:
                    model.V.extend(path)
                except:
                    model.V = []
                    model.V.extend(path)
            model.V = list(dict.fromkeys(model.V))
            model.P = range(len(model.k_path))
            model.nc = range(len(chain.fun))
            # CPU usage of each function
            for i in model.nc:
                try:
                    model.nf[i] = functions.cpu_usage(chain.fun[i])
                except:
                    model.nf = {}
                    model.nf[i] = functions.cpu_usage(chain.fun[i])
            # mem usage of each function
            for i in model.nc:
                try:
                    model.mf[i] = functions.mem_usage(chain.fun[i])
                except:
                    model.mf = {}
                    model.mf[i] = functions.mem_usage(chain.fun[i])
            # Set of links
            model.L = range(graph.links_num())
            # Set of IDs
            flag = 0
            model.phi = {}
            for p in model.P:
                for l in model.L:
                    flag = 0
                    for n in range(len(model.k_path[p]) - 1):
                        if (model.k_path[p][n], model.k_path[p][n + 1])\
                                == graph.link_list[l].name:
                            model.phi[(l, p)] = 1
                            flag = 1
                        elif flag == 0:
                            model.phi[(l, p)] = 0
        
            ###########################################
            # Variables
            ###########################################
            model.t = Var(within=NonNegativeReals)
            model.t_prime = Var(within=NonNegativeReals)
            model.a = Var(model.V, model.nc, model.P,within=Binary)
            model.b = Var(model.P, within=Binary)
            
            ###########################################
            # Objective function: min. t and t'
            ###########################################
            model.obj = Objective(expr=alpha * model.t + (1 - alpha) * model.t_prime
                                , sense=minimize)

            ###########################################
            # Constraints
            ##########################################
            # 1st constraint
            model.balance_CPU_cons = ConstraintList()
            for v in model.V:
                v_num = graph.name_to_num_node(v)
                model.balance_CPU_cons.add(sum([model.a[v, i, p] *
                                                model.nf[i] *
                                                chain.tra /
                                                graph.node_list[v_num].cap_cpu
                                            for i in model.nc
                                            for p in model.P
                                            ]) +
                                    graph.node_list[v_num].cons_cpu
                                    <=
                                    model.t)

            # 2nd constraint:
            model.cap_cpu_cons = ConstraintList()
            model.cap_cpu_cons.add(model.t <= 1)
            
            # 3rd constraint:
            model.cap_mem_cons = ConstraintList()
            for v in model.V:
                graph.name_to_num_node(v)
                model.cap_mem_cons.add(sum([model.a[v, i, p] *
                                                model.mf[i] *
                                                chain.tra /
                                                graph.node_list[v_num].cap_mem
                                                for i in model.nc
                                                for p in model.P
                                                ]) +
                                        graph.node_list[v_num].cons_mem
                                        <=
                                        1)
    
    
            # 4th constraint
            model.link_balance_cons = ConstraintList()
            for l in model.L:
                model.link_balance_cons.add(sum([model.b[p] *
                                                model.phi[(l, p)] *
                                                chain.tra /
                                                graph.link_list[l].ban
                                                for p in model.P
                                                ]) + 
                                                graph.link_list[l].cons

                                            <=
                                            model.t_prime
                )
            # 5th constraint:
            model.link_cap_cons = ConstraintList()
            model.link_cap_cons.add(model.t_prime <= 1)                                
            # 6ht constraint:
            model.path_selection_cons = ConstraintList()
            model.path_selection_cons.add(sum([model.b[p]
                                            for p in model.P
                                            ]) == 1
                                        )
                
            # 7th constraint
            model.satisfy_req_2_cons = ConstraintList()
            for p in model.P:
                for i in model.nc:
                    model.satisfy_req_2_cons.add(sum([
                        model.a[v, i, p]
                        for v in model.V
                    ])
                                                        <=
                                                        model.b[p]
                                                        )
            # 8th constraint:
            model.satisfy_req_3_cons = ConstraintList()
            for p in model.P:
                for i in model.nc:
                    model.satisfy_req_3_cons.add(sum([
                        model.a[v, i, p]
                        for v in model.k_path[p]

                    ])
                                                >=
                                                model.b[p]
                                                )
            # 9th constraint:
            model.seq_cons = ConstraintList()
            for p in model.P:
                for v_num, v in enumerate(model.k_path[p]):
                    for i in model.nc:
                        if v_num != 0:
                            model.seq_cons.add(sum([
                            model.a[v_1, i_1, p] 
                            for v_1 in model.k_path[p][: v_num]
                            for i_1 in range(i + 1, len(chain.fun))
                                        ])
                                        <=
                                        M * (1 - model.a[v, i, p])
                                        )

            opt = SolverFactory("cplex", executable=self.input_cons.path_cplex)
            opt.options["threads"] = self.input_cons.threads_num
            results = opt.solve(model)
            for v in model.V:
                v_num = graph.name_to_num_node(v)
                for i in model.nc:
                    for p in model.P:
                        graph.node_list[v_num].cons_mem += value(model.a[v, i, p]) * model.mf[i] * chain.tra / graph.node_list[v_num].cap_mem
                        graph.node_list[v_num].cons_cpu += value(model.a[v, i, p]) * model.nf[i] * chain.tra / graph.node_list[v_num].cap_cpu     
            for p in model.P:
                if value(model.b[p]):
                    for n in range(len(model.k_path[p])-1):
                        l = graph.name_to_num_link((model.k_path[p][n], model.k_path[p][n+1]))
                        graph.link_list[l].cons += chain.tra / graph.link_list[l].ban
    
        end_time = time.time()
        node_cpu_cap = []
        node_mem_cap = []
        for v in range(graph.nodes_num()):
            node_cpu_cap.append(graph.node_list[v].cons_cpu * 100)
            node_mem_cap.append(graph.node_list[v].cons_mem * 100)
        
        link_cap = []
        for l in range(len(graph.link_list)):
            link_cap.append(graph.link_list[l].cons * 100)
        print('MILP online:', sum(node_cpu_cap))
        return [max(node_cpu_cap), max(link_cap), end_time - start_time, max(node_mem_cap)]
