from coopr.pyomo import *
import  time
# import matplotlib.pyplot as plt
import InputConstants
# from PaperFunctions import Graph, Chains
class heuristic_offline_model:
    def __init__(self, k, alpha):
        self.input_cons = InputConstants.Inputs()
        self.k = k
        self.alpha = alpha
    def run(self, graph, chains, function): 
        start_time = time.time()
        # graph.link_list[0].cap = 0
        cpu = 0
        mem = 0
        node_cpu_cap = []
        node_mem_cap = []
        chains_usage = []
        for c in chains.chains_list:
            for u in c.users:
                chains_usage.append([c, u, c.cpu_usage * c.tra])
        chains_usage.sort(key=lambda x: x[2])
        # for c in chains.chains_list:
            # for u in c.users:
        for c, u, _ in chains_usage:
            k_path = graph.k_path(u[0], u[1], self.k)
            # print(k_path)
            # print("user {} wanna get service".format(u))
            path_num = self.__path_selection(graph, k_path, function, c)
            # print("ok")
            # print("path {} and is {} ".format(path_num, k_path[path_num]))
            self.__node_selection(graph, c, k_path[path_num], function)
            # print("path num:", path_num)
            # print("-------------------------------------------------")
        for v in range(graph.nodes_num()):
            node_cpu_cap.append(graph.node_list[v].cons_cpu * 100)
            node_mem_cap.append(graph.node_list[v].cons_mem * 100)
        
        link_cap = []
        link_name = []
        for l in range(len(graph.link_list)):
            link_cap.append(graph.link_list[l].cons / graph.link_list[l].ban * 100)
            link_name.append(l)
        end_time = time.time()
        # print("Heuristic time:", end_time-start_time)
        # with open('./Results/Heuristic/heuristic_cpu.txt', 'w') as f:
        #     print(node_cpu_cap, file=f)
        #     print("max of cpu usage", max(node_cpu_cap), file=f)
        #     print("sum of cpu usage", sum(node_cpu_cap), file=f)       
        # # plt1.bar(graph.node_name_list, node_cpu_cap)
        # plt.show()
        # plt1.savefig('result_cpu_Heuristic.png')
        # plt1.close()
        # with open('./Results/Heuristic/heuristic_memory.txt', 'w') as f:
        #     print(node_mem_cap, file=f)
        #     print("max of memory usage", max(node_mem_cap), file=f)
        #     print("sum of memory usage", sum(node_mem_cap), file=f)
        # # plt1.bar(graph.node_name_list, node_mem_cap)
        # plt.show()
        # plt1.savefig('result_mem_Heuristic.png')
        # plt1.close()
        # with open('./Results/Heuristic/heuristic_link.txt', 'w') as f:
        #     print(link_cap, file=f)
        #     print("bandwidth consumption:", sum(link_cap), file=f)
        #     print("max of link bandwidth:", max(link_cap), file=f)
        #     print("avg of link consumption: ", sum(link_cap) / len(link_cap), file=f)
        # # plt1.bar(link_name, link_cap)
        # plt.show()
        # plt1.savefig('result_link_Heuristic.png')
        # plt1.close()
        # with open('./Results/Heuristic/heuristic_info.txt', 'w') as f:
        #     print('time:', end_time-start_time, file=f)
        #     print('k_path:', self.input_cons.k_path_num, file=f)
        #     print('alpha:', self.input_cons.alpha, file=f)
        #     for c in chains.chains_list:
        #         print('chain {} has {} nember users'.format(c.name, chains.users_num(c.name)), file=f)
        return [max(node_cpu_cap), max(link_cap), end_time - start_time]
        # print(node_cap)



    def __path_selection(self, graph, k_path, function, c):
        path_cost =[]
        link_cap = 0
        link_cap_list = []
        cpu = []
        nodes_cpu_cap = 0
        nodes_mem_cap = 0
        mem = []
        tmp = []
        len_paths = 0
        for k in k_path:
            len_paths += len(k)
            tmp.append(len(k))
        min_len = min(tmp)
        for k in k_path:
            for n in range(len(k) - 1):
                l = graph.name_to_num_link((k[n], k[n + 1]))
                # for l in range(len(graph.link_list)):
                #     if (k[n], k[n + 1]) == graph.link_list[l].name:
                link_cap_list.append(graph.link_list[l].cons / graph.link_list[l].ban)

                        # break
            link_cap_avg = sum(link_cap_list) / (len(k) - 1)
            link_cap_max = max(link_cap_list)
            # cpu_max = []
            # mem_max = []               
            cpu = []
            mem = []
            for n in k:
                m = graph.name_to_num_node(n)
                # for m in range(len(graph.node_list)):
                #     if graph.node_list[m].name == n:
                        # cpu_max.append(graph.node_list[m].cons_cpu)
                        # mem = 
                cpu.append(graph.node_list[m].cons_cpu) 
                mem.append(graph.node_list[m].cons_mem)
                        # for _key in graph.node_list[m].fun.keys():
                        #     for f in graph.node_list[m].fun[_key]:
                        #         node_cpu_cap += function[f][self.input_cons.cpu_usage]
                        #         node_mem_cap += function[f][self.input_cons.memory_usage]
                        # break
                        # node_cpu_cap = node_cpu_cap / graph.node_list[m].cap_cpu
                        # node_mem_cap = node_mem_cap / graph.node_list[m].cap_mem
                # nodes_cpu_cap += node_cpu_cap
                # node_cpu_cap = 0
                # nodes_mem_cap += node_mem_cap
                # node_mem_cap = 0
            cpu_avg = sum(cpu) / len(k)
            mem_avg = sum(mem) / len(k)
            cpu_max = max(cpu) 
            mem_max = max(mem)
            # print(len(k), len_paths)
            # print("link cap is {} and cpu is {} and mem is {}".format(link_cap, cpu, mem))
            # print(mem_max)
            path_cost.append((1 - self.alpha) * ( link_cap_avg + link_cap_max + min_len / len(k) * (1 / (c.cpu_usage) ))/3 + 
                                  self.alpha * (cpu_max + cpu_avg)/2)
                
            link_cap = 0
            cpu = 0
            mem = 0
        # print("paths cost is {}".format(path_cost))

        # minimum = float("inf")
        # idx = 0
        # for i_, i in enumerate(path_cost):
        #     if i <= minimum:
        #         # print(i)
        #         idx = i_
        #         minimum = i

        # print(k_path[idx])
        # print("---------------------------------")
        idx = path_cost.index(min(path_cost))
        for n in range(len(k_path[idx])-1):
            l = graph.name_to_num_link((k_path[idx][n], k_path[idx][n+1]))
            # for l in range(len(graph.link_list)):
            #     # print("path {}".format(graph.link_list[l].name))
            #     if graph.link_list[l].name == (k_path[idx][n], k_path[idx][n+1]):
            graph.link_list[l].cons += c.tra
                    # print()
                    # print(graph.link_list[l].name, k_path[idx][n], k_path[idx][n+1])
                    # break
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
                            node_cpu_cap += functions.cpu_usage(f)
                            node_mem_cap += functions.mem_usage(f)

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
        # model.F = functions.names()
        # cpus usage of each function
        model.nc = range(len(chain.fun))
        model.nf = {}
        for i in model.nc:
            model.nf[i] = functions.cpu_usage(chain.fun[i])
        # mem usage of each function
        model.mf = {}
        for i in model.nc:
            model.mf[i] = functions.mem_usage(chain.fun[i])
        # model.I = {}
        # I = {}
        # for f_num, f_name in enumerate(model.F):
        # for f in model.F:
        #     for i in range(model.nc):
        #         if chain.fun[i] == f:
        #             model.I[(f, i)] = 1
        #         else:
        #             model.I[(f, i)] = 0
        ###########################################
        # Variables
        ###########################################
        model.t = Var(within=NonNegativeReals)
        model.a = Var(model.V, model.nc, within=Binary)
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
            v_num = graph.name_to_num_node(v)
            model.balance_cpu_cons.add(sum([model.a[v, i] *
                                            model.nf[i] *
                                            chain.tra /
                                            graph.node_list[v_num].cap_cpu
                                        for i in model.nc
                                        ]) +
                                   graph.node_list[v_num].cons_cpu
                                   <=
                                   model.t)
        model.cap_cpu_cons = ConstraintList()
        for v in model.V:
            v_num = graph.name_to_num_node(v)
            # for v_ in range(len(graph.node_list)):
            #     if v == graph.node_list[v_].name:
            #         v_num = v_
            #         break
            model.cap_cpu_cons.add(sum([model.a[v, i] *
                                        model.nf[i] *
                                        chain.tra /
                                        graph.node_list[v_num].cap_cpu
                                        for i in model.nc
                                        ]) +
                                   graph.node_list[v_num].cons_cpu
                                   <=
                                   1)
        # 1st constraint
        # model.balance_mem_cons = ConstraintList()
        # for v in model.V:
        #     graph.name_to_num_node(v)
        #     # for v_ in range(len(graph.node_list)):
        #     #     if v == graph.node_list[v_].name:
        #     #         v_num = v_
        #     #         break
        #     model.balance_mem_cons.add(sum([model.a[v, i] *
        #                                 model.mf[i] *
        #                                 chain.tra /
        #                                 graph.node_list[v_num].cap_mem
        #                                 for i in model.nc
        #                                 ]) +
        #                            graph.node_list[v_num].cons_mem
        #                            <=
        #                            model.t)
        model.cap_mem_cons = ConstraintList()
        for v in model.V:
            graph.name_to_num_node(v)
            # for v_ in range(len(graph.node_list)):
            #     if v == graph.node_list[v_].name:
            #         v_num = v_
            #         break
            model.cap_mem_cons.add(sum([model.a[v, i] *
                                            model.mf[i] *
                                            chain.tra /
                                            graph.node_list[v_num].cap_mem
                                            for i in model.nc
                                            ]) +
                                       graph.node_list[v_num].cons_mem
                                       <=
                                       1)

        model.satisfy_req_2_cons = ConstraintList()
        for i in model.nc:
            model.satisfy_req_2_cons.add(sum([
                model.a[v, i]
                for v in model.V
            ])
                                         ==
                                         1
                                         )
        model.seq_cons = ConstraintList()
        for v_num, v in enumerate(model.V):
            for i in model.nc:
                if v_num != 0:
                    model.seq_cons.add(sum([
                    model.a[v_1, i_1] 
                    for v_1 in model.V[: v_num]
                    for i_1 in range(i + 1, len(chain.fun))
                                ])
                                <=
                                M * (1 - model.a[v, i])
                                )
        # "cplex", executable="/opt/ibm/ILOG/CPLEX_Studio_Community128/cplex/bin/x86-64_linux/cplex"
        opt = SolverFactory("cplex", executable="/opt/ibm/ILOG/CPLEX_Studio128/cplex/bin/x86-64_linux/cplex")
        # opt.options["threads"] = 2
        results = opt.solve(model)
        # model.seq_cons.pprint()
        # model.a.pprint()
        mem = 0
        cpu = 0
        node_cpu_cap = []
        node_mem_cap = []
        # model.a.pprint()
        # model.seq_cons.pprint()
        # for v in range(len(graph.node_list)):
            # print(graph.node_list[v].fun)
        for v in model.V:
            v_num = graph.name_to_num_node(v)
            for i in model.nc:
                if value(model.a[v, i]):
                    mem += value(model.a[v, i]) * model.mf[i] * chain.tra
                    cpu += value(model.a[v, i]) * model.nf[i] * chain.tra
                    # graph.function_placement(v_num, chain.name, chain.fun[i])
            mem = mem / graph.node_list[v_num].cap_mem
            cpu = cpu / graph.node_list[v_num].cap_cpu
            graph.node_list[v_num].cons_cpu += cpu
            graph.node_list[v_num].cons_mem += mem
            node_mem_cap.append(mem)
            node_cpu_cap.append(cpu)
            cpu = 0
            mem = 0
        # print(node_cpu_cap, node_mem_cap)
        nodes_cap = [graph.node_list[i].cons_cpu for i in range(len(graph.node_list))]
        # print(nodes_cap)
        # for n in range(len(path)):
        #     for m in range(len(graph.node_list)):
        #         if graph.node_list[m].name == path[n]:
        #
        #             for f in chain.fun[f_num:]:
        #                 if (function[f] / graph.node_list[m].cap) <= (nodes_cap - node_cap_list[n]) and nodes_cap - node_cap_list[n] >= 0:
        #                     graph.function_palcement(path(n), chain.name, f)
        #                     f_num += 1
        #                     break


