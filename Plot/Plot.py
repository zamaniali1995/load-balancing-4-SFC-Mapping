import sys
import numpy as np

sys.path.insert(0, './PaperFunctions')
sys.path.insert(1, './Given')
sys.path.insert(1, './Models')
sys.path.insert(1, './Plot')
from MILP import MILP_model
from MILP_online import MILP_online_model
from heuristic_offline import heuristic_offline_model
from heuristic_online import heuristic_online_model
from MILP_batch import MILP_batch_model
from heuristic_online_batch import heuristic_online_batch_model
from heu_full import heu_full_model
import matplotlib.pyplot as plt
from decimal import Decimal, ROUND_DOWN
import InputConstants


class Plot:
    def __init__(self):
        self.input_cons = InputConstants.Inputs()
        self.heu_online = heuristic_online_model()
        self.heu_online_batch = heuristic_online_batch_model()
        self.heu_offline = heuristic_offline_model()
        self.heu_full = heu_full_model()
        self.MILP_online = MILP_online_model()
        self.MILP_batch = MILP_batch_model()
        self.MILP = MILP_model()
            
        self.tune_param = self.input_cons.heu_full_tune_param
        self.run_num = self.input_cons.run_num

        self.cpu_heu_full_max = [[] for _ in range(len(self.tune_param))]
        self.cpu_heu_full_avg = [[] for _ in range(len(self.tune_param))]
        self.link_heu_full_max = [[] for _ in range(len(self.tune_param))]
        self.link_heu_full_avg = [[] for _ in range(len(self.tune_param))] 
        self.time_heu_full = [[] for _ in range(len(self.tune_param))]
            
        self.cpu_MILP_batch_max = []
        self.cpu_MILP_batch_avg = []
        self.link_MILP_batch_max = []
        self.link_MILP_batch_avg = []
        self.time_MILP_batch = []
            
        self.cpu_MILP_max = []
        self.cpu_MILP_avg = []
        self.link_MILP_max = []
        self.link_MILP_avg = []
        self.time_MILP = []

        self.cpu_heu_full_max_list = [[] for _ in range(len(self.tune_param))]
        self.cpu_heu_full_avg_list = [[] for _ in range(len(self.tune_param))]
        self.link_heu_full_max_list = [[] for _ in range(len(self.tune_param))]
        self.link_heu_full_avg_list = [[] for _ in range(len(self.tune_param))]
        self.time_heu_full_list = [[] for _ in range(len(self.tune_param))]

        self.cpu_MILP_batch_max_list = []
        self.cpu_MILP_batch_avg_list = []
        self.link_MILP_batch_max_list = []
        self.link_MILP_batch_avg_list = []
        self.time_MILP_batch_list = []

        self.cpu_MILP_max_list = []
        self.cpu_MILP_avg_list = []
        self.link_MILP_max_list = []
        self.link_MILP_avg_list = []
        self.time_MILP_list = []

        self.hop_num_MILP = []
        self.hop_num_heu_full = [[] for _ in range(len(self.tune_param))]
        self.hop_num_MILP_batch = []

        self.hop_num_MILP_list = []
        self.hop_num_heu_full_list = [[] for _ in range(len(self.tune_param))]
        self.hop_num_MILP_batch_list = []
        
    def run(self, approach_list, graph, chain, funs, k, alpha, batch_size, user_num):
        graph.make_empty_network()
        if 'HF' in approach_list:
            for i, tune_param in enumerate(self.tune_param):
                cpu_max, cpu_avg, link_max, link_avg, time, links_num =\
                    self.heu_full.run(graph, chain, funs, alpha, user_num, batch_size, k, tune_param)
                self.cpu_heu_full_max[i].append(cpu_max)
                self.cpu_heu_full_avg[i].append(cpu_avg)
                self.link_heu_full_max[i].append(link_max)
                self.link_heu_full_avg[i].append(link_avg) 
                self.time_heu_full[i].append(time)
                self.hop_num_heu_full[i].append(links_num)
                with open(self.input_cons.path_curve_MILP, 'a') as f:
                    print('KSP:'+str(k)+'/'+'alpha:'+str(alpha)+'/batchSize:'+str(batch_size)+'heu_cpu_max'+'-->', self.cpu_heu_full_max, file=f)
                    print('KSP:'+str(k)+'/'+'alpha:'+str(alpha)+'/batchSize:'+str(batch_size)+'heu_cpu_avg'+'-->', self.cpu_heu_full_avg, file=f)
                    print('KSP:'+str(k)+'/'+'alpha:'+str(alpha)+'/batchSize:'+str(batch_size)+'heu_link_max'+'-->', self.link_heu_full_max, file=f)
                    print('KSP:'+str(k)+'/'+'alpha:'+str(alpha)+'/batchSize:'+str(batch_size)+'heu_link_avg'+'-->', self.link_heu_full_avg, file=f)
                    print('KSP:'+str(k)+'/'+'alpha:'+str(alpha)+'/batchSize:'+str(batch_size)+'heu_time'+'-->', self.time_heu_full, file=f)
                    print('KSP:'+str(k)+'/'+'alpha:'+str(alpha)+'/batchSize:'+str(batch_size)+'heu_link_num'+'-->', self.hop_num_heu_full, file=f)
                graph.make_empty_network()
        if 'MILPB' in approach_list:
            cpu_max, cpu_avg, link_max, link_avg, time, links_num =\
                 self.MILP_batch.run(graph, chain, funs, k, alpha, user_num, batch_size)
            self.cpu_MILP_batch_max.append(cpu_max)
            self.cpu_MILP_batch_avg.append(cpu_avg)
            self.link_MILP_batch_max.append(link_max)
            self.link_MILP_batch_avg.append(link_avg)
            self.time_MILP_batch.append(time)
            self.hop_num_MILP_batch.append(links_num)
            with open(self.input_cons.path_curve_MILP, 'a') as f:
                print('KSP:'+str(k)+'/'+'alpha:'+str(alpha)+'/batchSize:'+str(batch_size)+'MILPB_cpu_max'+'-->', self.cpu_MILP_batch_max, file=f)
                print('KSP:'+str(k)+'/'+'alpha:'+str(alpha)+'/batchSize:'+str(batch_size)+'MILPB_cpu_avg'+'-->', self.cpu_MILP_batch_avg, file=f)
                print('KSP:'+str(k)+'/'+'alpha:'+str(alpha)+'/batchSize:'+str(batch_size)+'MILPB_link_max'+'-->', self.link_MILP_batch_max, file=f)
                print('KSP:'+str(k)+'/'+'alpha:'+str(alpha)+'/batchSize:'+str(batch_size)+'MILPB_link_avg'+'-->', self.link_MILP_batch_avg, file=f)
                print('KSP:'+str(k)+'/'+'alpha:'+str(alpha)+'/batchSize:'+str(batch_size)+'MILPB_time'+'-->', self.time_MILP_batch, file=f)
                print('KSP:'+str(k)+'/'+'alpha:'+str(alpha)+'/batchSize:'+str(batch_size)+'MILPB_link_num'+'-->', self.hop_num_MILP_batch, file=f)

            graph.make_empty_network()
        if 'MILP' in approach_list:
            cpu_max, cpu_avg, link_max, link_avg, time, links_num = self.MILP.run(graph, chain, funs, k, alpha)
            self.cpu_MILP_max.append(cpu_max)
            self.cpu_MILP_avg.append(cpu_avg)
            self.link_MILP_max.append(link_max)
            self.link_MILP_avg.append(link_avg)
            self.time_MILP.append(time)
            self.hop_num_MILP.append(links_num)
            with open(self.input_cons.path_curve_MILP, 'a') as f:
                 print('KSP:'+str(k)+'/'+'alpha:'+str(alpha)+'/batchSize:'+str(batch_size)+'MILP_cpu_max'+'-->', self.cpu_MILP_max, file=f)
                 print('KSP:'+str(k)+'/'+'alpha:'+str(alpha)+'/batchSize:'+str(batch_size)+'MILP_cpu_avg'+'-->', self.cpu_MILP_avg, file=f)
                 print('KSP:'+str(k)+'/'+'alpha:'+str(alpha)+'/batchSize:'+str(batch_size)+'MILP_link_max'+'-->', self.link_MILP_max, file=f)
                 print('KSP:'+str(k)+'/'+'alpha:'+str(alpha)+'/batchSize:'+str(batch_size)+'MILP_link_avg'+'-->', self.link_MILP_avg, file=f)
                 print('KSP:'+str(k)+'/'+'alpha:'+str(alpha)+'/batchSize:'+str(batch_size)+'MILP_time'+'-->', self.time_MILP, file=f)
                 print('KSP:'+str(k)+'/'+'alpha:'+str(alpha)+'/batchSize:'+str(batch_size)+'MILP_link_num'+'-->', self.hop_num_MILP, file=f)

            graph.make_empty_network()

    def box_plot_save(self, approach, user_num, k, alpha, batch_size, versus_chain, versus_user, show, fomat_list):
        max_load_links = [[]]
        max_load_CPU_nodes = [[]]
        avg_load_links = [[]]
        avg_load_CPU_nodes = [[]]
        links_num = [[]]
        labels = []
        if 'HF' in approach:
            for i in range(len(self.tune_param)):
                self.cpu_heu_full_max_list[i].append(sum(self.cpu_heu_full_max[i]) / len(self.cpu_heu_full_max[i]))
                self.cpu_heu_full_avg_list[i].append(sum(self.cpu_heu_full_avg[i]) / len(self.cpu_heu_full_avg[i]))
                self.link_heu_full_max_list[i].append(sum(self.link_heu_full_max[i]) / len(self.link_heu_full_max[i]))
                self.link_heu_full_avg_list[i].append(sum(self.link_heu_full_avg[i]) / len(self.link_heu_full_avg[i]))
                self.time_heu_full_list[i].append(sum(self.time_heu_full[i]) / len(self.time_heu_full[i]))
                self.hop_num_heu_full_list[i].append(sum(self.hop_num_heu_full[i]) / len(self.hop_num_heu_full[i]))
                max_load_CPU_nodes[0].append((
                        max(self.cpu_heu_full_max[i]),
                        np.percentile(self.cpu_heu_full_max[i], 75),
                        np.percentile(self.cpu_heu_full_max[i], 50), 
                        np.percentile(self.cpu_heu_full_max[i], 25), 
                        min(self.cpu_heu_full_max[i]))
                        )
                avg_load_CPU_nodes[0].append((
                        max(self.cpu_heu_full_avg[i]),
                        np.percentile(self.cpu_heu_full_avg[i], 75),
                        np.percentile(self.cpu_heu_full_avg[i], 50), 
                        np.percentile(self.cpu_heu_full_avg[i], 25), 
                        min(self.cpu_heu_full_avg[i]))
                        )
                            
                max_load_links[0].append((
                        max(self.link_heu_full_max[i]),
                        np.percentile(self.link_heu_full_max[i], 75),
                        np.percentile(self.link_heu_full_max[i], 50), 
                        np.percentile(self.link_heu_full_max[i], 25), 
                        min(self.link_heu_full_max[i]))
                        )

                avg_load_links[0].append((
                        max(self.link_heu_full_avg[i]),
                        np.percentile(self.link_heu_full_avg[i], 75),
                        np.percentile(self.link_heu_full_avg[i], 50), 
                        np.percentile(self.link_heu_full_avg[i], 25), 
                        min(self.link_heu_full_avg[i]))
                        )
        labels.append('LB-FH')
        
        if 'MILPB' in approach:
            self.cpu_MILP_batch_max_list.append(sum(self.cpu_MILP_batch_max) / len(self.cpu_MILP_batch_max))
            self.cpu_MILP_batch_avg_list.append(sum(self.cpu_MILP_batch_avg) / len(self.cpu_MILP_batch_avg))
            self.link_MILP_batch_max_list.append(sum(self.link_MILP_batch_max) / len(self.link_MILP_batch_max))
            self.link_MILP_batch_avg_list.append(sum(self.link_MILP_batch_avg) / len(self.link_MILP_batch_avg))
            self.time_MILP_batch_list.append(sum(self.time_MILP_batch) / len(self.time_MILP_batch))
            self.hop_num_MILP_batch_list.append(sum(self.hop_num_MILP_batch) / len(self.hop_num_MILP_batch))
            
            max_load_CPU_nodes.append((
                    max(self.cpu_MILP_batch_max),
                    np.percentile(self.cpu_MILP_batch_max, 75),
                    np.percentile(self.cpu_MILP_batch_max, 50), 
                    np.percentile(self.cpu_MILP_batch_max, 25), 
                    min(self.cpu_MILP_batch_max)
                    )
            )
            avg_load_CPU_nodes.append((
                    max(self.cpu_MILP_batch_max),
                    np.percentile(self.cpu_MILP_batch_max, 75),
                    np.percentile(self.cpu_MILP_batch_max, 50), 
                    np.percentile(self.cpu_MILP_batch_max, 25), 
                    min(self.cpu_MILP_batch_max)
                    )
            )
            
            max_load_links.append((
                    max(self.link_MILP_batch_max),
                    np.percentile(self.link_MILP_batch_max, 75),
                    np.percentile(self.link_MILP_batch_max, 50), 
                    np.percentile(self.link_MILP_batch_max, 25), 
                    min(self.link_MILP_batch_max)
                    )
            )
            avg_load_links.append((
                    max(self.link_MILP_batch_avg),
                    np.percentile(self.link_MILP_batch_avg, 75),
                    np.percentile(self.link_MILP_batch_avg, 50), 
                    np.percentile(self.link_MILP_batch_avg, 25), 
                    min(self.link_MILP_batch_avg)
                    )
            )

            labels.append('MILPB/')
            
        if 'MILP' in approach:    
            self.cpu_MILP_max_list.append(sum(self.cpu_MILP_max) / len(self.cpu_MILP_max))
            self.cpu_MILP_avg_list.append(sum(self.cpu_MILP_avg) / len(self.cpu_MILP_avg))
            self.link_MILP_max_list.append(sum(self.link_MILP_max) / len(self.link_MILP_max))
            self.link_MILP_avg_list.append(sum(self.link_MILP_avg) / len(self.link_MILP_avg))
            self.time_MILP_list.append(sum(self.time_MILP) / len(self.time_MILP))

            self.hop_num_MILP_list.append(sum(self.hop_num_MILP) / len(self.hop_num_MILP))
            max_load_CPU_nodes.append((
                    max(self.cpu_MILP_max),
                    np.percentile(self.cpu_MILP_max, 75),
                    np.percentile(self.cpu_MILP_max, 50), 
                    np.percentile(self.cpu_MILP_max, 25), 
                    min(self.cpu_MILP_max)
                    )
            )

            avg_load_CPU_nodes.append((
                    max(self.cpu_MILP_avg),
                    np.percentile(self.cpu_MILP_avg, 75),
                    np.percentile(self.cpu_MILP_avg, 50), 
                    np.percentile(self.cpu_MILP_avg, 25), 
                    min(self.cpu_MILP_avg)
                    )
            )
                    
            max_load_links.append((
                    max(self.link_MILP_max),
                    np.percentile(self.link_MILP_max, 75),
                    np.percentile(self.link_MILP_max, 50), 
                    np.percentile(self.link_MILP_max, 25), 
                    min(self.link_MILP_max)
                    )
            )

            avg_load_links.append((
                    max(self.link_MILP_avg),
                    np.percentile(self.link_MILP_avg, 75),
                    np.percentile(self.link_MILP_avg, 50), 
                    np.percentile(self.link_MILP_avg, 25), 
                    min(self.link_MILP_avg)
                    )
            )

            labels.append('MILP')
        # print(max_load_links[0][0])
        for i, tune in enumerate(self.tune_param):
            _, ax = plt.subplots()
            # ax.set_title('maximum CPU load'+'/'+'user num:'+str(user_num)+'/'+'K shortest path:'+str(k)+'/'+'alpha:'+str(alpha)+'/batchSize:'+str(batch_size))
            if versus_chain:
                plt.xlabel('chains number')
            elif versus_user:
                plt.xlabel('users number')
            plt.ylabel('Maximum CPU usage(%)')
            tmp = []
            tmp.append(max_load_CPU_nodes[0][i])
            tmp.extend(max_load_CPU_nodes[1:])
            with open(self.input_cons.path_text_box_plot, 'a') as f:
                print('maximum CPU load'+'/'+'user num:'+str(user_num)+'/'+'K shortest path:'+str(k)+'/'+'alpha:'+str(alpha)+'/batchSize:'+str(batch_size)+'_tune:'+str(tune)+'-->', tmp, file=f)
            ax.boxplot(tmp, labels=labels)
            for f in fomat_list:
                plt.savefig(self.input_cons.path_box_plot+'maxCPUcap_'+'usernum:'+str(user_num)+'_KSP:'+str(k)+'_alpah:'+str(alpha)+'_batchSize:'+str(batch_size)+'_tune:'+str(tune)+f)
            if show:
                plt.show()
            plt.close()
            
            _, ax = plt.subplots()
            # ax.set_title('average CPU load'+'/'+'user num:'+str(user_num)+'/'+'K shortest path:'+str(k)+'/'+'alpha:'+str(alpha)+'/batchSize:'+str(batch_size))
            if versus_chain:
                plt.xlabel('chains number')
            elif versus_user:
                plt.xlabel('users number')
            plt.ylabel('Average CPU usage(%)')
            tmp = []
            tmp.append(avg_load_CPU_nodes[0][i])
            tmp.extend(avg_load_CPU_nodes[1:])
            with open(self.input_cons.path_text_box_plot, 'a') as f:
                print('Average CPU usage'+'/'+'user num:'+str(user_num)+'/'+'K shortest path:'+str(k)+'/'+'alpha:'+str(alpha)+'/batchSize:'+str(batch_size)+'_tune:'+str(tune)+'-->', tmp, file=f)
            ax.boxplot(tmp, labels=labels)
            for f in fomat_list:
                plt.savefig(self.input_cons.path_box_plot+'avgCPUcap_'+'usernum:'+str(user_num)+'_KSP:'+str(k)+'_alpah:'+str(alpha)+'_batchSize:'+str(batch_size)+'_tune:'+str(tune)+f)
            if show:
                plt.show()
            plt.close()
            
            _, ax = plt.subplots()
            # ax.set_title('maximum links load'+'/'+'user num:'+str(user_num)+'/'+'K shortest path:'+str(k)+'/'+'alpha:'+str(alpha)+'/batchSize:'+str(batch_size))
            if versus_chain:
                plt.xlabel('chains number')
            elif versus_user:
                plt.xlabel('users number')
            plt.ylabel('Maximum bandwidth usage(%)')
            tmp = []
            tmp.append(max_load_links[0][i])
            tmp.extend(max_load_links[1:])
            with open(self.input_cons.path_text_box_plot, 'a') as f:
                print('Maximum bandwidth usage'+'/'+'user num:'+str(user_num)+'/'+'K shortest path:'+str(k)+'/'+'alpha:'+str(alpha)+'/batchSize:'+str(batch_size)+'_tune:'+str(tune)+'-->', tmp, file=f)
            ax.boxplot(tmp, labels=labels)
            for f in fomat_list:
                plt.savefig(self.input_cons.path_box_plot+'maxlinkcap_'+'usernum:'+str(user_num)+'_KSP:'+str(k)+'_alpah:'+str(alpha)+'_batchSize:'+str(batch_size)+'_tune:'+str(tune)+f)
            if show:
                plt.show()
            plt.close()
            
            _, ax = plt.subplots()
            # ax.set_title('average links load'+'/'+'user num:'+str(user_num)+'/'+'K shortest path:'+str(k)+'/'+'alpha:'+str(alpha)+'/batchSize:'+str(batch_size))
            if versus_chain:
                plt.xlabel('chains number')
            elif versus_user:
                plt.xlabel('users number')
            plt.ylabel('Average bandwidth usage(%)')
            tmp = []
            tmp.append(avg_load_links[0][i])
            tmp.extend(avg_load_links[1:])
         #   with open(self.input_cons.path_text_box_plot, 'a') as f:
        #        print('Average bandwidth usage'+'/'+'user num:'+str(user_num)+'/'+'K shortest path:'+str(k)+'/'+'alpha:'+str(alpha)+'/batchSize:'+str(batch_size)+'_tune:'+str(tune)+'-->', tmp, file=f)
       #     ax.boxplot(avg_load_links, labels=labels)
            for f in fomat_list:
                plt.savefig(self.input_cons.path_box_plot+'avglinkcap_'+'usernum:'+str(user_num)+'_KSP:'+str(k)+'_alpah:'+str(alpha)+'_batchSize:'+str(batch_size)+'_tune:'+str(tune)+f)
            if show:
                plt.show()
            plt.close()
    
        self.cpu_heu_full_max = [[] for _ in range(len(self.tune_param))]
        self.cpu_heu_full_avg = [[] for _ in range(len(self.tune_param))]
        self.link_heu_full_max = [[] for _ in range(len(self.tune_param))]
        self.link_heu_full_avg = [[] for _ in range(len(self.tune_param))] 
        self.time_heu_full = [[] for _ in range(len(self.tune_param))]
        self.hop_num_heu_full = [[] for _ in range(len(self.tune_param))]

        self.cpu_MILP_batch_max = []
        self.link_MILP_batch_max = []
        self.time_MILP_batch = []
        self.hop_num_MILP_batch = []

        self.cpu_MILP_batch_avg = []
        self.link_MILP_batch_avg = []
        self.time_MILP_batch = []
        
        self.cpu_MILP_max = []
        self.link_MILP_max = []
        self.time_MILP = [] 
        self.hop_num_MILP = []
        
        self.cpu_MILP_avg = []
        self.link_MILP_avg = []
        self.time_MILP = []    
        
    def curve(self, approach, alpha, batch_size, k, user_list, chain_list, user_num, chain_num, format_list, show, versus_chain, versus_user):
        # print(self.cpu_heu_full_max_list)
        with open(self.input_cons.path_text_box_plot, 'a') as f:
            if 'MILPB' in approach:
                print('KSP:'+str(k)+'/'+'alpha:'+str(alpha)+'/batchSize:'+str(batch_size)+'MILPB_cpu_max'+'-->', self.cpu_MILP_batch_max_list, file=f)
                #print('KSP:'+str(k)+'/'+'alpha:'+str(alpha)+'/batchSize:'+str(batch_size)+'MILPB_cpu_avg'+'-->', self.cpu_MILP_batch_avg_list, file=f)
                print('KSP:'+str(k)+'/'+'alpha:'+str(alpha)+'/batchSize:'+str(batch_size)+'MILPB_link_max'+'-->', self.link_MILP_batch_max_list, file=f)
               # print('KSP:'+str(k)+'/'+'alpha:'+str(alpha)+'/batchSize:'+str(batch_size)+'MILPB_link_avg'+'-->', self.link_MILP_batch_avg_list, file=f)
                print('KSP:'+str(k)+'/'+'alpha:'+str(alpha)+'/batchSize:'+str(batch_size)+'MILPB_time'+'-->', self.time_MILP_batch_list, file=f)
                print('KSP:'+str(k)+'/'+'alpha:'+str(alpha)+'/batchSize:'+str(batch_size)+'MILpb_hop_num'+'-->', self.hop_num_MILP_batch_list, file=f)
            if 'MILP' in approach:
                print('KSP:'+str(k)+'/'+'alpha:'+str(alpha)+'/batchSize:'+str(batch_size)+'MILP_cpu_max'+'-->', self.cpu_MILP_max_list, file=f)
