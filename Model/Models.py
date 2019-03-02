#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Siun Jan 27 16:44:41 2019
@author: ali(zamaniali1995@gmail.com)
"""
from coopr.pyomo import *
import InputConstants
# Must be changed
class Model:
    def __init__(self):
        self.input_cons = InputConstants.Inputs()

    def creat_model(self, graph, functions, chains, k_path):
        node_num = len(graph.node_list)
        func_num = len(functions)
        chain_num = len(chains)
        sou_num = node_num
        dist_num = node_num
        M = 100000
        # K_path_num = 2
        # chain_num = 3
        # source_distinations = [
        #     [(1, 1), (2, 14), (3, 13)], 
        #     [(1, 1), (2, 14), (3, 13)],
        #     [(1, 1), (2, 14), (3, 13)],
        # ]
        # k_path = {
        #     (1, 1): [(1, 2, 1), (1, 3, 1)],
        #     (2, 14): [(2, 3, 5, 14), (2, 3, 6, 14)],
        #     (3, 13): [(3, 4, 5, 13), (3, 4, 6, 13)]
        # }

        ##########################################
        # Define concrete model
        ###########################################
        model_1 = ConcreteModel()

        ###########################################
        # Sets
        ###########################################
        # Set of nodes: v
        model_1.V = graph.node_name_list
        # Set of functions: F
        model_1.F = range(func_num)
        # Set of chains: C
        model_1.C = range(chain_num)
        # Set of sources: S
        model_1.S = []
        for c in range(chain_num):
            for i in range(len(chains[c].users)):
                model_1.S.append(chains[c].users[i][0])
        # model_1.S = graph.node_name_list
        # Set of distinations: D
        model_1.D = []
        for c in range(chain_num):
            for i in range(len(chains[c].users)):
                model_1.D.append(chains[c].users[i][1])
        # model_1.D = graph.node_name_list
        # Set of K shortest paths: K_sd
        model_1.k_path = k_path
        # Set of k paths
        model_1.p = range(self.input_cons.k_path_num)
        # Set of function of each chain
        nc = []
        model_1.nc = []
        for c in range(chain_num):
            nc.append(len(chains[c].fun))
            tmp = range(len(chains[c].fun))
            model_1.nc.append(tmp)
        model_1.nf = []
        for f in functions.keys():
            model_1.nf.append(functions[f])
        # model_1.nf = nf
        # model_1.i(C) = 
        # Set of users
        model_1.R = []
        for c in range(chain_num):
            model_1.R.append(chains[c].users)  
        # Nodes capacity  
        model_1.n = graph.node_list[0].cap
        # Set of IDs
        model_1.I = {}
        I = {}
        for c in range(chain_num):
            for f_num, f_name in enumerate(functions.keys()):
                for i in range(nc[c]):
                    if chains[c].fun[i] == f_name:
                        I[(f_num, i, c)] = 1
                        model_1.I[(f_num, i, c)] = 1
                    else :
                        I[(f_num, i, c)] = 0
                        model_1.I[(f_num, i, c)] = 0
        # print(model_1.I)
        ###########################################
        # Variables
        ###########################################
        model_1.t = Var(within=NonNegativeReals)
        # model_1.a = Var(model_1.V, model_1.C, model_1.F, model_1.S, model_1.D, within= Binary)
        model_1.a = Var(model_1.V, model_1.C, model_1.nc[0], model_1.S, model_1.D, within= Binary)
        model_1.b = Var(model_1.p, model_1.C, model_1.S, model_1.D, within= Binary)
        # model_1.d = [] * 4
        # for c in model_1.C:
        model_1.d = Var(model_1.nc[0], model_1.C, model_1.S, model_1.D, within= Binary)
        ###########################################
        # Objective function: min. t
        ###########################################
        model_1.obj = Objective(expr= model_1.t, sense= minimize)

        ###########################################
        # Constraints
        ##########################################
        # 1st constraint
        model_1.balance_cons = ConstraintList()
        for v in model_1.V:
            model_1.balance_cons.add(sum([model_1.a[v, c, i, s, d] * 
                                          model_1.I[(f, i, c)] *
                                          model_1.nf[f] * 
                                          1 
                                                             for c in model_1.C 
                                                             for s, d in model_1.R[c]
                                                             for i in model_1.nc[c]
                                                             for f in model_1.F
                                                             ]) 
                                                             <= 
                                                             model_1.t)
        # 2nd constraint
        model_1.node_cap_cons = ConstraintList()
        for v in model_1.V:
            model_1.node_cap_cons.add(sum([model_1.a[v, c, i, s, d] * 
                                          model_1.I[(f, i, c)] *
                                          model_1.nf[f] * 
                                          1 
 
                                                             for c in model_1.C 
                                                             for (s, d) in model_1.R[c]
                                                             for i in model_1.nc[c]
                                                             for f in model_1.F
                                                             ]) 
                                                             <= 
                                                             model_1.n)
        # 3rd constraint
        
        
        
        # 4th constraint
        model_1.path_selection_cons = ConstraintList()
        for c in model_1.C:
            for (s, d) in model_1.R[c]:
                model_1.path_selection_cons.add(sum([model_1.b[p , c, s, d] 
                                                for p in range(len(model_1.k_path[(s, d)]))
                                                ])
                                                ==
                                                1
                                                )
        # 5th constraint
        model_1.satisfy_req_1_cons = ConstraintList()
        for c in model_1.C:
            for (s, d) in model_1.R[c]:
                for i in model_1.nc[c]:
                    for p in range(len(k_path[(s, d)])):
                        model_1.satisfy_req_1_cons.add(sum([
                            model_1.a[v, c, i, s, d]  
                            for v in model_1.k_path[(s, d)][p]
                            
                        ])
                        <=
                        1 + M * (1 - model_1.b[p, c, s, d])
                        )
                # 5th constraint
        model_1.satisfy_req_2_cons = ConstraintList()
        for c in model_1.C:
            for (s, d) in model_1.R[c]:
                for i in model_1.nc[c]:
                    for p in range(len(k_path[(s, d)])):
                        model_1.satisfy_req_2_cons.add(sum([
                            model_1.a[v, c, i, s, d]  
                            for v in model_1.k_path[(s, d)][p]
                            
                        ])
                        >=
                        1 - M * (1 - model_1.b[p, c, s, d])
                        )
        # 5th constraint
        # model_1.satisfy_req_1_cons = ConstraintList()
        # for c in model_1.C:
        #     for (s, d) in model_1.R[c]:
        #         model_1.satisfy_req_1_cons.add(sum([model_1.d[i, c, s, d]
        #                                         for i in model_1.nc[c]
        #                                         ])
        #                                         == 
        #                                         nc[c]
        #                                         )
        # # 6th constraint:
        # model_1.satisfy_req_2_cons = ConstraintList()
        # for c in model_1.C:
        #     for (s, d) in model_1.R[c]:
        #         for i in model_1.nc[c]:
        #             model_1.satisfy_req_2_cons.add(sum([
        #                 model_1.a[v, c, f, s, d] * model_1.I[(f, i, c)]
        #                                     for v in model_1.V
        #                                     for f in model_1.F
        #             ])
        #              <=
        #             model_1.d[i, c, s, d])
        # # 7th constraint:
        # model_1.satisfy_req_3_cons = ConstraintList()
        # for c in model_1.C:
        #     for (s, d) in model_1.R[c]:
        #         for f in model_1.F:
        #             model_1.satisfy_req_3_cons.add(sum([
        #                 model_1.d[i, c, s, d] * model_1.I[(f, i, c)]
        #                 for i in model_1.nc[c]
        #             ])
        #             <=
        #             sum([
        #                 model_1.a[v, c, f, s, d]
        #                 for v in model_1.V
        #             ])
        #             )
        # # 8th constraint:
        # model_1.deploy_on_path_cons = ConstraintList()
        # for c in model_1.C:
        #     for (s, d) in model_1.R[c]:
        #         for p in model_1.p:
        #             if len(k_path[(s, d)]) >= p + 1:
        #                 model_1.deploy_on_path_cons.add(sum([
        #                     model_1.a[v, c, f, s, d]
        #                     for v in k_path[(s, d)][p]
        #                     for f in model_1.F
        #             ])
        #             <= 
        #             model_1.b[p, c, s, d]
        #             )
        # 9th constraint:
        model_1.seq_cons = ConstraintList()
        for c in model_1.C:
            for (s, d) in model_1.R[c]:
                for p in range(len(model_1.k_path[(s, d)])):
                    for i in range(nc[c] - 1):
                        for v in model_1.k_path[(s, d)][p]:
                            model_1.seq_cons.add(sum([
                                model_1.a[v, c, i_1, s, d]
                                for v_1 in model_1.V[: len(graph.node_list) - 1]
                                for i_1 in range(i+1, nc[c])
                            ])
                            <=
                            M * (2 - model_1.b[p, c, s, d] - model_1.a[v, c, i, s, d])
                            )



        # model_1.pprint()
        # # 2nd constraint
        # model_1.path_cons = ConstraintList()
        # for c in model_1.C:
        #     for sd in chains[c].users:
        #         s = sd[0]
        #         d = sd[1]
        #         model_1.path_cons.add(sum([model_1.b[s, d, p, c] for p in model_1.K_sd]) == 1)
        opt = SolverFactory("cbc")
        opt.options["threads"] = 4
        results = opt.solve(model_1) 
        # model_1.pprint()
        node_cap = []
        tmp = 0
        for v in model_1.V:
            for c in model_1.C:
                for i in range(14):
                    for (s, d) in model_1.R[c]:
                        # print(value(model_1.a[v, c, i, s, d]))
                        tmp += value(model_1.a[v, c, i, s, d])
            node_cap.append(tmp)
            tmp = 0
        # model_1.a.pprint()
        # model_1.b.pprint()
        # model_1.path_selection_cons.pprint()
        # model_1.balance_cons.pprint()
        model_1.satisfy_req_1_cons.pprint()
        model_1.b.pprint()
        model_1.a.pprint()
        # print(I)
        # print(k_path[("1", "2")])
        print(node_cap)
        # print(results)
        # model_1.satisfy_req_1_cons.pprint()
        # print(model_1.balancke_cons)


############################################################################
#from pyomo.environ import *
# from coopr.pyomo import *
# warehouses_num = 3 
# customers_num = 4
# P = 2
# d = {(0, 0): 1.7, (0, 1): 7.2, (0, 2): 9.0, (0, 3): 8.3,
#      (1, 0): 2.9, (1, 1): 6.3, (1, 2): 9.8, (1, 3): 0.7,
#      (2, 0): 4.5, (2, 1): 4.8, (2, 2): 4.2, (2, 3): 9.3}
# model = ConcreteModel()
# model.Locations = range(warehouses_num)
# model.Customers = range(customers_num)
# model.x = Var(model.Locations, model.Customers, bounds=(0.0, 1.0))
# model.y = Var(model.Locations, within=Binary)
# model.obj = Objective( expr = sum([d[n,m] * model.x[n, m] for n in model.Locations for m in model.Customers])) 
# model.single_x = ConstraintList()
# for m in model.Customers:
#     model.single_x.add(
#         sum([model.x[n, m] for n in model.Locations]) == 1.0
#     ) 
# model.bound_y = ConstraintList()
# for n in model.Locations:
#     for m in model.Customers:
#         model.bound_y.add(model.x[n, m] <= model.y[n])
# model.num_facilities = Constraint(
#     expr = sum([model.y[n] for n in model.Locations]) == P
# ) 
# opt = SolverFactory("glpk")
# results = opt.solve(model)                             
# model.pprint()
# results.write()
# model = ConcreteModel()
# model.x_1 = Var(within=Binary)
# model.x_2 = Var(within=Binary)
# model.obj = Objective(expr=model.x_1, sense=minimize)
# model.con1 = Constraint(expr=model.x_1  >= 0.5)
# model.con2 = Constraint(expr=2*model.x_1 + 5*model.x_2 >= 2)
# model.pprint()
# opt = SolverFactory("glpk")
# results = opt.solve(model)
# results.write()