from coopr.pyomo import *
import  time
import InputConstants

class benchmark_second:
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
            link_num = self.__node_selection(graph, chain, k_path, function, tune_param)
            links_num += link_num
        for v in range(graph.nodes_num()):
            node_cpu_cap.append(graph.node_list[v].cons_cpu * 100)
            node_mem_cap.append(graph.node_list[v].cons_mem * 100)
        link_cap = []      
        for l in range(len(graph.link_list)):
            link_cap.append(graph.link_list[l].cons * 100)
        end_time = time.time()
        print('second benchmark:', sum(node_cpu_cap))
        return max(node_cpu_cap), sum(node_cpu_cap)/len(node_cpu_cap), max(link_cap),\
        sum(node_cpu_cap)/len(node_cpu_cap), end_time - start_time, links_num

    def __node_selection(self, graph, c, k_path, functions, tune_param):
        placements_list = []
        for path in k_path:
            placements = []
            v = 0
            i = 0
            nodes_cons = [graph.node_list[graph.name_to_num_node(v)].cons_cpu for v in path]
            while( i < len(c.fun)):
                if i != 0:
                    p = placements[-1]
                    nodes_cons[p[0]] += (functions.cpu_usage(c.fun[p[1]]) * c.tra / graph.node_list[graph.name_to_num_node(path[p[0]])].cap_cpu)
                v = nodes_cons.index(min(nodes_cons[v:])) 
                if len(path)==v+1:
                    for j in range(i, len(c.fun)):
                        placements.append([v, j])
                        nodes_cons[v] += (functions.cpu_usage(c.fun[j]) * c.tra / graph.node_list[graph.name_to_num_node(path[v])].cap_cpu)
                    i = len(c.fun)
                else:
                    placements.append([v, i])
                    i += 1
            placements_list.append((placements, nodes_cons))
        max_in_each_path = []
        for p in placements_list:
            max_in_each_path.append(max(p[1]))
        min_path = min(max_in_each_path)
        link_cons_max = []
        link_cons_list = []
        for m in range(len(max_in_each_path)):
            if max_in_each_path[m] == min_path:
                k = k_path[m]
                link_cons_list = []
                for n in range(len(k) - 1):
                    l = graph.name_to_num_link((k[n], k[n + 1]))
                    link_cons_list.append(graph.link_list[l].cons)
                link_cons_max.append([m, max(link_cons_list)])
        idx = min(link_cons_max, key=lambda x: x[1])[0]
        placements = placements_list[idx]
        for p in placements[0]:
            v = p[0]
            i = p[1]
            graph.node_list[graph.name_to_num_node(k_path[idx][v])].cons_cpu += functions.cpu_usage(c.fun[i]) * c.tra / graph.node_list[graph.name_to_num_node(k_path[idx][v])].cap_cpu
            graph.node_list[graph.name_to_num_node(k_path[idx][v])].cons_mem += functions.mem_usage(c.fun[i]) * c.tra / graph.node_list[graph.name_to_num_node(k_path[idx][v])].cap_mem
        for n in range(len(k_path[idx])-1):
            l = graph.name_to_num_link((k_path[idx][n], k_path[idx][n+1]))
            graph.link_list[l].cons += c.tra / graph.link_list[l].ban
        return len(k_path[idx])

                    
