from coopr.pyomo import *
import matplotlib.pyplot as plt1
import InputConstants
class Two_step_algorithm:
    def __init__(self):
        self.input_cons = InputConstants.Inputs()
    def create(self, graph, chain, k_paths, function):
        graph.link_list[0].cap = 0
        tmp = 0
        node_cap = []
        for c in chain:
            for u in c.users:
                k_path = k_paths[u]
                path_num = self.__path_selection(graph, k_path, function)
                self.__node_selection(graph, c, k_path[path_num], function)
                # print("path num:", path_num)
                # print("-------------------------------------------------")
        for v, v_ in enumerate(graph.node_list):
            for c in chain:
            #     print(graph.node_list[v].fun)
                for f in graph.node_list[v].fun[c.name]:
                    tmp += graph.function_cpu_usage(f)
                #     print("in node {}, function {} of chain {} is deployed".format(v_.name, f, c.name))
            node_cap.append(tmp)
            tmp = 0
        print(node_cap)
        plt1.bar(graph.node_name_list, node_cap)
        # plt.show()
        plt1.savefig('result_Heuristic.png')
        # print(node_cap)

    def __path_selection(self, graph, k_path, function):
        path_cost =[]
        link_cap = 0
        node_cap = 0
        nodes_cap = 0
        for k in k_path:
            for n in range(len(k) - 1):
                for l in range(len(graph.link_list)):
                    if (k[n], k[n + 1]) == graph.link_list[l].name:
                        link_cap += graph.link_list[l].cap
                        break
            link_cap = link_cap / (len(k) - 1)
            for n in k:
                for m in range(len(graph.node_list)):
                    if graph.node_list[m].name == n:
                        for _key in graph.node_list[m].fun.keys():
                            for f in graph.node_list[m].fun[_key]:
                                node_cap += function[f][self.input_cons.cpu_usage]
                        break
                        node_cap = node_cap / graph.node_list[m].cap
                nodes_cap += node_cap
                node_cap = 0
            nodes_cap = nodes_cap / len(k)
            path_cost.append(link_cap + nodes_cap)
            link_cap = 0
            nodes_cap = 0
            idx = path_cost.index(min(path_cost))
            for n in range(len(k_path[idx])-1):
                for l in range(len(graph.link_list)):
                    if graph.link_list[l].name == (k_path[idx][n], k_path[idx][n+1]):
                        graph.link_list[l].cap += 10
                        break
        return  idx
    def __node_selection(self, graph, chain, path, functions):
        node_cap_list = []
        node_cap = 0
        nodes_cap = 0
        f_num = 0
        # print(path)
        for n in path:
            # print(n)
            for m in range(len(graph.node_list)):
                if graph.node_list[m].name == n:
                    # print("ok")
                    for _key in graph.node_list[m].fun.keys():
                        for f in graph.node_list[m].fun[_key]:
                            node_cap += functions[f][self.input_cons.cpu_usage]

                # node_cap = node_cap
            node_cap_list.append(node_cap)
            nodes_cap += node_cap
            node_cap = 0
            nodes_cap = nodes_cap / len(path)
            # print(node_cap_list)

        # print(node_cap_list)
        M = 10000
        ##########################################
        # Define concrete model
        ###########################################
        model = ConcreteModel()
        # print("-------------------------")
        ###########################################
        # Sets
        ###########################################
        # Set of nodes: v
        model.V = path
        # Set of functions: F
        model.F = range(len(chain.fun))
        model.nf = []
        for f in functions.keys():
            model.nf.append(functions[f][self.input_cons.cpu_usage])
        model.mf = []
        for f in functions.keys():
            model.mf.append(functions[f][self.input_cons.memory_usage])

        ###########################################
        # Variables
        ###########################################
        model.t = Var(within=NonNegativeReals)
        model.a = Var(model.V, model.F, within=Binary)
        ###########################################
        # Objective function: min. t
        ###########################################
        model.obj = Objective(expr=model.t, sense=minimize)

        ###########################################
        # Constraints
        ##########################################
        # 1st constraint
        model.balance_cons = ConstraintList()
        for v_num, v in enumerate(model.V):
            model.balance_cons.add(sum([model.a[v, f] *
                                        model.nf[f] *
                                        1
                                        for f in model.F
                                        ]) +
                                   node_cap_list[v_num]
                                   <=
                                   model.t)

        model.satisfy_req_2_cons = ConstraintList()
        for f in model.F:
            model.satisfy_req_2_cons.add(sum([
                model.a[v, f]
                for v in model.V
            ])
                                         ==
                                         1
                                         )
        model.seq_cons = ConstraintList()
        for v_num, v in enumerate(model.V):
            for f in model.F:
                if v_num != 0:
                    model.seq_cons.add(sum([
                    model.a[v_1, f_1]
                    for v_1 in model.V[: v_num]
                    for f_1 in range(f + 1, len(chain.fun))
                                ])
                                <=
                                M * (1 - model.a[v, f])
                                )
        opt = SolverFactory("glpk")
        # "cplex", executable="/opt/ibm/ILOG/CPLEX_Studio_Community128/cplex/bin/x86-64_linux/cplex"
        # opt.options["threads"] = 4
        results = opt.solve(model)
        # model.seq_cons.pprint()
        # model.a.pprint()
        tmp = 0
        node_cap1 = []
        # for v in range(len(graph.node_list)):
            # print(graph.node_list[v].fun)
        for v in model.V:
            for v_ in range(len(graph.node_list)):
                if graph.node_list[v_].name == v:
                    v_num = v_
                    break
            for f in model.F:
                if value(model.a[v, f]):
                    # print("ok")
                    # print(value(model.a[v, c, i, s, d]))
                    tmp += value(model.a[v, f])
                    # graph.node_list[v_num].fun[chain.name].append(chain.fun[f])
                    graph.function_placement(v_num, chain.name, chain.fun[f])
            node_cap1.append(tmp)
            tmp = 0
        # print(node_cap1)
        # for n in range(len(path)):
        #     for m in range(len(graph.node_list)):
        #         if graph.node_list[m].name == path[n]:
        #
        #             for f in chain.fun[f_num:]:
        #                 if (function[f] / graph.node_list[m].cap) <= (nodes_cap - node_cap_list[n]) and nodes_cap - node_cap_list[n] >= 0:
        #                     graph.function_palcement(path(n), chain.name, f)
        #                     f_num += 1
        #                     break