#                print('KSP:'+str(k)+'/'+'alpha:'+str(alpha)+'/batchSize:'+str(batch_size)+'MILP_cpu_avg'+'-->', self.cpu_MILP_avg_list, file=f)
                print('KSP:'+str(k)+'/'+'alpha:'+str(alpha)+'/batchSize:'+str(batch_size)+'MILP_link_max'+'-->', self.link_MILP_max_list, file=f)
 #               print('KSP:'+str(k)+'/'+'alpha:'+str(alpha)+'/batchSize:'+str(batch_size)+'MILP_link_avg'+'-->', self.link_MILP_avg_list, file=f)
                print('KSP:'+str(k)+'/'+'alpha:'+str(alpha)+'/batchSize:'+str(batch_size)+'MILP_time'+'-->', self.time_MILP_list, file=f)
                print('KSP:'+str(k)+'/'+'alpha:'+str(alpha)+'/batchSize:'+str(batch_size)+'MILP_hop_num'+'-->', self.hop_num_MILP_list, file=f)
                
        for i, tune in enumerate(self.tune_param):
            _, ax = plt.subplots()
            
            if versus_chain:
#                plt.xlabel('chains number')
                # ax.set_title('KSP:'+str(k)+'/'+'alpha:'+str(alpha)+'/batchSize:'+str(batch_size))
                if 'HF' in approach:
 #                   plt.plot(chain_list, self.cpu_heu_full_max_list[i], 's', color='red')
  #                  plt.plot(chain_list, self.cpu_heu_full_max_list[i], color='red', label='LB-HF')
                    with open(self.input_cons.path_text_curve_versus_chain, 'a') as f:
                        print('KSP:'+str(k)+'/'+'alpha:'+str(alpha)+'/batchSize:'+str(batch_size)+'heu_cpu_max'+'/tune:'+str(tune)+'-->', self.cpu_heu_full_max_list, file=f)
                        print('KSP:'+str(k)+'/'+'alpha:'+str(alpha)+'/batchSize:'+str(batch_size)+'heu_hop_num'+'/tune:'+str(tune)+'-->', self.hop_num_heu_full_list,file=f)
                    
                if 'MILPB' in approach:
                    plt.plot(chain_list, self.cpu_MILP_batch_max_list, '*', color='black')
                    plt.plot(chain_list, self.cpu_MILP_batch_max_list, color='black', label='B-MILP')
                    with open(self.input_cons.path_text_curve_versus_chain, 'a') as f:
                        print('KSP:'+str(k)+'/'+'alpha:'+str(alpha)+'/batchSize:'+str(batch_size)+'BMILP_cpu_max'+'/tune:'+str(tune)+'-->', self.cpu_MILP_batch_max_list, file=f)
                
                if 'MILP' in approach:
                    plt.plot(chain_list, self.cpu_MILP_max_list, 'o', color='blue')
                    plt.plot(chain_list, self.cpu_MILP_max_list, color='blue', label='MILP')
                    with open(self.input_cons.path_text_curve_versus_chain, 'a') as f:
                        print('KSP:'+str(k)+'/'+'alpha:'+str(alpha)+'/batchSize:'+str(batch_size)+'MILP_cpu_max'+'/tune:'+str(tune)+'-->', self.cpu_MILP_batch_max_list, file=f)

                plt.ylabel('Maximum CPU usage(%)')
                plt.legend()
                plt.grid(True)
                if show:
                    plt.show()
                for f in format_list:
                    plt.savefig(self.input_cons.path_curve_versus_chain+'maxCPUvCHAIN'+'_KSP:'+str(k)+'_alpah:'+str(alpha)+'_batchSize:'+str(batch_size)+'_tune:'+str(tune)+f)
                plt.close()

            elif versus_user:
                plt.xlabel('users number')
                # ax.set_title('KSP:'+str(k)+'/'+'alpha:'+str(alpha)+'/batchSize:'+str(batch_size)+'/chains number:'+str(chain_num))
                
                if 'HF' in approach:
                    plt.plot(user_list, self.cpu_heu_full_max_list[i], 's', color='red')
                    plt.plot(user_list, self.cpu_heu_full_max_list[i], color='red', label='HF')
                if 'MILPB' in approach:
                    plt.plot(user_list, self.cpu_MILP_batch_max_list, '*', color='black')
                    plt.plot(user_list, self.cpu_MILP_batch_max_list, color='black', label='MILPB')
                if 'MILP' in approach:
                    plt.plot(user_list, self.cpu_MILP_max_list, 'o', color='blue')
                    plt.plot(user_list, self.cpu_MILP_max_list, color='blue', label='MILP')
                
                plt.ylabel('Maximum CPU usage(%)')
                plt.legend()
                plt.grid(True)
                if show:
                    plt.show()
                for f in format_list:
                    plt.savefig(self.input_cons.path_curve_versus_user+'maxCPUvUSER_'+'_KSP:'+str(k)+'_alpah:'+str(alpha)+'_batchSize:'+str(batch_size)+'_chains:'+str(chain_num)+'_tune:'+str(tune)+f)
                plt.close()

            _, ax = plt.subplots()
            if versus_chain:
                plt.xlabel('chains number')
                # ax.set_title('KSP:'+str(k)+'/'+'alpha:'+str(alpha)+'/batchSize:'+str(batch_size))
            #    if 'HF' in approach:
   #                 plt.plot(chain_list, self.cpu_heu_full_avg_list[i], 's', color='red')
    #                plt.plot(chain_list, self.cpu_heu_full_avg_list[i], color='red', label='HF')
                with open(self.input_cons.path_text_curve_versus_chain, 'a') as f:
                    print('KSP:'+str(k)+'/'+'alpha:'+str(alpha)+'/batchSize:'+str(batch_size)+'heu_cpu_avg'+'/tune:'+str(tune)+'-->', self.cpu_heu_full_avg_list, file=f)
                    print('KSP:'+str(k)+'/'+'alpha:'+str(alpha)+'/batchSize:'+str(batch_size)+'heu_hop_num'+'/tune:'+str(tune)+'-->', self.hop_num_heu_full_list, file=f)           
                if 'MILPB' in approach:
                    plt.plot(chain_list, self.cpu_MILP_batch_avg_list, '*', color='black')
                    plt.plot(chain_list, self.cpu_MILP_batch_avg_list, color='black', label='MILPB')
                if 'MILP' in approach:
                    plt.plot(chain_list, self.cpu_MILP_avg_list, 'o', color='blue')
                    plt.plot(chain_list, self.cpu_MILP_avg_list, color='blue', label='MILP')
                    
                plt.ylabel('Average CPU usage(%)')
                plt.legend()
                plt.grid(True)
                if show:
                    plt.show()
                for f in format_list:
                    plt.savefig(self.input_cons.path_curve_versus_chain+'avgCPUvCHAIN'+'_KSP:'+str(k)+'_alpah:'+str(alpha)+'_batchSize:'+str(batch_size)+'_tune:'+str(tune)+f)
                plt.close()

            elif versus_user:
                plt.xlabel('users number')
                # ax.set_title('KSP:'+str(k)+'/'+'alpha:'+str(alpha)+'/batchSize:'+str(batch_size)+'/chains number:'+str(chain_num))
                
                if 'HF' in approach:
                    plt.plot(user_list, self.cpu_heu_full_avg_list[i], 's', color='red')
                    plt.plot(user_list, self.cpu_heu_full_avg_list[i], color='red', label='HF')
                if 'MILPB' in approach:
                    plt.plot(user_list, self.cpu_MILP_batch_avg_list, '*', color='black')
                    plt.plot(user_list, self.cpu_MILP_batch_avg_list, color='black', label='MILPB')
                if 'MILP' in approach:
                    plt.plot(user_list, self.cpu_MILP_avg_list, 'o', color='blue')
                    plt.plot(user_list, self.cpu_MILP_avg_list, color='blue', label='MILP')
                
                plt.ylabel('Average CPU usage(%)')
                plt.legend()
                plt.grid(True)
                if show:
                    plt.show()
                for f in format_list:
                    plt.savefig(self.input_cons.path_curve_versus_user+'avgCPUvUSER_'+'_KSP:'+str(k)+'/alpah:'+str(alpha)+'_batchSize:'+str(batch_size)+'_chains:'+str(chain_num)+'_tune:'+str(tune)+f)
                plt.close()
        
            _, ax = plt.subplots()
            if versus_chain:
                # ax.set_title('KSP:'+str(k)+'/alpha:'+str(alpha)+'/batchSize:'+str(batch_size))
                
                if 'HF' in approach:
                    plt.plot(chain_list, self.time_heu_full_list[i], 's', color='red')
                    plt.plot(chain_list, self.time_heu_full_list[i], color='red', label='HF')
                    with open(self.input_cons.path_text_curve_versus_chain, 'a') as f:
                        print('KSP:'+str(k)+'/'+'alpha:'+str(alpha)+'/batchSize:'+str(batch_size)+'heu_time'+'/tune:'+str(tune)+'-->', self.time_heu_full_list, file=f)
                
                if 'MILPB' in approach:
                    plt.plot(chain_list, self.time_MILP_batch_list, '*', color='black')
                    plt.plot(chain_list, self.time_MILP_batch_list, color='black', label='MILPB')
                    with open(self.input_cons.path_text_curve_versus_chain, 'a') as f:
                        print('KSP:'+str(k)+'/'+'alpha:'+str(alpha)+'/batchSize:'+str(batch_size)+'BMILP_time'+'/tune:'+str(tune)+'-->', self.time_MILP_batch_list, file=f)
                
                if 'MILP' in approach:
                    plt.plot(chain_list, self.time_MILP_list, 'o', color='blue')
                    plt.plot(chain_list, self.time_MILP_list, color='blue', label='MILP')
                    with open(self.input_cons.path_text_curve_versus_chain, 'a') as f:
                        print('KSP:'+str(k)+'/'+'alpha:'+str(alpha)+'/batchSize:'+str(batch_size)+'MILP_time'+'/tune:'+str(tune)+'-->', self.time_MILP_list, file=f)
                
                plt.xlabel('chains number')
                plt.ylabel('Time (s)')
                plt.legend()
                plt.grid(True)
                if show:
                    plt.show()
                for f in format_list:
                    plt.savefig(self.input_cons.path_curve_versus_chain+'timevUSER_'+'_KSP:'+str(k)+'_alpah:'+str(alpha)+'_batchSize:'+str(batch_size)+'_tune:'+str(tune)+f)
                
                plt.close()
            elif versus_user:
                # ax.set_title('KSP:'+str(k)+'/alpha:'+str(alpha)+'/batchSize:'+str(batch_size))
                
                if 'HF' in approach:
                    plt.plot(user_list, self.time_heu_full_list[i], 's', color='red')
                    plt.plot(user_list, self.time_heu_full_list[i], color='red', label='HF')
                if 'MILPB' in approach:
                    plt.plot(user_list, self.time_MILP_batch_list, '*', color='black')
                    plt.plot(user_list, self.time_MILP_batch_list, color='black', label='MILPB')
                if 'MILP' in approach:
                    plt.plot(user_list, self.time_MILP_list, 'o', color='blue')
                    plt.plot(user_list, self.time_MILP_list, color='blue', label='MILP')
                
                if versus_chain:
                    plt.xlabel('users number')
                plt.ylabel('Time (s)')
                plt.legend()
                plt.grid(True)
                if show:
                    plt.show()
                for f in format_list:
                    plt.savefig(self.input_cons.versus_chain+'timevUSER_'+'_KSP:'+str(k)+'_alpah:'+str(alpha)+'_batchSize:'+str(batch_size)+'_chains:'+str(chains_num)+'_tune:'+str(tune)+f)  
                plt.close()
                
            _, ax = plt.subplots()
            if versus_chain:
                # ax.set_title('KSP:'+str(k)+'/'+'alpha:'+str(alpha)+'/batchSize:'+str(batch_size))
                
                if 'HF' in approach:
                    plt.plot(chain_list, self.link_heu_full_max_list[i], 's', color='red')
                    plt.plot(chain_list, self.link_heu_full_max_list[i], color='red', label='HF')
                    with open(self.input_cons.path_text_curve_versus_chain, 'a') as f:
                        print('KSP:'+str(k)+'/'+'alpha:'+str(alpha)+'/batchSize:'+str(batch_size)+'heu_link_max'+'/tune:'+str(tune)+'-->', self.link_heu_full_max_list, file=f)
                
                if 'MILPB' in approach:
                    plt.plot(chain_list, self.link_MILP_batch_max_list, '*', color='black')
                    plt.plot(chain_list, self.link_MILP_batch_max_list, color='black', label='MILPB')
                    with open(self.input_cons.path_text_curve_versus_chain, 'a') as f:
                        print('KSP:'+str(k)+'/'+'alpha:'+str(alpha)+'/batchSize:'+str(batch_size)+'BMILP_link_max'+'/tune:'+str(tune)+'-->', self.link_MILP_batch_max_list, file=f)
                
                if 'MILP' in approach:
                    plt.plot(chain_list, self.link_MILP_max_list, 'o', color='blue')
                    plt.plot(chain_list, self.link_MILP_max_list, color='blue', label='MILP')
                    with open(self.input_cons.path_text_curve_versus_chain, 'a') as f:
                        print('KSP:'+str(k)+'/'+'alpha:'+str(alpha)+'/batchSize:'+str(batch_size)+'MILP_link_max'+'/tune:'+str(tune)+'-->', self.link_MILP_max_list, file=f)
                    
                plt.xlabel('chains number')
                plt.ylabel('Maximum bandwidth usage (%)')
                plt.legend()
                plt.grid(True)
                if show:
                    plt.show()
                for f in format_list:        
                    plt.savefig(self.input_cons.path_curve_versus_chain+'maxbandwidthvUSER_'+'_KSP:'+str(k)+'_alpah:'+str(alpha)+'_batchSize:'+str(batch_size)+'_tune:'+str(tune)+f)
                
                plt.close()
            elif versus_user:
                # ax.set_title('KSP:'+str(k)+'/'+'alpha:'+str(alpha)+'/batchSize:'+str(batch_size))
                
                if 'HF' in approach:
                    plt.plot(user_list, self.link_heu_full_max_list[i], 's', color='red')
                    plt.plot(user_list, self.link_heu_full_max_list[i], color='red', label='HF')
                if 'MILPB' in approach:
                    plt.plot(user_list, self.link_MILP_batch_max_list, '*', color='black')
                    plt.plot(user_list, self.link_MILP_batch_max_list, color='black', label='MILPB')
                if 'MILP' in approach:
                    plt.plot(user_list, self.link_MILP_max_list, 'o', color='blue')
                    plt.plot(user_list, self.link_MILP_max_list, color='blue', label='MILP')
                
                plt.xlabel('users number')
                plt.ylabel('Maximum bandwidth usage (%)')
                plt.legend()
                plt.grid(True)
                if show:
                    plt.show()
                for f in format_list:        
                    plt.savefig(self.input_cons.path_curve_versus_user+'maxbandwidthvUSER_'+'_KSP:'+str(k)+'_alpah:'+str(alpha)+'_batchSize:'+str(batch_size)+'_users:'+str(user_num)+'_chains:'+str(chain_num)+'_tune:'+str(tune)+f)
                
                plt.close()

            _, ax = plt.subplots()
            if versus_chain:
                # ax.set_title('KSP:'+str(k)+'/'+'alpha:'+str(alpha)+'/batchSize:'+str(batch_size))
                
                if 'HF' in approach:
                    plt.plot(chain_list, self.link_heu_full_avg_list[i], 's', color='red')
                    plt.plot(chain_list, self.link_heu_full_avg_list[i], color='red', label='HF')
                with open(self.input_cons.path_text_curve_versus_chain, 'a') as f:
                    print('KSP:'+str(k)+'/'+'alpha:'+str(alpha)+'/batchSize:'+str(batch_size)+'heu_link_avg'+'/tune:'+str(tune)+'-->', self.link_heu_full_avg_list, file=f)
                
                if 'MILPB' in approach:
                    plt.plot(chain_list, self.link_MILP_batch_avg_list, '*', color='black')
                    plt.plot(chain_list, self.link_MILP_batch_avg_list, color='black', label='MILPB')
                if 'MILP' in approach:
                    plt.plot(chain_list, self.link_MILP_avg_list, 'o', color='blue')
                    plt.plot(chain_list, self.link_MILP_avg_list, color='blue', label='MILP')
                
                plt.xlabel('chains number')
                plt.ylabel('Average bandwidth usage (%)')
                plt.legend()
                plt.grid(True)
                if show:
                    plt.show()
                for f in format_list:        
                    plt.savefig(self.input_cons.path_curve_versus_chain+'avgbandwidthvUSER_'+'_KSP:'+str(k)+'_alpah:'+str(alpha)+'_batchSize:'+str(batch_size)+'_tune:'+str(tune)+f)
                
                plt.close()
            elif versus_user:
                # ax.set_title('KSP:'+str(k)+'/'+'alpha:'+str(alpha)+'/batchSize:'+str(batch_size))
                
                if 'HF' in approach:
                    plt.plot(user_list, self.link_heu_full_avg_list[i], 's', color='red')
                    plt.plot(user_list, self.link_heu_full_avg_list[i], color='red', label='HF')
                if 'MILPB' in approach:
                    plt.plot(user_list, self.link_MILP_batch_avg_list, '*', color='black')
                    plt.plot(user_list, self.link_MILP_batch_avg_list, color='black', label='MILPB')
                if 'MILP' in approach:
                    plt.plot(user_list, self.link_MILP_avg_list, 'o', color='blue')
                    plt.plot(user_list, self.link_MILP_avg_list, color='blue', label='MILP')
                
                plt.xlabel('users number')
                plt.ylabel('Average bandwidth usage (%)')
                plt.legend()
                plt.grid(True)
                if show:
                    plt.show()
                for f in format_list:        
                    plt.savefig(self.input_cons.path_curve_versus_user+'avgbandwidthvUSER_'+'_KSP:'+str(k)+'_alpah:'+str(alpha)+'_batchSize:'+str(batch_size)+'_users:'+str(user_num)+'_chains:'+str(chain_num)+'_tune:'+str(tune)+f)
                
                plt.close()
            if versus_chain:
                if 'HF' in approach:
                    plt.plot(chain_list, self.link_heu_full_max_list[i], 's', color='red', label='LB-HF-BW')
                    plt.plot(chain_list, self.link_heu_full_max_list[i], color='red')
                    plt.plot(chain_list, self.cpu_heu_full_avg_list[i], '^', color='g', label='LB-HF-CR')
                    plt.plot(chain_list, self.cpu_heu_full_avg_list[i], color='g')

                if 'MILPB' in approach:
                    plt.plot(chain_list, self.link_MILP_batch_max_list, '*', color='black', label='B-MILP-BW')
                    plt.plot(chain_list, self.link_MILP_batch_max_list, color='black')
                    plt.plot(chain_list, self.cpu_MILP_batch_avg_list, 'p', color='c',label='B-MILPB-CR')
                    plt.plot(chain_list, self.cpu_MILP_batch_avg_list, color='c')
    
                if 'MILP' in approach:
                    plt.plot(chain_list, self.link_MILP_max_list, 'o', color='blue', label='MILP-BW')
                    plt.plot(chain_list, self.link_MILP_max_list, color='blue')
                    plt.plot(chain_list, self.cpu_MILP_avg_list, '+', color='m', label='MILP-CPU')
                    plt.plot(chain_list, self.cpu_MILP_avg_list, color='m')
                    
                plt.xlabel('chains number')
                plt.ylabel('Maximum utilization (%)')
                plt.legend()
                plt.grid(True)
                if show:
                    plt.show()
                for f in format_list:        
                    plt.savefig(self.input_cons.path_curve_versus_chain+'CPU&BW_'+'_KSP:'+str(k)+'_alpah:'+str(alpha)+'_batchSize:'+str(batch_size)+'_tune:'+str(tune)+f)
                
                plt.close()    
            
        self.cpu_heu_full_max_list = [[] for _ in range(len(self.tune_param))]
        self.cpu_heu_full_avg_list = [[] for _ in range(len(self.tune_param))]
        self.link_heu_full_max_list = [[] for _ in range(len(self.tune_param))]
        self.link_heu_full_avg_list = [[] for _ in range(len(self.tune_param))]
        self.time_heu_full_list = [[] for _ in range(len(self.tune_param))]
                
        self.cpu_MILP_batch_max_list = []
        self.link_MILP_batch_max_list = []
        self.time_MILP_batch_list = []
        
        self.cpu_MILP_batch_avg_list = []
        self.link_MILP_batch_avg_list = []
        
        self.cpu_MILP_max_list = []
        self.link_MILP_max_list = []
        self.time_MILP_list = []
        
        self.cpu_MILP_avg_list = []
        self.link_MILP_avg_list = []
        
