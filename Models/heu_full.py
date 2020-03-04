from coopr.pyomo import *
import  time
import InputConstants



class heu_full_model:
    def __init__(self):
        self.input_cons = InputConstants.Inputs()
    def run(self, graph, chains, function, alpha, user_num, batch_size, k, tune_param): 
        start_time = time.time()
        node_cpu_cap = []
        node_mem_cap = []
        batch_chain = []
        links_num = 0
        for c in chains.chains_list:
            for u in c.users:
                batch_chain.append([c, u, c.cpu_usage * c.tra, c.tra])
        batch_chain.sort(key=lambda x: x[2], reverse=True)
        batch_chain.sort(key=lambda x: x[3], reverse=True)
        for chain, u, _, _ in batch_chain:
            k_path = graph.k_path(u[0], u[1], k)
            path_num, link_num= self.__path_selection(graph, k_path, function, chain, alpha)
            links_num += link_num
            self.__node_selection(graph, chain, k_path[path_num], function, tune_param)
        for v in range(graph.nodes_num()):
            node_cpu_cap.append(graph.node_list[v].cons_cpu * 100)
            node_mem_cap.append(graph.node_list[v].cons_mem * 100)
        link_cap = []
        for l in range(len(graph.link_list)):
            link_cap.append(graph.link_list[l].cons * 100)
        end_time = time.time()
        print('heuristic full:', sum(node_cpu_cap))
        return max(node_cpu_cap), sum(node_cpu_cap)/len(node_cpu_cap), max(link_cap),\
        sum(node_cpu_cap)/len(node_cpu_cap), end_time - start_time, links_num
    def __path_selection(self, graph, k_path, function, c, alpha):
        path_cost =[]
        link_cap_list = []
        cpu_cap = []
        link_cons_list = []
        cpu = []
        tmp = []
        len_paths = 0
        for k in k_path:
            for n in range(len(k) - 1):
                l = graph.name_to_num_link((k[n], k[n + 1]))
                link_cons_list.append(graph.link_list[l].cons)
                link_cap_list.append(graph.link_list[l].ban)
            link_cons_avg = sum(link_cons_list) / (len(k) - 1)
            link_cap_avg = sum(link_cap_list) / (len(k) - 1)
            link_cons_max = max(link_cons_list)
            link_cons_list = []
            cpu_cons = []
            for n in k:
                m = graph.name_to_num_node(n)
                cpu_cons.append(graph.node_list[m].cons_cpu) 
                cpu_cap.append(graph.node_list[m].cap_cpu)
            cpu_avg = sum(cpu_cons) / len(k)
            # cpu_avg = cpu_avg 
            cpu_max = max(cpu_cons)
            path_cost.append(((1 - alpha) * ( link_cons_avg + link_cons_max ) + alpha * (cpu_max + cpu_avg ), len(k)))
            # path_cost.append(((1 - alpha) * ( link_cons_max ) + alpha * (cpu_max + cpu_avg ), len(k)))
            
            # path_cost.append(((link_cons_avg + link_cons_max), len(k)))

            # path_cost.append((link_cons_max, len(k)))
            cpu_cons = []
            cpu_cap = []
            link_cap_list = []
        # path_cost.sort(key=lambda x: x[1])
        path_cost = [p[0] for p in path_cost]
        idx = path_cost.index(min(path_cost))
        for n in range(len(k_path[idx])-1):
            l = graph.name_to_num_link((k_path[idx][n], k_path[idx][n+1]))
            graph.link_list[l].cons += c.tra / graph.link_list[l].ban
        return idx, len(k_path[idx])-1

    def __node_selection(self, graph, c, path, functions, tune_param):
        # print('*'*40)
        delta = c.cpu_usage * c.tra 
        # / sum([graph.node_list[graph.name_to_num_node(v)].cap_cpu for v in path])
        req_cap = c.cpu_usage * c.tra / sum([graph.node_list[graph.name_to_num_node(v)].cap_cpu for v in path])
        path_cons = [graph.node_list[graph.name_to_num_node(v)].cons_cpu for v in path]
        # print('path_cons', path_cons)
        # print('f', len(c.fun))
        theta_star = max(path_cons)
        res_cap = 0
        if theta_star == 0:
            req_cap /= len(path)
            i = 0
            v = 0
            if len(path) >= len(c.fun):
                for i in range(len(c.fun)):
                    graph.node_list[graph.name_to_num_node(path[v])].cons_cpu += functions.cpu_usage(c.fun[i]) * c.tra / graph.node_list[graph.name_to_num_node(path[v])].cap_cpu
                    graph.node_list[graph.name_to_num_node(path[v])].cons_mem += functions.mem_usage(c.fun[i]) * c.tra / graph.node_list[graph.name_to_num_node(path[v])].cap_mem
                    # print('i and v', i, v)
                    v += 1
            else:
                i = 0
                for v in path:
                    if i==len(c.fun):
                        break
                    while graph.node_list[graph.name_to_num_node(v)].cons_cpu+((functions.cpu_usage(c.fun[i]) * c.tra)/graph.node_list[graph.name_to_num_node(v)].cap_cpu)<=req_cap+tune_param:
                        graph.node_list[graph.name_to_num_node(v)].cons_cpu += functions.cpu_usage(c.fun[i]) * c.tra / graph.node_list[graph.name_to_num_node(v)].cap_cpu
                        graph.node_list[graph.name_to_num_node(v)].cons_mem += functions.mem_usage(c.fun[i]) * c.tra / graph.node_list[graph.name_to_num_node(v)].cap_mem
                        i += 1
                        if i==len(c.fun):
                            break
                if i < len(c.fun):
                    for j in range(i, len(c.fun)):
                        graph.node_list[graph.name_to_num_node(v)].cons_cpu += functions.cpu_usage(c.fun[j]) * c.tra / graph.node_list[graph.name_to_num_node(v)].cap_cpu
                        graph.node_list[graph.name_to_num_node(v)].cons_mem += functions.mem_usage(c.fun[i]) * c.tra / graph.node_list[graph.name_to_num_node(v)].cap_mem
                    i = len(c.fun)  

        else:
            i = 0
            theta_star_mines = 0
            total_cap = 0
            for v in path:
                res_cap += (theta_star - graph.node_list[graph.name_to_num_node(v)].cons_cpu)*graph.node_list[graph.name_to_num_node(v)].cap_cpu

            if delta<=res_cap:
                theta_star_mines = theta_star
            else:
                theta_star_mines += delta
                for v in path:
                    theta_star_mines += graph.node_list[graph.name_to_num_node(v)].cons_cpu*graph.node_list[graph.name_to_num_node(v)].cap_cpu
                    total_cap += graph.node_list[graph.name_to_num_node(v)].cap_cpu
                theta_star_mines /= total_cap
            for v in path:
                if i==len(c.fun):
                    break
                while graph.node_list[graph.name_to_num_node(v)].cons_cpu+((functions.cpu_usage(c.fun[i]) * c.tra)/graph.node_list[graph.name_to_num_node(v)].cap_cpu)<=theta_star_mines+tune_param:
                    graph.node_list[graph.name_to_num_node(v)].cons_cpu += functions.cpu_usage(c.fun[i]) * c.tra / graph.node_list[graph.name_to_num_node(v)].cap_cpu
                    graph.node_list[graph.name_to_num_node(v)].cons_mem += functions.mem_usage(c.fun[i]) * c.tra / graph.node_list[graph.name_to_num_node(v)].cap_mem
                    i += 1
                    if i==len(c.fun):
                        break
            if i < len(c.fun):
                for j in range(i, len(c.fun)):
                    graph.node_list[graph.name_to_num_node(v)].cons_cpu += functions.cpu_usage(c.fun[j]) * c.tra / graph.node_list[graph.name_to_num_node(v)].cap_cpu
                    graph.node_list[graph.name_to_num_node(v)].cons_mem += functions.mem_usage(c.fun[i]) * c.tra / graph.node_list[graph.name_to_num_node(v)].cap_mem
                i = len(c.fun)  
            
        



