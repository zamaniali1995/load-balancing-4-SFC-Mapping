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

class MILP_model:
    def __init__(self):
        self.input_cons = InputConstants.Inputs()
        
    def run(self, graph, chains, functions, k, alpha):
        start_time =time.time()
        M = 100000
        ##########################################
        # Define concrete model
        ###########################################
        model = ConcreteModel()

        ###########################################
        # Sets
        ###########################################
        # Set of nodes: v
        model.V = graph.nodes_name
        # Set of functions: F
        model.F = range(functions.num())
        # Set of chains: C
        model.C = range(chains.num())
        # Set of sources and destinations: S, D
        for c in chains.chains_list:
            for u in c.users:
                try:
                    model.S.append(u[0])
                    model.D.append(u[1])
                except:
                    model.S = []
                    model.D = []
                    model.S.append(u[0])
                    model.D.append(u[1])
        model.S = list(dict.fromkeys(model.S))
        model.D = list(dict.fromkeys(model.D))
        # k_path function
        model.k_path = graph.k_path
        # Set of k paths
        model.P = range(k)
        # Set of function of each chain
        model.nc = []
        for c in model.C:
            model.nc.append(chains.funs_num(chains.chains_list[c].name))
        # cpus usage of each function
        model.nf = []
        for f in functions.functions_list.keys():
            model.nf.append(functions.cpu_usage(f))
        # mem usage of each function
        model.mf = []
        for f in functions.functions_list.keys():
            model.mf.append(functions.mem_usage(f))
        # Set of users
        model.L = range(graph.links_num())
        model.R = []
        for c in model.C:
            model.R.append(chains.chains_list[c].users)
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
                    if chains.chains_list[c].fun[i] == f_name:
                        model.I[(f_num, i, c)] = 1
                    else:
                        model.I[(f_num, i, c)] = 0
        
        ###########################################
        # Variables
        ###########################################
        max_fun = max([model.nc[c] for c in model.C])
        model.t = Var(within=NonNegativeReals)
        model.t_prime = Var(within=NonNegativeReals)
        model.a = Var(model.V, model.C, model.P, range(max_fun), model.S, model.D, within=Binary)
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
        for v_num, v in enumerate(model.V):
            model.balance_CPU_cons.add(sum([model.a[v, c, p, i, s, d] *
                                            model.I[(f, i, c)] *
                                            model.nf[f] *
                                            chains.chains_list[c].tra /
                                            graph.node_list[v_num].cap_cpu
                                            for c in model.C
                                            for s, d in model.R[c]
                                            for p in model.P
                                            for i in range(model.nc[c])
                                            for f in model.F
                                            ]) 
                                            <= model.t
                                       )
        
        # 2nd constraint
        model.node_CPU_cap_cons = ConstraintList()
        model.node_CPU_cap_cons.add(model.t <= 1)
        
        # 3rd constraint
        model.node_memory_cap_cons = ConstraintList()
        for v_num, v in enumerate(model.V):
            model.node_memory_cap_cons.add(sum([model.a[v, c, p, i, s, d] *
                                                model.I[(f, i, c)] *
                                                model.mf[f] *
                                                chains.chains_list[c].tra /
                                                graph.node_list[v_num].cap_mem
                                                for c in model.C
                                                for (s, d) in model.R[c]
                                                for p in model.P
                                                for i in range(model.nc[c])
                                                for f in model.F
                                                ])
                                           <=
                                           1)

        # 4th constraint
        model.link_balance_cons = ConstraintList()
        for l in model.L:
            model.link_balance_cons.add(sum([model.b[p, c, s, d] *
                                            model.phi[(l, p, s, d)] *
                                            chains.chains_list[c].tra /
                                            graph.link_list[l].ban
                                            for c in model.C
                                            for (s, d) in model.R[c]
                                            for p in range(len(model.k_path(s, d, k)))
                                            ])
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
        opt.options['timelimit'] = 2000
        results = opt.solve(model)

        node_cpu_cap = []
        node_mem_cap = []
        cpu = 0
        mem = 0
        for v_num, v in enumerate(model.V):
            for c in model.C:
                for (s, d) in model.R[c]:
                    for p in model.P:
                        for i in range(model.nc[c]):
                            for f in model.F:
                                cpu += value(model.a[v, c, p, i, s, d]) * model.I[(f, i, c)] * model.nf[f] * chains.chains_list[c].tra
                                mem += value(model.a[v, c, p, i, s, d]) * model.I[(f, i, c)] * model.mf[f] * chains.chains_list[c].tra
            node_cpu_cap.append(cpu / graph.node_list[v_num].cap_cpu * 100)
            node_mem_cap.append(mem / graph.node_list[v_num].cap_mem *100)
            cpu = 0
            mem = 0
        link = 0
        link_cap = []
        for l in model.L:
            for c in model.C:
                for (s, d) in model.R[c]:
                    for p in range(len(model.k_path(s, d, k))):
                        link += value(model.b[p, c, s, d]) * model.phi[(l, p, s, d)] * chains.chains_list[c].tra
            link_cap.append(link / graph.link_list[l].ban * 100)
            link = 0
        end_time = time.time()
        print('MILP: {}'.format(sum(node_cpu_cap)))
        return max(node_cpu_cap), sum(node_cpu_cap)/len(node_cpu_cap), max(link_cap),\
        sum(link_cap)/len(link_cap), end_time - start_time
   