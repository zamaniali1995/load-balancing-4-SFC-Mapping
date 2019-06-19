from coopr.pyomo import *
import  time
import InputConstants
class heuristic_online_batch_model:
    def __init__(self):
        self.input_cons = InputConstants.Inputs()

    def run(self, graph, chains, functions, k, alpha, user_num, batch_size): 
        start_time = time.time()
        link_cap = []
        node_cpu_cap = []
        node_mem_cap = []
        chain_sorted = []
        for c in chains.chains_list:
            for u in c.users:
                chain_sorted.append([c, u, c.cpu_usage * c.tra, c.tra])
        chain_sorted.sort(key=lambda x: x[3], reverse=True)
        chain_sorted.sort(key=lambda x: x[2], reverse=True)
        for chain, u, _, _ in chain_sorted:
            k_path = graph.k_path(u[0], u[1], k)
            cap_links = []
            k_path_ver = []
            for _k in k_path:
                for n in range(len(_k)-1):
                    l = graph.name_to_num_link((_k[n], _k[n+1]))
                    cap_links.append(graph.link_list[l].cons)
                if max(cap_links) + chain.tra <= 100:
                    k_path_ver.append(_k)
                cap_links = []
            if k_path_ver != []:
                path_num = self.__path_selection(graph, k_path_ver, functions, chain, alpha)
                self.__node_selection(graph, chain, k_path_ver[path_num], functions)
            else:
                print('problem is not feasible')
                break
        for v in range(graph.nodes_num()):
            node_cpu_cap.append(graph.node_list[v].cons_cpu * 100)
            node_mem_cap.append(graph.node_list[v].cons_mem * 100)
        
        for l in range(len(graph.link_list)):
            link_cap.append(graph.link_list[l].cons * 100)

        end_time = time.time()
        print('heuristic online batch', sum(node_cpu_cap))
        return [max(node_cpu_cap), max(link_cap), end_time - start_time, max(node_mem_cap)]

    def __path_selection(self, graph, k_path, function, c, alpha):
        path_cost =[]
        link_cap_list = []
        cpu = []
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
                link_cap_list.append(graph.link_list[l].cons / graph.link_list[l].ban)
            link_cap_avg = sum(link_cap_list) / (len(k) - 1)
            link_cap_max = max(link_cap_list)
            cpu = []
            mem = []
            for n in k:
                m = graph.name_to_num_node(n)
                cpu.append(graph.node_list[m].cons_cpu) 
                mem.append(graph.node_list[m].cons_mem)
            cpu_avg = sum(cpu) / len(k)
            cpu_max = max(cpu) 

            path_cost.append((1 - alpha) * ( link_cap_avg + link_cap_max + min_len / len(k) * (1 / (c.cpu_usage) ))/3 + 
                                  alpha * (cpu_max + cpu_avg)/2)
                
            cpu = 0
            mem = 0
        idx = path_cost.index(min(path_cost))
        for n in range(len(k_path[idx])-1):
            l = graph.name_to_num_link((k_path[idx][n], k_path[idx][n+1]))
            graph.link_list[l].cons += c.tra / graph.link_list[l].ban
        return idx

    def __node_selection(self, graph, chain, path, functions):
        M = 10000

        ##########################################
        # Define concrete model
        ###########################################
        model = ConcreteModel()

        ###########################################
        # Sets
        ###########################################
        # Set of nodes: v
        model.V = path
        # Set of functions: F
        model.nc = range(len(chain.fun))
        # cpus usage of each function
        model.nf = {}
        for i in model.nc:
            model.nf[i] = functions.cpu_usage(chain.fun[i])
        # mem usage of each function
        model.mf = {}
        for i in model.nc:
            model.mf[i] = functions.mem_usage(chain.fun[i])
        
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
        # 2nd constraint:
        model.cap_cpu_cons = ConstraintList()
        for v in model.V:
            v_num = graph.name_to_num_node(v)
            model.cap_cpu_cons.add(sum([model.a[v, i] *
                                        model.nf[i] *
                                        chain.tra /
                                        graph.node_list[v_num].cap_cpu
                                        for i in model.nc
                                        ]) +
                                   graph.node_list[v_num].cons_cpu
                                   <=
                                   1)
        # 3rd constraint:
        model.cap_mem_cons = ConstraintList()
        for v in model.V:
            graph.name_to_num_node(v)
            model.cap_mem_cons.add(sum([model.a[v, i] *
                                            model.mf[i] *
                                            chain.tra /
                                            graph.node_list[v_num].cap_mem
                                            for i in model.nc
                                            ]) +
                                       graph.node_list[v_num].cons_mem
                                       <=
                                       1)
        # 4th constraint:
        model.satisfy_req_2_cons = ConstraintList()
        for i in model.nc:
            model.satisfy_req_2_cons.add(sum([
                model.a[v, i]
                for v in model.V
            ])
                                         ==
                                         1
                                         )
                                         
        # 5th constraint:                                 
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
        opt = SolverFactory("cplex", executable=self.input_cons.path_cplex)
        opt.options["threads"] = self.input_cons.threads_num
        results = opt.solve(model)
        for v in model.V:
            v_num = graph.name_to_num_node(v)
            for i in model.nc:
                graph.node_list[v_num].cons_cpu += value(model.a[v, i]) * model.nf[i] * chain.tra / graph.node_list[v_num].cap_cpu
                graph.node_list[v_num].cons_mem += value(model.a[v, i]) * model.mf[i] * chain.tra / graph.node_list[v_num].cap_mem
         