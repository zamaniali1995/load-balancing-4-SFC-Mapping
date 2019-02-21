#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Siun Jan 27 16:44:41 2019
@author: ali
"""
#from pyomo.environ import *
from coopr.pyomo import *
warehouses_num = 3 
customers_num = 4
P = 2
d = {(0, 0): 1.7, (0, 1): 7.2, (0, 2): 9.0, (0, 3): 8.3,
     (1, 0): 2.9, (1, 1): 6.3, (1, 2): 9.8, (1, 3): 0.7,
     (2, 0): 4.5, (2, 1): 4.8, (2, 2): 4.2, (2, 3): 9.3}
model = ConcreteModel()
model.Locations = range(warehouses_num)
model.Customers = range(customers_num)
model.x = Var(model.Locations, model.Customers, bounds=(0.0, 1.0))
model.y = Var(model.Locations, within=Binary)
model.obj = Objective( expr = sum([d[n,m] * model.x[n, m] for n in model.Locations for m in model.Customers])) 
model.single_x = ConstraintList()
for m in model.Customers:
    model.single_x.add(
        sum([model.x[n, m] for n in model.Locations]) == 1.0
    ) 
model.bound_y = ConstraintList()
for n in model.Locations:
    for m in model.Customers:
        model.bound_y.add(model.x[n, m] <= model.y[n])
model.num_facilities = Constraint(
    expr = sum([model.y[n] for n in model.Locations]) == P
) 
opt = SolverFactory("glpk")
results = opt.solve(model)                             
model.pprint()
results.write()
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