# class heu_full_model:
#     def __init__(self):
#         self.input_cons = InputConstants.Inputs()
#     def run(self, graph, chains, function, alpha, user_num, batch_size, k, tune_param): 
#         start_time = time.time()
#         node_cpu_cap = []
#         node_mem_cap = []
#         batch_chain = []
#         links_num = 0
#         for c in chains.chains_list:
#             for u in c.users:
#                 batch_chain.append([c, u, c.cpu_usage * c.tra, c.tra])
#         batch_chain.sort(key=lambda x: x[2], reverse=True)
#         batch_chain.sort(key=lambda x: x[3], reverse=True)
#         for chain, u, _, _ in batch_chain:
#             k_path = graph.k_path(u[0], u[1], k)
#             path_num, link_num= self.__path_selection(graph, k_path, function, chain, alpha)
#             links_num += link_num
#             self.__node_selection(graph, chain, k_path[path_num], function, tune_param)
#         for v in range(graph.nodes_num()):
#             node_cpu_cap.append(graph.node_list[v].cons_cpu * 100)
#             node_mem_cap.append(graph.node_list[v].cons_mem * 100)
#         link_cap = []
#         for l in range(len(graph.link_list)):
#             link_cap.append(graph.link_list[l].cons * 100)
#         end_time = time.time()
#         print('heuristic full:', sum(node_cpu_cap))
#         return max(node_cpu_cap), sum(node_cpu_cap)/len(node_cpu_cap), max(link_cap),\
#         sum(node_cpu_cap)/len(node_cpu_cap), end_time - start_time, links_num
        
