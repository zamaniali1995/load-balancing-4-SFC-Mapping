from coopr.pyomo import *
import  time
import matplotlib.pyplot as plt1
import InputConstants
class Two_step_algorithm:
    def __init__(self):
        self.input_cons = InputConstants.Inputs()
    def create(self, graph, chain, k_paths, function):
        start_time = time.time()
        # graph.link_list[0].cap = 0
        cpu = 0
        mem = 0
        node_cpu_cap = []
        node_mem_cap = []

        for c in chain:
            for u in c.users:
                k_path = k_paths[u]
                # print("user {} wanna get service".format(u))
                path_num = self.__path_selection(graph, k_path, function, c)

                # print("path {} and is {} ".format(path_num, k_path[path_num]))
                self.__node_selection(graph, c, k_path[path_num], function)
                # print("path num:", path_num)
                # print("-------------------------------------------------")
        for v in range(len(graph.node_list)):
            node_cpu_cap.append(graph.node_list[v].cons_cpu * 100)
            node_mem_cap.append(graph.node_list[v].cons_mem * 100)
            # for c in chain:
            # #     print(graph.node_list[v].fun)
            #     for f in graph.node_list[v].fun[c.name]:
            #         cpu += graph.function_cpu_usage(f) * c.tra
            #         mem += graph.function_memory_usage(f) * c.tra

            #     print("in node {}, function {} of chain {} is deployed".format(v_.name, f, c.name))
            # node_cpu_cap.append(cpu / graph.node_list[v].cap_cpu * 100)
            # node_mem_cap.append(mem / graph.node_list[v].cap_mem * 100)
            # cpu = 0
            # mem = 0
        link_cap = []
        link_name = []
        for l in range(len(graph.link_list)):
            link_cap.append(graph.link_list[l].cons / graph.link_list[l].ban * 100)
            link_name.append(l)
        end_time = time.time()
        # print(node_cap)
        with open('./Results/Heuristic/heuristic_cpu.txt', 'w') as f:
            print(node_cpu_cap, file=f)
        # plt1.bar(graph.node_name_list, node_cpu_cap)
        # plt.show()
        # plt1.savefig('result_cpu_Heuristic.png')
        # plt1.close()
        with open('./Results/Heuristic/heuristic_memory.txt', 'w') as f:
            print(node_mem_cap, file=f)
        # plt1.bar(graph.node_name_list, node_mem_cap)
        # plt.show()
        # plt1.savefig('result_mem_Heuristic.png')
        # plt1.close()
        with open('./Results/Heuristic/huristic_link', 'w') as f:
            print(link_cap, file=f)
        # plt1.bar(link_name, link_cap)
        # plt.show()
        # plt1.savefig('result_link_Heuristic.png')
        # plt1.close()
        with open('./Results/Heuristic/heuristic_info.txt', 'w') as f:
            print('time:', end_time-start_time, file=f)
            print('k_path:', self.input_cons.k_path_num, file=f)
            print('alpha:', self.input_cons.alpha, file=f)
        # print(node_cap)

    def __path_selection(self, graph, k_path, function, c):
        path_cost =[]
        link_cap = 0
        cpu = 0
        nodes_cpu_cap = 0
        nodes_mem_cap = 0
        mem = 0
        len_paths = 0
        for k in k_path:
            len_paths += len(k)
        for k in k_path:
            for n in range(len(k) - 1):
                for l in range(len(graph.link_list)):
                    if (k[n], k[n + 1]) == graph.link_list[l].name:
                        link_cap += graph.link_list[l].cons / graph.link_list[l].ban
                        break
            link_cap = link_cap / (len(k) - 1)
            for n in k:
                for m in range(len(graph.node_list)):
                    if graph.node_list[m].name == n:
                        cpu += graph.node_list[m].cons_cpu
                        mem += graph.node_list[m].cons_mem
                        # for _key in graph.node_list[m].fun.keys():
                        #     for f in graph.node_list[m].fun[_key]:
                        #         node_cpu_cap += function[f][self.input_cons.cpu_usage]
                        #         node_mem_cap += function[f][self.input_cons.memory_usage]
                        break
                        # node_cpu_cap = node_cpu_cap / graph.node_list[m].cap_cpu
                        # node_mem_cap = node_mem_cap / graph.node_list[m].cap_mem
                # nodes_cpu_cap += node_cpu_cap
                # node_cpu_cap = 0
                # nodes_mem_cap += node_mem_cap
                # node_mem_cap = 0
            cpu /= len(k)
            mem /= len(k)
            # print(len(k), len_paths)
            # print("link cap is {} and cpu is {} and mem is {}".format(link_cap, cpu, mem))
            path_cost.append((1 - self.input_cons.alpha) * link_cap +
                             self.input_cons.alpha *
                             # (max(nodes_cpu_cap, nodes_mem_cap))
                             (cpu + mem) / 2 +
                             len_paths / len(k) * 0.001
                             )
            link_cap = 0
            cpu = 0
            mem = 0
        # print("paths cost is {}".format(path_cost))
        minimum = float("inf")
        idx = 0
        for i_, i in enumerate(path_cost):
            if i <= minimum:
                # print(i)
                idx = i_
                minimum = i
        # print(k_path[idx])
        # print("---------------------------------")
        # idx = path_cost.index(min(path_cost))
        for n in range(len(k_path[idx])-1):
            for l in range(len(graph.link_list)):
                # print("path {}".format(graph.link_list[l].name))
                if graph.link_list[l].name == (k_path[idx][n], k_path[idx][n+1]):
                    graph.link_list[l].cons += c.tra
                    # print()
                    # print(graph.link_list[l].name, k_path[idx][n], k_path[idx][n+1])
                    break
        # print(idx, path_cost, k_path[idx])
        return idx

    def __node_selection(self, graph, chain, path, functions):
        node_cap_cpu_list = []
        node_cpu_cap = 0
        nodes_cpu_cap = 0
        node_mem_cap = 0
        node_cap_mem_list = []
        f_num = 0
        # print(path)
        for n in path:
            # print(n)
            for m in range(len(graph.node_list)):
                if graph.node_list[m].name == n:
                    # print("ok")
                    for _key in graph.node_list[m].fun.keys():
                        for f in graph.node_list[m].fun[_key]:
                            node_cpu_cap += functions[f][self.input_cons.cpu_usage]
                            node_mem_cap += functions[f][self.input_cons.memory_usage]

                # node_cap = node_cap
            node_cap_cpu_list.append(node_cpu_cap / graph.node_list[m].cap_cpu)
            node_cap_mem_list.append(node_mem_cap / graph.node_list[m].cap_mem)
            node_cpu_cap = 0
            node_mem_cap = 0
            # nodes_cap += node_cap
            # node_cap = 0
            # nodes_cap = nodes_cap / len(path)
            # print(node_cap_list)

        # print(node_cap_list)
        # print("amout of cpu that is accupaid: {}".format(node_cap_cpu_list))
        # print("amout of cpu that is accupaid: {}".format(node_cap_mem_list))
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
        model.balance_cpu_cons = ConstraintList()
        for v in model.V:
            for v_ in range(len(graph.node_list)):
                if v == graph.node_list[v_].name:
                    v_num = v_
                    break
            model.balance_cpu_cons.add(sum([model.a[v, f] *
                                        model.nf[f] *
                                        chain.tra /
                                        graph.node_list[v_num].cap_cpu
                                        for f in model.F
                                        ]) +
                                   graph.node_list[v_num].cons_cpu
                                   <=
                                   model.t)
        model.cap_cpu_cons = ConstraintList()
        for v in model.V:
            for v_ in range(len(graph.node_list)):
                if v == graph.node_list[v_].name:
                    v_num = v_
                    break
            model.cap_cpu_cons.add(sum([model.a[v, f] *
                                        model.nf[f] *
                                        chain.tra /
                                        graph.node_list[v_num].cap_cpu
                                        for f in model.F
                                        ]) +
                                   graph.node_list[v_num].cons_cpu
                                   <=
                                   1)
        # 1st constraint
        model.balance_mem_cons = ConstraintList()
        for v in model.V:
            for v_ in range(len(graph.node_list)):
                if v == graph.node_list[v_].name:
                    v_num = v_
                    break
            model.balance_mem_cons.add(sum([model.a[v, f] *
                                        model.mf[f] *
                                        chain.tra /
                                        graph.node_list[v_num].cap_mem
                                        for f in model.F
                                        ]) +
                                   graph.node_list[v_num].cons_mem
                                   <=
                                   model.t)
        model.cap_mem_cons = ConstraintList()
        for v in model.V:
            for v_ in range(len(graph.node_list)):
                if v == graph.node_list[v_].name:
                    v_num = v_
                    break
            model.cap_mem_cons.add(sum([model.a[v, f] *
                                            model.mf[f] *
                                            chain.tra /
                                            graph.node_list[v_num].cap_mem
                                            for f in model.F
                                            ]) +
                                       graph.node_list[v_num].cons_mem
                                       <=
                                       1)

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
        # "cplex", executable="/opt/ibm/ILOG/CPLEX_Studio_Community128/cplex/bin/x86-64_linux/cplex"
        opt = SolverFactory("cplex", executable="/opt/ibm/ILOG/CPLEX_Studio128/cplex/bin/x86-64_linux/cplex")
        # opt.options["threads"] = 4
        results = opt.solve(model)
        # model.seq_cons.pprint()
        # model.a.pprint()
        mem = 0
        cpu = 0
        node_cpu_cap = []
        node_mem_cap = []

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
                    mem += value(model.a[v, f]) * model.mf[f] * chain.tra
                    cpu += value(model.a[v, f]) * model.nf[f] * chain.tra
                    # graph.node_list[v_num].fun[chain.name].append(chain.fun[f])
                    graph.function_placement(v_num, chain.name, chain.fun[f])
            mem = mem / graph.node_list[v_num].cap_mem
            cpu = cpu / graph.node_list[v_num].cap_cpu
            graph.node_list[v_num].cons_cpu += cpu
            graph.node_list[v_num].cons_mem += mem
            node_mem_cap.append(mem)
            node_cpu_cap.append(cpu)
            cpu = 0
            mem = 0
        # print(node_cpu_cap, node_mem_cap)
        # for n in range(len(path)):
        #     for m in range(len(graph.node_list)):
        #         if graph.node_list[m].name == path[n]:
        #
        #             for f in chain.fun[f_num:]:
        #                 if (function[f] / graph.node_list[m].cap) <= (nodes_cap - node_cap_list[n]) and nodes_cap - node_cap_list[n] >= 0:
        #                     graph.function_palcement(path(n), chain.name, f)
        #                     f_num += 1
        #                     break


