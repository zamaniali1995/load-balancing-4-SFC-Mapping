#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Siun Jan 27 16:44:41 2019
@author: ali(zamaniali1995@gmail.com)
"""
from coopr.pyomo import *
# Must be changed
node_num = 14
func_num = 5
source_distinations = {
    "chain_1": [(1, 1), (2, 14), (3, 13)], 
    "chain_2": [(1, 1), (2, 14), (3, 13)],
    "chain_3": [(1, 1), (2, 14), (3, 13)],
}
k_path = {
    (1, 1): [(1, 2, 1), (1, 3, 1)],
    (2, 14): [(2, 3, 5, 14), (2, 3, 6, 14)],
    (3, 13): [(3, 4, 5, 13), (3, 4, 6, 13)]
}
###########################################
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

###########################################
# Variables
###########################################
model_1.t = Var(within=NonNegativeReals)
model_1.a = Var(model_1.V, model_1.F, within= Binary)

###########################################
# Objective function: min. t
###########################################
model_1.obj = Objective(expr= model_1.t, sense= minimize)

###########################################
# Constraints
###########################################
# 1st constraint
model_1.balance_constraints = ConstraintList()
for v in model_1.V:
    model_1.balance_constraints.add(sum([model_1.a[v, f] for f in model_1.F]) <= model_1.t)
# 2nd constraint

model_1.pprint()