#     def __path_selection(self, graph, k_path, function, c, alpha):
#         path_cost =[]
#         link_cap_list = []
#         cpu_cap = []
#         link_cons_list = []
#         cpu = []
#         tmp = []
#         len_paths = 0
#         for k in k_path:
#             for n in range(len(k) - 1):
#                 l = graph.name_to_num_link((k[n], k[n + 1]))
#                 link_cons_list.append(graph.link_list[l].cons)
#                 link_cap_list.append(graph.link_list[l].ban)
#             link_cons_avg = sum(link_cons_list) / (len(k) - 1)
#             link_cap_avg = sum(link_cap_list) / (len(k) - 1)
#             link_cons_max = max(link_cons_list)
#             link_cons_list = []
#             cpu_cons = []
#             for n in k:
#                 m = graph.name_to_num_node(n)
#                 cpu_cons.append(graph.node_list[m].cons_cpu) 
#                 cpu_cap.append(graph.node_list[m].cap_cpu)
#             cpu_avg = sum(cpu_cons) / len(k)
#             cpu_avg = cpu_avg 
#             cpu_max = max(cpu_cons)
#             # path_cost.append(((1 - alpha) * ( link_cons_avg + link_cons_max ) + alpha * (cpu_max+ cpu_avg ), len(k)))
#             path_cost.append((link_cons_max, len(k)))
#             cpu_cons = []
#             cpu_cap = []
#             link_cap_list = []
#         path_cost.sort(key=lambda x: x[1])
#         path_cost = [p[0] for p in path_cost]
#         idx = path_cost.index(min(path_cost))
#         for n in range(len(k_path[idx])-1):
#             l = graph.name_to_num_link((k_path[idx][n], k_path[idx][n+1]))
#             graph.link_list[l].cons += c.tra / graph.link_list[l].ban
#         return idx, len(k_path[idx])-1

