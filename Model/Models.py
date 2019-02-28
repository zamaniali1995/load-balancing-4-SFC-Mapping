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
        model_1.V = range(node_num)
        # Set of functions: F
        model_1.F = range(func_num)
        # Set of chains: C
        model_1.C = range(chain_num)
        # Set of sources: S
        model_1.S = graph.node_name_list
        # Set of distinations: D
        model_1.D = graph.node_name_list
        # Set of K shortest paths: K_sd
        model_1.K_sd = k_path
        # Set of k paths
        model_1.p = range(self.input_cons.k_path_num)
        # Set of function of each chain
        model_1.i = range(5)
        ###########################################
        # Variables
        ###########################################
        model_1.t = Var(within=NonNegativeReals)
        model_1.a = Var(model_1.V, model_1.C, model_1.F, model_1.S, model_1.D, within= Binary)
        model_1.b = Var(model_1.p, model_1.C, model_1.S, model_1.D, within= Binary)
        model_1.d = Var(model_1.i, model_1.C, model_1.S, model_1.D, within= Binary)
        ###########################################
        # Objective function: min. t
        ###########################################
        model_1.obj = Objective(expr= model_1.t, sense= minimize)

        ###########################################
        # Constraints
        ##########################################
        # # 1st constraint
        # model_1.balance_cons = ConstraintList()
        # for v in model_1.V:
        #     model_1.balance_cons.add(sum([model_1.a[c, v, f] for c in model_1.C 
        #                                                      for f in model_1.F
        #                                                      ]) <= model_1.t)
        # # 2nd constraint
        # model_1.path_cons = ConstraintList()
        # for c in model_1.C:
        #     for sd in chains[c].users:
        #         s = sd[0]
        #         d = sd[1]
        #         model_1.path_cons.add(sum([model_1.b[s, d, p, c] for p in model_1.K_sd]) == 1)
        opt = SolverFactory("glpk")
        results = opt.solve(model_1) 
        model_1.pprint()


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