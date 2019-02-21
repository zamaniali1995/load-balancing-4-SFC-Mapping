#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Siun Jan 27 16:44:41 2019
@author: ali
"""
#from pyomo.environ import *
from coopr.pyomo import *
model = ConcreteModel()
model.x_1 = Var(within=Binary)
model.x_2 = Var(within=Binary)
model.obj = Objective(expr=model.x_1, sense=minimize)
model.con1 = Constraint(expr=model.x_1  >= 0.5)
#model.con2 = Constraint(expr=2*model.x_1 + 5*model.x_2 >= 2)
model.pprint()
opt = SolverFactory("glpk")
results = opt.solve(model)
results.write()