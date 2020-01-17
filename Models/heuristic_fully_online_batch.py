from coopr.pyomo import *
import  time
# import matplotlib.pyplot as plt
import InputConstants
# from PaperFunctions import Graph, Chains
class heuristic_fully_batch_model:
    def __init__(self, k, alpha, user_num, batch_size):
        self.input_cons = InputConstants.Inputs()
        self.k = k
        self.alpha = alpha
        self.user_num = user_num
        self.batch_size = batch_size
    def run(self, graph, chains, function): 
        start_time = time.time()
        # graph.link_list[0].cap = 0
        cpu = 0
        mem = 0
        node_cpu_cap = []
        node_mem_cap = []
        chains_usage = []
        # for c in chains.chains_list:
        #     for u in c.users:
        #         chains_usage.append([c, u, c.cpu_usage * c.tra])
        # chains_usage.sort(key=lambda x: x[2])
        # # for c in chains.chains_list:
            # for u in c.users:
        batch_chain = []
        cnt = 0
        batch_num = 0
        for c in chains.chains_list:
            for u in c.users:
                batch_chain.append([c, u, c.cpu_usage * c.tra, c.tra])
                cnt += 1
                if cnt == self.batch_size or cnt == self.user_num or (batch_num == self.user_num // self.batch_size and cnt == self.user_num % self.batch_size):
                    batch_num += 1
                    batch_chain.sort(key=lambda x: x[3], reverse=True)
                    batch_chain.sort(key=lambda x: x[2], reverse=True)
                    # for c in chains.chains_list:
                        # for u in c.users:
                    
                    for chain, u, _, _ in batch_chain:
                        # print(u)
                                # for c, u, _ in chains_usage:
                        k_path = graph.k_path(u[0], u[1], self.k)
                        # print(k_path)
                        # print("user {} wanna get service".format(u))
                        path_num = self.__path_selection(graph, k_path, function, chain)
                        # print("ok")
                        # print("path {} and is {} ".format(path_num, k_path[path_num]))
                        # print(k_path[path_num])
                        self.__node_selection(graph, chain, k_path[path_num], function)
                        # print("path num:", path_num)
                        # print("-------------------------------------------------")
                    # print("**/***********")

                    cnt = 0
                    batch_chain = []
        for v in range(graph.nodes_num()):
            node_cpu_cap.append(graph.node_list[v].cons_cpu * 100 / graph.node_list[v].cap_cpu)
            node_mem_cap.append(graph.node_list[v].cons_mem * 100 / graph.node_list[v].cap_cpu)
        
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
        print('heuristic fully batch', sum(node_cpu_cap))
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
            path_cost.append((1 - self.alpha) * ( link_cap_avg + link_cap_max )/2 + 
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

    def __node_selection(self, graph, c, path, functions):
        req_cap = c.cpu_usage * c.tra
        path_cap = [graph.node_list[graph.name_to_num_node(v)].cons_cpu for v in path]
        max_cap = max(path_cap)
        res_cap = 0
        # print(path)
        if max_cap == 0:
            # print('11111111111111111111111')
            divi_cap = (c.cpu_usage * c.tra) // len(path)
            i = 0
            v = 0
            if len(path) >= len(c.fun):
                for i in range(len(c.fun)):
                    graph.node_list[graph.name_to_num_node(path[v])].cons_cpu += functions.cpu_usage(c.fun[i]) * c.tra
                    # print('f {} is placed in node {}'.format(i, path[v]))
                    v += 1
            else:
                tmp = divi_cap
                while( i < len(c.fun)):
                    # print('fun {} and node {}'.format(i, v))
                    # print('max: {} and res: {} and cap: {} and tmp:{}'.format(max_cap, graph.node_list[graph.name_to_num_node(path[v])].cons_cpu, functions.cpu_usage(c.fun[i]) * c.tra, tmp))

                    if tmp >=  functions.cpu_usage(c.fun[i]) * c.tra * 0.5:
                        graph.node_list[graph.name_to_num_node(path[v])].cons_cpu += functions.cpu_usage(c.fun[i]) * c.tra
                        tmp -= functions.cpu_usage(c.fun[i]) * c.tra
                        # print('f {} is placed in node {}'.format(i, path[v]))
                        i += 1
                    elif v < len(path) - 1:
                        v += 1
                        tmp = divi_cap
                    elif i < len(c.fun):
                        for j in range(i, len(c.fun)):
                            graph.node_list[graph.name_to_num_node(path[v])].cons_cpu += functions.cpu_usage(c.fun[j]) * c.tra
                            # print('f {} is placed in node {}'.format(j, path[v]))
                            # print('max: {} and res: {} and cap: {} and tmp:{}'.format(max_cap, graph.node_list[graph.name_to_num_node(path[v])].cons_cpu, functions.cpu_usage(c.fun[i]) * c.tra, tmp))
                        i = len(c.fun)
        else:
            for v in path:
                res_cap += max_cap - graph.node_list[graph.name_to_num_node(v)].cons_cpu
            # print('2222f2222222222222')
            # max_fun = max([functions.cpu_usage(f) * c.tra for f in c.fun])
            # print('chain_req: {}, res_cap: {}'.format(req_cap, res_cap))
            ex_cap = (req_cap - res_cap) / len(path)
            # ex_cap = ((ex_cap // max_fun) + 1) * max_fun
            i = 0
            v = 0
            tmp = ex_cap
            while( i < len(c.fun)):
                # print('fun {} and node {}'.format(i, v))
                # print('max: {} and res: {} and cap: {} and tmp:{}'.format(max_cap, graph.node_list[graph.name_to_num_node(path[v])].cons_cpu, functions.cpu_usage(c.fun[i]) * c.tra, tmp))

                if (max_cap - graph.node_list[graph.name_to_num_node(path[v])].cons_cpu) >= (functions.cpu_usage(c.fun[i]) * c.tra * 0.5):
                    graph.node_list[graph.name_to_num_node(path[v])].cons_cpu += functions.cpu_usage(c.fun[i]) * c.tra
                    # print('f {} is placed in node {}'.format(i, path[v]))
                    i += 1
                elif tmp >=  functions.cpu_usage(c.fun[i]) * c.tra * 0.5:
                    graph.node_list[graph.name_to_num_node(path[v])].cons_cpu += functions.cpu_usage(c.fun[i]) * c.tra
                    tmp -= functions.cpu_usage(c.fun[i]) * c.tra
                    # print('f {} is placed in node {}'.format(i, path[v]))
                    i += 1
                elif v < len(path) - 1:
                    v += 1
                    tmp = ex_cap
                elif i < len(c.fun):
                    for j in range(i, len(c.fun)):
                        graph.node_list[graph.name_to_num_node(path[v])].cons_cpu += functions.cpu_usage(c.fun[j]) * c.tra
                        # print('f {} is placed in node {}'.format(j, path[v]))
                        # print('max: {} and res: {} and cap: {} and tmp:{}'.format(max_cap, graph.node_list[graph.name_to_num_node(path[v])].cons_cpu, functions.cpu_usage(c.fun[i]) * c.tra, tmp))
                    i = len(c.fun)
        # print([graph.node_list[v].cons_cpu for v in range(graph.nodes_num())])
                        