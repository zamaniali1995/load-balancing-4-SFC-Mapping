#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Siun Jan 27 16:44:41 2019
@author: ali(zamaniali1995@gmail.com)
"""
from coopr.pyomo import *
import time
# import pyomo.environ as pyo
import InputConstants
import matplotlib.pyplot as plt


# Must be changed
class MILP_batch_model:
    def __init__(self):
        self.input_cons = InputConstants.Inputs()

    def run(self, graph, chains, functions, k, alpha, user_num, batch_size):
        start_time =time.time()
        chains_sorted = []
        batch_chains = []
        cnt = 0
        batch_num = 0
        nodes_set = []
        sources = []
        destinations = []
        for c in chains.chains_list:
            for u in c.users:
                chains_sorted.append([c, u, c.cpu_usage * c.tra, c.tra])
                
        chains_sorted.sort(key=lambda x: x[2], reverse=True)
        chains_sorted.sort(key=lambda x: x[3], reverse=True)
        
        for c, u, _, _ in chains_sorted:
            batch_chains.append([c.name, u])
            sources.append(u[0])
            destinations.append(u[1])
            for p in graph.k_path(u[0], u[1], k):
                nodes_set.extend(p)
            cnt += 1
            if cnt == batch_size or cnt == user_num or (batch_num == user_num // batch_size and cnt == user_num % batch_size):               
                batch_num += 1
                M = 100000
                nodes_set = list(dict.fromkeys(nodes_set))
                sources = list(dict.fromkeys(sources))
                destinations = list(dict.fromkeys(destinations))       
        
                ##########################################
                # Define concrete model
                ###########################################
                model = ConcreteModel()

                ###########################################
                # Sets
                ###########################################
                # Set of nodes: v
                model.V = nodes_set
                # Set of functions: F
                model.F = range(functions.num())
                # Set of chains: C
                model.C = [c for c, _ in batch_chains]
                model.C = list(dict.fromkeys(model.C))
                # Set of sources: S
                model.S = sources
                # Set of distinations: D
                model.D = destinations
                # Set of K shortest paths: K_sd
                model.k_path = graph.k_path
                # Set of k paths
                model.P = range(k)
                # Set of function of each chain
                model.nc = {}
                for c in model.C:
                    model.nc[c] = chains.funs_num(c)
                # cpus usage of each function
                model.nf = []
                for f in functions.functions_list.keys():
                    model.nf.append(functions.cpu_usage(f))
                # mem usage of each function
                model.mf = []
                for f in functions.functions_list.keys():
                    model.mf.append(functions.mem_usage(f))
                # Set of links
                model.L = range(graph.links_num())
                # Set of users
                model.R = {}
                for c, u in batch_chains:
                    try:
                        model.R[c].append(u) 
                    except:
                        model.R[c] = []
                        model.R[c].append(u)
                # Set of IDs
                flag = 0
                model.phi = {}
                for c in model.C:
                    for (s, d) in model.R[c]:
                        P = model.k_path(s, d, k)
                        for p in range(len(P)):
                            for l in model.L:
                                flag = 0
                                for n in range(len(P[p]) - 1):
                                    if (model.k_path(s, d, k)[p][n], model.k_path(s, d, k)[p][n + 1])\
                                            == graph.link_list[l].name:
                                        model.phi[(l, p, s, d)] = 1
                                        flag = 1
                                    elif flag == 0:
                                        model.phi[(l, p, s, d)] = 0
                model.I = {}
                for c in model.C:
                    for f_num, f_name in enumerate(functions.functions_list.keys()):
                        for i in range(model.nc[c]):
                            if chains.chains_list[chains.name_to_num(c)].fun[i] == f_name:
                                model.I[(f_num, i, c)] = 1
                            else:
                                model.I[(f_num, i, c)] = 0
                
                ###########################################
                # Variables
                ###########################################
                max_of_chain_function = max([model.nc[c] for c in model.C])
                model.t = Var(within=NonNegativeReals)
                model.t_prime = Var(within=NonNegativeReals)
                model.a = Var(model.V, model.C, model.P, range(max_of_chain_function), model.S, model.D, within=Binary)
                model.b = Var(model.P, model.C, model.S, model.D, within=Binary)
                
                ###########################################
                # Objective function: min. t
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
                    model.balance_CPU_cons.add(sum([model.a[v, c, p, i, s, d] *
                                                    model.I[(f, i, c)] *
                                                    model.nf[f] *
                                                    chains.chains_list[chains.name_to_num(c)].tra /
                                                    graph.node_list[v_num].cap_cpu
                                                    for c in model.C
                                                    for s, d in model.R[c]
                                                    for p in model.P
                                                    for i in range(model.nc[c])
                                                    for f in model.F
                                                    ]) +
                                                    graph.node_list[v_num].cons_cpu
                                                    <= model.t
                                            )
                
                # 2nd constraint
                model.node_CPU_cap_cons = ConstraintList()
                model.node_CPU_cap_cons.add(model.t <= 1)
                
                # 3rd constraint
                model.node_memory_cap_cons = ConstraintList()
                for v in model.V:
                    v_num = graph.name_to_num_node(v)
                    model.node_memory_cap_cons.add(sum([model.a[v, c, p, i, s, d] *
                                                        model.I[(f, i, c)] *
                                                        model.mf[f] *
                                                        chains.chains_list[chains.name_to_num(c)].tra /
                                                        graph.node_list[v_num].cap_mem
                                                        for c in model.C
                                                        for (s, d) in model.R[c]
                                                        for p in model.P
                                                        for i in range(model.nc[c])
                                                        for f in model.F
                                                        ]) + 
                                                        graph.node_list[v_num].cons_mem
                                                <=
                                                1)

                # 4th constraint
                model.link_balance_cons = ConstraintList()
                for l in model.L:
                    model.link_balance_cons.add(sum([model.b[p, c, s, d] *
                                                    model.phi[(l, p, s, d)] *
                                                    chains.chains_list[chains.name_to_num(c)].tra /
                                                    graph.link_list[l].ban
                                                    for c in model.C
                                                    for (s, d) in model.R[c]
                                                    for p in range(len(model.k_path(s, d, k)))
                                                    ])+
                                                    graph.link_list[l].cons
                                                <=
                                                model.t_prime
                                                )
                # 5th constraint
                model.link_cap_cons = ConstraintList()
                model.link_cap_cons.add(model.t_prime <= 1)
                
                # 6th constraint
                model.path_selection_cons = ConstraintList()
                for c in model.C:
                    for (s, d) in model.R[c]:
                        model.path_selection_cons.add(sum([model.b[p, c, s, d]
                                                        for p in range(len(model.k_path(s, d, k)))
                                                        ]) == 1
                                                    )
                
                # 7th constraint
                model.satisfy_req_2_cons = ConstraintList()
                for c in model.C:
                    for (s, d) in model.R[c]:
                        for p in model.P:
                            for i in range(model.nc[c]):

                                model.satisfy_req_2_cons.add(sum([
                                    model.a[v, c, p, i, s, d]
                                    for v in model.V
                                ])
                                                            <=
                                                            model.b[p, c, s, d]
                                                            )

                # 8th constraint
                model.satisfy_req_3_cons = ConstraintList()
                for c in model.C:
                    for (s, d) in model.R[c]:
                        P = model.k_path(s, d, k)
                        for p in range(len(P)):
                            for i in range(model.nc[c]):
                                model.satisfy_req_3_cons.add(sum([
                                    model.a[v, c, p, i, s, d]
                                    for v in P[p]

                                ])
                                                            >=
                                                            model.b[p, c, s, d]
                                                            )
                # 9th constraint:
                model.seq_cons = ConstraintList()
                for c in model.C:
                    for (s, d) in model.R[c]:
                        P = model.k_path(s, d, k)
                        for p in range(len(P)):
                            for i in range(model.nc[c] - 1):
                                for v_num, v in enumerate(P[p]):
                                    if v_num != 0:
                                        model.seq_cons.add(sum([
                                            model.a[v_1, c, p, i_1, s, d]
                                            for v_1 in model.k_path(s, d, k)[p][: v_num]
                                            for i_1 in range(i + 1, model.nc[c])
                                        ])
                                                        <=
                                                        M * (2 - model.b[p, c, s, d] - model.a[v, c, p, i, s, d])
                                                        )
                opt = SolverFactory("cplex", executable=self.input_cons.path_cplex)
                opt.options["threads"] = self.input_cons.threads_num
                results = opt.solve(model)
                node_cpu_cap = []
                node_mem_cap = []
                for v in model.V:
                    v_num = graph.name_to_num_node(v)
                    for c in model.C:
                        for (s, d) in model.R[c]:
                            for p in model.P:
                                for i in range(model.nc[c]):
                                    for f in model.F:
                                        graph.node_list[v_num].cons_cpu += value(model.a[v, c, p, i, s, d]) * model.I[(f, i, c)] * model.nf[f] * chains.chains_list[chains.name_to_num(c)].tra / graph.node_list[v_num].cap_cpu
                                        graph.node_list[v_num].cons_mem += value(model.a[v, c, p, i, s, d]) * model.I[(f, i, c)] * model.mf[f] * chains.chains_list[chains.name_to_num(c)].tra / graph.node_list[v_num].cap_mem
                link_cap = []
                for l in model.L:
                    for c in model.C:
                        for (s, d) in model.R[c]:
                            for p in range(len(model.k_path(s, d, k))):
                                graph.link_list[l].cons += value(model.b[p, c, s, d]) * model.phi[(l, p, s, d)] * chains.chains_list[chains.name_to_num(c)].tra / graph.link_list[l].ban                     
                nodes_set = []
                batch_chains = []
                sources = []
                destinations = []
                cnt = 0
    
        end_time = time.time()
        node_cpu_cap = []
        node_mem_cap = []
        for v in range(graph.nodes_num()):
            node_cpu_cap.append(graph.node_list[v].cons_cpu * 100)
            node_mem_cap.append(graph.node_list[v].cons_mem * 100)
        
        link_cap = []
        for l in range(len(graph.link_list)):
            link_cap.append(graph.link_list[l].cons * 100)
        
        print('MILP batch:', sum(node_cpu_cap))
        return max(node_cpu_cap), sum(node_cpu_cap)/len(node_cpu_cap), max(link_cap), sum(link_cap)/len(link_cap), end_time - start_time 
            
        