#     def __node_selection(self, graph, c, path, functions, tune_param):
#         # print('*'*40)
#         req_cap = c.cpu_usage * c.tra / sum([graph.node_list[graph.name_to_num_node(v)].cap_cpu for v in path])
#         path_cons = [graph.node_list[graph.name_to_num_node(v)].cons_cpu for v in path]
#         # print('path_cons', path_cons)
#         # print('f', len(c.fun))
#         max_cap = max(path_cons)
#         res_cap = 0
#         if max_cap == 0:
#             req_cap /= len(path)
#             i = 0
#             v = 0
#             if len(path) >= len(c.fun):
#                 for i in range(len(c.fun)):
#                     graph.node_list[graph.name_to_num_node(path[v])].cons_cpu += functions.cpu_usage(c.fun[i]) * c.tra / graph.node_list[graph.name_to_num_node(path[v])].cap_cpu
#                     graph.node_list[graph.name_to_num_node(path[v])].cons_mem += functions.mem_usage(c.fun[i]) * c.tra / graph.node_list[graph.name_to_num_node(path[v])].cap_mem
#                     # print('i and v', i, v)
#                     v += 1
#             else:
#                 tmp = req_cap
#                 while( i < len(c.fun)):
#                     # print('divi_cap', tmp)
#                     # print('cap_function', functions.cpu_usage(c.fun[i]) * c.tra/graph.node_list[graph.name_to_num_node(path[v])].cap_cpu)
#                     if tmp + tune_param >=  functions.cpu_usage(c.fun[i]) * c.tra/graph.node_list[graph.name_to_num_node(path[v])].cap_cpu:
#                         graph.node_list[graph.name_to_num_node(path[v])].cons_cpu += functions.cpu_usage(c.fun[i]) * c.tra / graph.node_list[graph.name_to_num_node(path[v])].cap_cpu
#                         graph.node_list[graph.name_to_num_node(path[v])].cons_mem += functions.mem_usage(c.fun[i]) * c.tra / graph.node_list[graph.name_to_num_node(path[v])].cap_mem
#                         tmp -= functions.cpu_usage(c.fun[i]) * c.tra / graph.node_list[graph.name_to_num_node(path[v])].cap_cpu
#                         # print('i and v', i, v)
#                         i += 1
#                     elif v < len(path) - 1:
#                         v += 1
#                         tmp = req_cap
#                     elif i < len(c.fun):
#                         for j in range(i, len(c.fun)):
#                             graph.node_list[graph.name_to_num_node(path[v])].cons_cpu += functions.cpu_usage(c.fun[j]) * c.tra / graph.node_list[graph.name_to_num_node(path[v])].cap_cpu
#                             graph.node_list[graph.name_to_num_node(path[v])].cons_mem += functions.mem_usage(c.fun[i]) * c.tra / graph.node_list[graph.name_to_num_node(path[v])].cap_mem
#                             # print('i and v', j, v)
#                         i = len(c.fun)
#         else:
#             for v in path:
#                 res_cap += max_cap - graph.node_list[graph.name_to_num_node(v)].cons_cpu
#             ex_cap = (req_cap - res_cap) / len(path)
#             # print('res_cap', res_cap)
#             # print('req_cap', req_cap)
            
#             if ex_cap <0:
#                 ex_cap=0
#             i = 0
#             v = 0
#             tmp = ex_cap

#             # print('ex_cap', ex_cap)
#             while( i < len(c.fun)):
#                 # if max(path_cons)-min(path_cons)<0.1:

#                 if tmp+(max_cap - graph.node_list[graph.name_to_num_node(path[v])].cons_cpu)+tune_param >= 
#                 (functions.cpu_usage(c.fun[i]) * c.tra)/graph.node_list[graph.name_to_num_node(path[v])].cap_cpu:
#                     graph.node_list[graph.name_to_num_node(path[v])].cons_cpu += functions.cpu_usage(c.fun[i]) * c.tra / graph.node_list[graph.name_to_num_node(path[v])].cap_cpu
#                     graph.node_list[graph.name_to_num_node(path[v])].cons_mem += functions.mem_usage(c.fun[i]) * c.tra / graph.node_list[graph.name_to_num_node(path[v])].cap_mem
#                     # print('i and v', i, v)
#                     # print('all', tmp+(max_cap - graph.node_list[graph.name_to_num_node(path[v])].cons_cpu))
#                     i += 1

#              #   elif tmp+(max_cap - graph.node_list[graph.name_to_num_node(path[v])].cons_cpu) >=  functions.cpu_usage(c.fun[i]) * c.tra * tune_param:
#               #      graph.node_list[graph.name_to_num_node(path[v])].cons_cpu += functions.cpu_usage(c.fun[i]) * c.tra / graph.node_list[v].cap_cpu
#                #     graph.node_list[graph.name_to_num_node(path[v])].cons_mem += functions.mem_usage(c.fun[i]) * c.tra / graph.node_list[v].cap_mem
#                    # tmp -= functions.cpu_usage(c.fun[i]) * c.tra
#                 #    i += 1
#                 elif v < len(path) - 1:
#                     v += 1
#                     tmp = ex_cap
#                 elif i < len(c.fun):
#                     for j in range(i, len(c.fun)):
#                         graph.node_list[graph.name_to_num_node(path[v])].cons_cpu += functions.cpu_usage(c.fun[j]) * c.tra / graph.node_list[graph.name_to_num_node(path[v])].cap_cpu
#                         graph.node_list[graph.name_to_num_node(path[v])].cons_mem += functions.mem_usage(c.fun[i]) * c.tra / graph.node_list[graph.name_to_num_node(path[v])].cap_mem
#                         # print('i and v', j, v)
#                     i = len(c.fun)   
#             # print('path cons last:', [graph.node_list[graph.name_to_num_node(v)].cons_cpu for v in path])                    
