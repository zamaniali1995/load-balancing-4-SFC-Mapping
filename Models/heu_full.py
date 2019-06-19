from coopr.pyomo import *
import  time
import InputConstants

class heu_full_model:
    def __init__(self):
        self.input_cons = InputConstants.Inputs()
    def run(self, graph, chains, function, alpha, user_num, batch_size, k): 
        start_time = time.time()
        node_cpu_cap = []
        node_mem_cap = []
        batch_chain = []
        for c in chains.chains_list:
            for u in c.users:
                batch_chain.append([c, u, c.cpu_usage * c.tra, c.tra])
        batch_chain.sort(key=lambda x: x[2], reverse=True)
        batch_chain.sort(key=lambda x: x[3], reverse=True)
        for chain, u, _, _ in batch_chain:
            k_path = graph.k_path(u[0], u[1], k)
            path_num = self.__path_selection(graph, k_path, function, chain, alpha)
            self.__node_selection(graph, chain, k_path[path_num], function)
        for v in range(graph.nodes_num()):
            node_cpu_cap.append(graph.node_list[v].cons_cpu * 100 / graph.node_list[v].cap_cpu)
            node_mem_cap.append(graph.node_list[v].cons_mem * 100 / graph.node_list[v].cap_mem)
        link_cap = []
        for l in range(len(graph.link_list)):
            link_cap.append(graph.link_list[l].cons / graph.link_list[l].ban * 100)
        end_time = time.time()
        print('heuristic full:', sum(node_cpu_cap))
        return max(node_cpu_cap), sum(node_cpu_cap)/len(node_cpu_cap), max(link_cap),\
        sum(node_cpu_cap)/len(node_cpu_cap), end_time - start_time
        
    def __path_selection(self, graph, k_path, function, c, alpha):
        path_cost =[]
        link_cap_list = []
        cpu = []
        tmp = []
        len_paths = 0
        for k in k_path:
            len_paths += len(k)
            tmp.append(len(k))
        min_len = min(tmp)
        for k in k_path:
            for n in range(len(k) - 1):
                l = graph.name_to_num_link((k[n], k[n + 1]))
                link_cap_list.append(graph.link_list[l].cons / graph.link_list[l].ban)
            link_cap_avg = sum(link_cap_list) / (len(k) - 1)
            link_cap_max = max(link_cap_list)
            cpu = []
            for n in k:
                m = graph.name_to_num_node(n)
                cpu.append(graph.node_list[m].cons_cpu) 
            cpu_avg = sum(cpu) / len(k)
            cpu_max = max(cpu) 
            path_cost.append((1 - alpha) * ( link_cap_avg + link_cap_max +
             min_len/len(k))/3 + alpha * (cpu_max + cpu_avg)/2)
            cpu = 0
        idx = path_cost.index(min(path_cost))
        for n in range(len(k_path[idx])-1):
            l = graph.name_to_num_link((k_path[idx][n], k_path[idx][n+1]))
            graph.link_list[l].cons += c.tra
        return idx

    def __node_selection(self, graph, c, path, functions):
        req_cap = c.cpu_usage * c.tra
        path_cap = [graph.node_list[graph.name_to_num_node(v)].cons_cpu for v in path]
        max_cap = max(path_cap)
        res_cap = 0
        if max_cap == 0:
            divi_cap = (c.cpu_usage * c.tra) // len(path)
            i = 0
            v = 0
            if len(path) >= len(c.fun):
                for i in range(len(c.fun)):
                    graph.node_list[graph.name_to_num_node(path[v])].cons_cpu += functions.cpu_usage(c.fun[i]) * c.tra
                    graph.node_list[graph.name_to_num_node(path[v])].cons_mem += functions.mem_usage(c.fun[i]) * c.tra
                    v += 1
            else:
                tmp = divi_cap
                while( i < len(c.fun)):
                    if tmp >=  functions.cpu_usage(c.fun[i]) * c.tra * 0.5:
                        graph.node_list[graph.name_to_num_node(path[v])].cons_cpu += functions.cpu_usage(c.fun[i]) * c.tra
                        graph.node_list[graph.name_to_num_node(path[v])].cons_mem += functions.mem_usage(c.fun[i]) * c.tra
                        tmp -= functions.cpu_usage(c.fun[i]) * c.tra
                        i += 1
                    elif v < len(path) - 1:
                        v += 1
                        tmp = divi_cap
                    elif i < len(c.fun):
                        for j in range(i, len(c.fun)):
                            graph.node_list[graph.name_to_num_node(path[v])].cons_cpu += functions.cpu_usage(c.fun[j]) * c.tra
                            graph.node_list[graph.name_to_num_node(path[v])].cons_mem += functions.mem_usage(c.fun[i]) * c.tra
                        i = len(c.fun)
        else:
            for v in path:
                res_cap += max_cap - graph.node_list[graph.name_to_num_node(v)].cons_cpu
            ex_cap = (req_cap - res_cap) / len(path)
            i = 0
            v = 0
            tmp = ex_cap
            while( i < len(c.fun)):
                if (max_cap - graph.node_list[graph.name_to_num_node(path[v])].cons_cpu) >= (functions.cpu_usage(c.fun[i]) * c.tra * 0.5):
                    graph.node_list[graph.name_to_num_node(path[v])].cons_cpu += functions.cpu_usage(c.fun[i]) * c.tra
                    graph.node_list[graph.name_to_num_node(path[v])].cons_mem += functions.mem_usage(c.fun[i]) * c.tra
                    i += 1
                elif tmp >=  functions.cpu_usage(c.fun[i]) * c.tra * 0.5:
                    graph.node_list[graph.name_to_num_node(path[v])].cons_cpu += functions.cpu_usage(c.fun[i]) * c.tra
                    graph.node_list[graph.name_to_num_node(path[v])].cons_mem += functions.mem_usage(c.fun[i]) * c.tra    
                    tmp -= functions.cpu_usage(c.fun[i]) * c.tra
                    i += 1
                elif v < len(path) - 1:
                    v += 1
                    tmp = ex_cap
                elif i < len(c.fun):
                    for j in range(i, len(c.fun)):
                        graph.node_list[graph.name_to_num_node(path[v])].cons_cpu += functions.cpu_usage(c.fun[j]) * c.tra
                        graph.node_list[graph.name_to_num_node(path[v])].cons_mem += functions.mem_usage(c.fun[i]) * c.tra                   
                    i = len(c.fun)                       
