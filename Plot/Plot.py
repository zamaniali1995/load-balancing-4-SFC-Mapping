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
            
        self.cpu_heu_full_max = []
        self.cpu_heu_full_avg = []
        self.link_heu_full_max = []
        self.link_heu_full_avg = [] 
        self.time_heu_full = []
            
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

        self.cpu_heu_full_max_list = []
        self.cpu_heu_full_avg_list = []
        self.link_heu_full_max_list = []
        self.link_heu_full_avg_list = []
        self.time_heu_full_list = []

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
        
    def run(self, approach_list, graph, chain, funs, k, alpha, batch_size, user_num):
        graph.make_empty_network()
        if 'HF' in approach_list:
            cpu_max, cpu_avg, link_max, link_avg, time =\
                 self.heu_full.run(graph, chain, funs, alpha, user_num, batch_size, k)
            self.cpu_heu_full_max.append(cpu_max)
            self.cpu_heu_full_avg.append(cpu_avg)
            self.link_heu_full_max.append(link_max)
            self.link_heu_full_avg.append(link_avg) 
            self.time_heu_full.append(time)
            graph.make_empty_network()
        if 'MILPB' in approach_list:
            cpu_max, cpu_avg, link_max, link_avg, time =\
                 self.MILP_batch.run(graph, chain, funs, k, alpha, user_num, batch_size)
            self.cpu_MILP_batch_max.append(cpu_max)
            self.cpu_MILP_batch_avg.append(cpu_avg)
            self.link_MILP_batch_max.append(link_max)
            self.link_MILP_batch_avg.append(link_avg)
            self.time_MILP_batch.append(time)
            graph.make_empty_network()
        if 'MILP' in approach_list:
            cpu_max, cpu_avg, link_max, link_avg, time = self.MILP.run(graph, chain, funs, k, alpha)
            self.cpu_MILP_max.append(cpu_max)
            self.cpu_MILP_avg.append(cpu_avg)
            self.link_MILP_max.append(link_max)
            self.link_MILP_avg.append(link_avg)
            self.time_MILP.append(time)
            graph.make_empty_network()

    def box_plot_save(self, approach, user_num, k, alpha, batch_size, versus_chain, versus_user, show, fomat_list):
        max_load_links = []
        max_load_CPU_nodes = []
        avg_load_links = []
        avg_load_CPU_nodes = []
        labels = []
        if 'HF' in approach:
            self.cpu_heu_full_max_list.append(sum(self.cpu_heu_full_max) / len(self.cpu_heu_full_max))
            self.cpu_heu_full_avg_list.append(sum(self.cpu_heu_full_avg) / len(self.cpu_heu_full_avg))
            self.link_heu_full_max_list.append(sum(self.link_heu_full_max) / len(self.link_heu_full_max))
            self.link_heu_full_avg_list.append(sum(self.link_heu_full_avg) / len(self.link_heu_full_avg))
            self.time_heu_full_list.append(sum(self.time_heu_full) / len(self.time_heu_full))
            max_load_CPU_nodes.append((
                    max(self.cpu_heu_full_max),
                    np.percentile(self.cpu_heu_full_max, 75),
                    np.percentile(self.cpu_heu_full_max, 50), 
                    np.percentile(self.cpu_heu_full_max, 25), 
                    min(self.cpu_heu_full_max))
                    )
            avg_load_CPU_nodes.append((
                    max(self.cpu_heu_full_avg),
                    np.percentile(self.cpu_heu_full_avg, 75),
                    np.percentile(self.cpu_heu_full_avg, 50), 
                    np.percentile(self.cpu_heu_full_avg, 25), 
                    min(self.cpu_heu_full_avg))
                    )
                        
            max_load_links.append((
                    max(self.link_heu_full_max),
                    np.percentile(self.link_heu_full_max, 75),
                    np.percentile(self.link_heu_full_max, 50), 
                    np.percentile(self.link_heu_full_max, 25), 
                    min(self.link_heu_full_max))
                    )

            avg_load_links.append((
                    max(self.link_heu_full_avg),
                    np.percentile(self.link_heu_full_avg, 75),
                    np.percentile(self.link_heu_full_avg, 50), 
                    np.percentile(self.link_heu_full_avg, 25), 
                    min(self.link_heu_full_avg))
                    )
            labels.append(('HF/'+'t:'+str(round(sum(self.time_heu_full)/len(self.time_heu_full), 2))))
        
        if 'MILPB' in approach:
            self.cpu_MILP_batch_max_list.append(sum(self.cpu_MILP_batch_max) / len(self.cpu_MILP_batch_max))
            self.cpu_MILP_batch_avg_list.append(sum(self.cpu_MILP_batch_avg) / len(self.cpu_MILP_batch_avg))
            self.link_MILP_batch_max_list.append(sum(self.link_MILP_batch_max) / len(self.link_MILP_batch_max))
            self.link_MILP_batch_avg_list.append(sum(self.link_MILP_batch_avg) / len(self.link_MILP_batch_avg))
            self.time_MILP_batch_list.append(sum(self.time_MILP_batch) / len(self.time_MILP_batch))
            
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

            labels.append(('MILPB/'+'t:'+str(round(sum(self.time_MILP_batch)/len(self.time_MILP_batch), 2)) ))
            
        if 'MILP' in approach:    
            self.cpu_MILP_max_list.append(sum(self.cpu_MILP_max) / len(self.cpu_MILP_max))
            self.cpu_MILP_avg_list.append(sum(self.cpu_MILP_avg) / len(self.cpu_MILP_avg))
            self.link_MILP_max_list.append(sum(self.link_MILP_max) / len(self.link_MILP_max))
            self.link_MILP_avg_list.append(sum(self.link_MILP_avg) / len(self.link_MILP_avg))
            self.time_MILP_list.append(sum(self.time_MILP) / len(self.time_MILP))

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

            labels.append(('MOF/'+'t:'+str(round(sum(self.time_MILP)/len(self.time_MILP), 2)) ))

        _, ax = plt.subplots()
        ax.set_title('maximum CPU load'+'/'+'user num:'+str(user_num)+'/'+'K shortest path:'+str(k)+'/'+'alpha:'+str(alpha)+'/batchSize:'+str(batch_size))
        if versus_chain:
            plt.xlabel('chains number')
        elif versus_user:
            plt.xlabel('users number')
        plt.ylabel('maximum cpu usage(%)')
        ax.boxplot(max_load_CPU_nodes, labels=labels)
        for f in fomat_list:
            plt.savefig(self.input_cons.path_box_plot+'maxCPUcap_'+'usernum:'+str(user_num)+'_KSP:'+str(k)+'_alpah:'+str(alpha)+'_batchSize:'+str(batch_size)+f)
        if show:
            plt.show()
        plt.close()
        
        _, ax = plt.subplots()
        ax.set_title('average CPU load'+'/'+'user num:'+str(user_num)+'/'+'K shortest path:'+str(k)+'/'+'alpha:'+str(alpha)+'/batchSize:'+str(batch_size))
        if versus_chain:
            plt.xlabel('chains number')
        elif versus_user:
            plt.xlabel('users number')
        plt.ylabel('average cpu usage(%)')
        ax.boxplot(avg_load_CPU_nodes, labels=labels)
        for f in fomat_list:
            plt.savefig(self.input_cons.path_box_plot+'avgCPUcap_'+'usernum:'+str(user_num)+'_KSP:'+str(k)+'_alpah:'+str(alpha)+'_batchSize:'+str(batch_size)+f)
        if show:
            plt.show()
        plt.close()
        
        _, ax = plt.subplots()
        ax.set_title('maximum links load'+'/'+'user num:'+str(user_num)+'/'+'K shortest path:'+str(k)+'/'+'alpha:'+str(alpha)+'/batchSize:'+str(batch_size))
        if versus_chain:
            plt.xlabel('chains number')
        elif versus_user:
            plt.xlabel('users number')
        plt.ylabel('maximum bandwidth usage(%)')
        ax.boxplot(max_load_links, labels=labels)
        for f in fomat_list:
            plt.savefig(self.input_cons.path_box_plot+'maxlinkcap_'+'usernum:'+str(user_num)+'_KSP:'+str(k)+'_alpah:'+str(alpha)+'_batchSize:'+str(batch_size)+f)
        if show:
            plt.show()
        plt.close()
        
        _, ax = plt.subplots()
        ax.set_title('average links load'+'/'+'user num:'+str(user_num)+'/'+'K shortest path:'+str(k)+'/'+'alpha:'+str(alpha)+'/batchSize:'+str(batch_size))
        if versus_chain:
            plt.xlabel('chains number')
        elif versus_user:
            plt.xlabel('users number')
        plt.ylabel('average bandwidth usage(%)')
        ax.boxplot(avg_load_links, labels=labels)
        for f in fomat_list:
            plt.savefig(self.input_cons.path_box_plot+'avglinkcap_'+'usernum:'+str(user_num)+'_KSP:'+str(k)+'_alpah:'+str(alpha)+'_batchSize:'+str(batch_size)+f)
        if show:
            plt.show()
        plt.close()
    
        self.cpu_heu_full_max = []
        self.link_heu_full_max = []
        self.time_heu_full = []
        
        self.cpu_heu_full_avg = []
        self.link_heu_full_avg = []
        self.time_heu_full = []

        self.cpu_MILP_batch_max = []
        self.link_MILP_batch_max = []
        self.time_MILP_batch = []
        
        self.cpu_MILP_batch_avg = []
        self.link_MILP_batch_avg = []
        self.time_MILP_batch = []
        
        self.cpu_MILP_max = []
        self.link_MILP_max = []
        self.time_MILP = []    
        
        self.cpu_MILP_avg = []
        self.link_MILP_avg = []
        self.time_MILP = []    
        
    def curve(self, approach, alpha, batch_size, k, user_list, chain_list, user_num, chain_num, format_list, show, versus_chain, versus_user):
        
        _, ax = plt.subplots()
        if versus_chain:
            plt.xlabel('chains number')
            ax.set_title('KSP:'+str(k)+'/'+'alpha:'+str(alpha)+'/batchSize:'+str(batch_size))
            if 'HF' in approach:
                plt.plot(chain_list, self.cpu_heu_full_max_list, 's', color='red')
                plt.plot(chain_list, self.cpu_heu_full_max_list, color='red', label='HF')
            if 'MILPB' in approach:
                plt.plot(chain_list, self.cpu_MILP_batch_max_list, '*', color='black')
                plt.plot(chain_list, self.cpu_MILP_batch_max_list, color='black', label='MILPB')
            if 'MILP' in approach:
                plt.plot(chain_list, self.cpu_MILP_max_list, 'o', color='blue')
                plt.plot(chain_list, self.cpu_MILP_max_list, color='blue', label='MILP')
                
            plt.ylabel('maximum CPU usage(%)')
            plt.legend()
            plt.grid(True)
            if show:
                plt.show()
            for f in format_list:
                plt.savefig(self.input_cons.path_curve_versus_chain+'maxCPUvCHAIN'+'_KSP:'+str(k)+'_alpah:'+str(alpha)+'_batchSize:'+str(batch_size)+f)
            plt.close()

        elif versus_user:
            plt.xlabel('users number')
            ax.set_title('KSP:'+str(k)+'/'+'alpha:'+str(alpha)+'/batchSize:'+str(batch_size)+'/chains number:'+str(chain_num))
            
            if 'HF' in approach:
                plt.plot(user_list, self.cpu_heu_full_max_list, 's', color='red')
                plt.plot(user_list, self.cpu_heu_full_max_list, color='red', label='HF')
            if 'MILPB' in approach:
                plt.plot(user_list, self.cpu_MILP_batch_max_list, '*', color='black')
                plt.plot(user_list, self.cpu_MILP_batch_max_list, color='black', label='MILPB')
            if 'MILP' in approach:
                plt.plot(user_list, self.cpu_MILP_max_list, 'o', color='blue')
                plt.plot(user_list, self.cpu_MILP_max_list, color='blue', label='MILP')
            
            plt.ylabel('maximum CPU usage(%)')
            plt.legend()
            plt.grid(True)
            if show:
                plt.show()
            for f in format_list:
                plt.savefig(self.input_cons.path_curve_versus_user+'maxCPUvUSER_'+'_KSP:'+str(k)+'_alpah:'+str(alpha)+'_batchSize:'+str(batch_size)+'_chains:'+str(chain_num)+f)
            plt.close()

        _, ax = plt.subplots()
        if versus_chain:
            plt.xlabel('chains number')
            ax.set_title('KSP:'+str(k)+'/'+'alpha:'+str(alpha)+'/batchSize:'+str(batch_size))
            if 'HF' in approach:
                plt.plot(chain_list, self.cpu_heu_full_avg_list, 's', color='red')
                plt.plot(chain_list, self.cpu_heu_full_avg_list, color='red', label='HF')
            if 'MILPB' in approach:
                plt.plot(chain_list, self.cpu_MILP_batch_avg_list, '*', color='black')
                plt.plot(chain_list, self.cpu_MILP_batch_avg_list, color='black', label='MILPB')
            if 'MILP' in approach:
                plt.plot(chain_list, self.cpu_MILP_avg_list, 'o', color='blue')
                plt.plot(chain_list, self.cpu_MILP_avg_list, color='blue', label='MILP')
                
            plt.ylabel('average CPU usage(%)')
            plt.legend()
            plt.grid(True)
            if show:
                plt.show()
            for f in format_list:
                plt.savefig(self.input_cons.path_curve_versus_chain+'avgCPUvCHAIN'+'_KSP:'+str(k)+'_alpah:'+str(alpha)+'_batchSize:'+str(batch_size)+f)
            plt.close()

        elif versus_user:
            plt.xlabel('users number')
            ax.set_title('KSP:'+str(k)+'/'+'alpha:'+str(alpha)+'/batchSize:'+str(batch_size)+'/chains number:'+str(chain_num))
            
            if 'HF' in approach:
                plt.plot(user_list, self.cpu_heu_full_avg_list, 's', color='red')
                plt.plot(user_list, self.cpu_heu_full_avg_list, color='red', label='HF')
            if 'MILPB' in approach:
                plt.plot(user_list, self.cpu_MILP_batch_avg_list, '*', color='black')
                plt.plot(user_list, self.cpu_MILP_batch_avg_list, color='black', label='MILPB')
            if 'MILP' in approach:
                plt.plot(user_list, self.cpu_MILP_avg_list, 'o', color='blue')
                plt.plot(user_list, self.cpu_MILP_avg_list, color='blue', label='MILP')
            
            plt.ylabel('average CPU usage(%)')
            plt.legend()
            plt.grid(True)
            if show:
                plt.show()
            for f in format_list:
                plt.savefig(self.input_cons.path_curve_versus_user+'avgCPUvUSER_'+'_KSP:'+str(k)+'_alpah:'+str(alpha)+'_batchSize:'+str(batch_size)+'_chains:'+str(chain_num)+f)
            plt.close()
    
        _, ax = plt.subplots()
        if versus_chain:
            ax.set_title('KSP:'+str(k)+'/alpha:'+str(alpha)+'/batchSize:'+str(batch_size))
            
            if 'HF' in approach:
                plt.plot(chain_list, self.time_heu_full_list, 's', color='red')
                plt.plot(chain_list, self.time_heu_full_list, color='red', label='HF')
            if 'MILPB' in approach:
                plt.plot(chain_list, self.time_MILP_batch_list, '*', color='black')
                plt.plot(chain_list, self.time_MILP_batch_list, color='black', label='MILPB')
            if 'MILP' in approach:
                plt.plot(chain_list, self.time_MILP_list, 'o', color='blue')
                plt.plot(chain_list, self.time_MILP_list, color='blue', label='MILP')
            
            plt.xlabel('chains number')
            plt.ylabel('time (s)')
            plt.legend()
            plt.grid(True)
            if show:
                plt.show()
            for f in format_list:
                plt.savefig(self.input_cons.path_curve_versus_chain+'timevUSER_'+'_KSP:'+str(k)+'_alpah:'+str(alpha)+'_batchSize:'+str(batch_size)+f)
            
            plt.close()
        elif versus_user:
            ax.set_title('KSP:'+str(k)+'/alpha:'+str(alpha)+'/batchSize:'+str(batch_size))
            
            if 'HF' in approach:
                plt.plot(user_list, self.time_heu_full_list, 's', color='red')
                plt.plot(user_list, self.time_heu_full_list, color='red', label='HF')
            if 'MILPB' in approach:
                plt.plot(user_list, self.time_MILP_batch_list, '*', color='black')
                plt.plot(user_list, self.time_MILP_batch_list, color='black', label='MILPB')
            if 'MILP' in approach:
                plt.plot(user_list, self.time_MILP_list, 'o', color='blue')
                plt.plot(user_list, self.time_MILP_list, color='blue', label='MILP')
            
            if versus_chain:
                plt.xlabel('users number')
            plt.ylabel('time (s)')
            plt.legend()
            plt.grid(True)
            if show:
                plt.show()
            for f in format_list:
                plt.savefig(self.input_cons.versus_chain+'timevUSER_'+'_KSP:'+str(k)+'_alpah:'+str(alpha)+'_batchSize:'+str(batch_size)+'_chains:'+str(chains_num)+f)  
            plt.close()
            
        _, ax = plt.subplots()
        if versus_chain:
            ax.set_title('KSP:'+str(k)+'/'+'alpha:'+str(alpha)+'/batchSize:'+str(batch_size))
            
            if 'HF' in approach:
                plt.plot(chain_list, self.link_heu_full_max_list, 's', color='red')
                plt.plot(chain_list, self.link_heu_full_max_list, color='red', label='HF')
            if 'MILPB' in approach:
                plt.plot(chain_list, self.link_MILP_batch_max_list, '*', color='black')
                plt.plot(chain_list, self.link_MILP_batch_max_list, color='black', label='MILPB')
            if 'MILP' in approach:
                plt.plot(chain_list, self.link_MILP_max_list, 'o', color='blue')
                plt.plot(chain_list, self.link_MILP_max_list, color='blue', label='MILP')
            
            plt.xlabel('chains number')
            plt.ylabel('maximum bandwidth usage (%)')
            plt.legend()
            plt.grid(True)
            if show:
                plt.show()
            for f in format_list:        
                plt.savefig(self.input_cons.path_curve_versus_chain+'maxbandwidthvUSER_'+'_KSP:'+str(k)+'_alpah:'+str(alpha)+'_batchSize:'+str(batch_size)+f)
            
            plt.close()
        elif versus_user:
            ax.set_title('KSP:'+str(k)+'/'+'alpha:'+str(alpha)+'/batchSize:'+str(batch_size))
            
            if 'HF' in approach:
                plt.plot(user_list, self.link_heu_full_max_list, 's', color='red')
                plt.plot(user_list, self.link_heu_full_max_list, color='red', label='HF')
            if 'MILPB' in approach:
                plt.plot(user_list, self.link_MILP_batch_max_list, '*', color='black')
                plt.plot(user_list, self.link_MILP_batch_max_list, color='black', label='MILPB')
            if 'MILP' in approach:
                plt.plot(user_list, self.link_MILP_max_list, 'o', color='blue')
                plt.plot(user_list, self.link_MILP_max_list, color='blue', label='MILP')
            
            plt.xlabel('users number')
            plt.ylabel('maximum bandwidth usage (%)')
            plt.legend()
            plt.grid(True)
            if show:
                plt.show()
            for f in format_list:        
                plt.savefig(self.input_cons.path_curve_versus_user+'maxbandwidthvUSER_'+'_KSP:'+str(k)+'_alpah:'+str(alpha)+'_batchSize:'+str(batch_size)+'_users:'+str(user_num)+'_chains:'+str(chain_num)+f)
            
            plt.close()

        _, ax = plt.subplots()
        if versus_chain:
            ax.set_title('KSP:'+str(k)+'/'+'alpha:'+str(alpha)+'/batchSize:'+str(batch_size))
            
            if 'HF' in approach:
                plt.plot(chain_list, self.link_heu_full_avg_list, 's', color='red')
                plt.plot(chain_list, self.link_heu_full_avg_list, color='red', label='HF')
            if 'MILPB' in approach:
                plt.plot(chain_list, self.link_MILP_batch_avg_list, '*', color='black')
                plt.plot(chain_list, self.link_MILP_batch_avg_list, color='black', label='MILPB')
            if 'MILP' in approach:
                plt.plot(chain_list, self.link_MILP_avg_list, 'o', color='blue')
                plt.plot(chain_list, self.link_MILP_avg_list, color='blue', label='MILP')
            
            plt.xlabel('chains number')
            plt.ylabel('average bandwidth usage (%)')
            plt.legend()
            plt.grid(True)
            if show:
                plt.show()
            for f in format_list:        
                plt.savefig(self.input_cons.path_curve_versus_chain+'avgbandwidthvUSER_'+'_KSP:'+str(k)+'_alpah:'+str(alpha)+'_batchSize:'+str(batch_size)+f)
            
            plt.close()
        elif versus_user:
            ax.set_title('KSP:'+str(k)+'/'+'alpha:'+str(alpha)+'/batchSize:'+str(batch_size))
            
            if 'HF' in approach:
                plt.plot(user_list, self.link_heu_full_avg_list, 's', color='red')
                plt.plot(user_list, self.link_heu_full_avg_list, color='red', label='HF')
            if 'MILPB' in approach:
                plt.plot(user_list, self.link_MILP_batch_avg_list, '*', color='black')
                plt.plot(user_list, self.link_MILP_batch_avg_list, color='black', label='MILPB')
            if 'MILP' in approach:
                plt.plot(user_list, self.link_MILP_avg_list, 'o', color='blue')
                plt.plot(user_list, self.link_MILP_avg_list, color='blue', label='MILP')
            
            plt.xlabel('users number')
            plt.ylabel('average bandwidth usage (%)')
            plt.legend()
            plt.grid(True)
            if show:
                plt.show()
            for f in format_list:        
                plt.savefig(self.input_cons.path_curve_versus_user+'avgbandwidthvUSER_'+'_KSP:'+str(k)+'_alpah:'+str(alpha)+'_batchSize:'+str(batch_size)+'_users:'+str(user_num)+'_chains:'+str(chain_num)+f)
            
            plt.close()
            
        self.cpu_heu_full_max_list = []
        self.link_heu_full_max_list = []
        self.time_heu_full_list = []

        self.cpu_heu_full_avg_list = []
        self.link_heu_full_avg_list = []
                
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
        