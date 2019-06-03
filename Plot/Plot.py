import sys
import numpy as np

sys.path.insert(0, './PaperFunctions')
sys.path.insert(1, './Given')
sys.path.insert(1, './Models')
sys.path.insert(1, './Plot')
from MILP_offline import MILP_offline_model
from MILP_online import MILP_online_model
from heuristic_offline import heuristic_offline_model
from heuristic_online import heuristic_online_model
from MILP_online_batch import MILP_online_batch_model
from heuristic_online_batch import heuristic_online_batch_model
from heuristic_fully_online_batch import heuristic_fully_batch_model
import matplotlib.pyplot as plt
from decimal import Decimal, ROUND_DOWN
import InputConstants


class Plot:
    def __init__(self):
        self.input_cons = InputConstants.Inputs()
        self.heu_online = heuristic_online_model()
        self.heu_online_batch = heuristic_online_batch_model()
        self.heu_offline = heuristic_offline_model()
        self.heu_fully = heuristic_fully_batch_model()
        self.MILP_online = MILP_online_model()
        self.MILP_online_batch = MILP_online_batch_model()
        self.MILP_offline = MILP_offline_model()

        self.cpu_heu_online = []
        self.link_heu_online = []
        self.time_heu_online = []
        self.mem_heu_online = []
        
        self.cpu_heu_online_batch = []
        self.link_heu_online_batch = []
        self.time_heu_online_batch = []
        self.mem_heu_online_batch = []
        
        self.cpu_heu_offline = []
        self.link_heu_offline = []
        self.time_heu_offline = []
        self.mem_heu_offline = []
            
        self.cpu_heu_fully_batch = []
        self.link_heu_fully_batch = []
        self.time_heu_fully_batch = []
        self.mem_heu_fully_batch = []

        self.cpu_MILP_online = []
        self.link_MILP_online = []
        self.time_MILP_online = []
        self.mem_MILP_online = []

        self.cpu_MILP_batch_online = []
        self.link_MILP_batch_online = []
        self.time_MILP_batch_online = []
        self.mem_MILP_batch_online = []

        self.cpu_MILP_offline = []
        self.link_MILP_offline = []
        self.time_MILP_offline = []
        self.mem_MILP_offline = []
            
        self.cpu_heu_online_batch_list = []
        self.link_heu_online_batch_list = []
        self.time_heu_online_batch_list = []
        self.mem_heu_online_batch_list = []

        self.cpu_heu_fully_batch_list = []
        self.link_heu_fully_batch_list = []
        self.time_heu_fully_batch_list = []
        self.mem_heu_fully_batch_list = []
                
        self.cpu_MILP_online_list = []
        self.link_MILP_online_list = []
        self.time_MILP_online_list = []
        self.mem_MILP_online_list = []
        
        self.cpu_MILP_batch_online_list = []
        self.link_MILP_batch_online_list = []
        self.time_MILP_batch_online_list = []
        self.mem_MILP_batch_online_list = []
        
        self.cpu_heu_offline_list = []
        self.link_heu_offline_list = []
        self.time_heu_offline_list = []
        self.mem_heu_offline_list = []
        
        self.cpu_heu_online_list = []
        self.link_heu_online_list = []
        self.time_heu_online_list = []
        self.mem_heu_online_list = []
        
        self.cpu_MILP_offline_list = []
        self.link_MILP_offline_list = []
        self.time_MILP_offline_list = []
        self.mem_MILP_offline_list = []
        
    def run(self, approach_list, graph, chain, funs, k, alpha, batch_size, user_num):
        # print(approach_list)
        graph.make_empty_network()
        if 'HON' in approach_list:            
            cpu, link, time, mem = self.heu_online.run(graph, chain, funs, k, alpha)
            self.cpu_heu_online.append(cpu)
            self.link_heu_online.append(link)
            self.time_heu_online.append(time)
            self.mem_heu_online.append(mem)
            graph.make_empty_network()
        if 'HONB' in approach_list:
            cpu, link, time, mem = self.heu_online_batch.run(graph, chain, funs, k, alpha, user_num, batch_size)
            self.cpu_heu_online_batch.append(cpu)
            self.link_heu_online_batch.append(link)
            self.time_heu_online_batch.append(time)
            self.mem_heu_online_batch.append(mem)
            graph.make_empty_network()
        if 'HOF' in approach_list:
            cpu, link, time, mem = self.heu_offline.run(graph, chain, funs, k, alpha)
            self.cpu_heu_offline.append(cpu)
            self.link_heu_offline.append(link)
            self.time_heu_offline.append(time)
            self.mem_heu_offline.append(mem)
            graph.make_empty_network()
        if 'HFB' in approach_list:
            cpu, link, time, mem = self.heu_fully.run(graph, chain, funs, alpha, user_num, batch_size, k)
            self.cpu_heu_fully_batch.append(cpu)
            self.link_heu_fully_batch.append(link)
            self.time_heu_fully_batch.append(time)
            self.mem_heu_fully_batch.append(mem)
            graph.make_empty_network()
        if 'MON' in approach_list:
            cpu, link, time, mem = self.MILP_online.run(graph, chain, funs, k, alpha)
            self.cpu_MILP_online.append(cpu)
            self.link_MILP_online.append(link)
            self.time_MILP_online.append(time)
            self.mem_MILP_online.append(mem)
            graph.make_empty_network()
        if 'MONB' in approach_list:
            cpu, link, time, mem = self.MILP_online_batch.run(graph, chain, funs, k, alpha, user_num, batch_size)
            self.cpu_MILP_batch_online.append(cpu)
            self.link_MILP_batch_online.append(link)
            self.time_MILP_batch_online.append(time)
            self.mem_MILP_batch_online.append(mem)
            graph.make_empty_network()
        if 'MOF' in approach_list:
            cpu, link, time, mem = self.MILP_offline.run(graph, chain, funs, k, alpha)
            self.cpu_MILP_offline.append(cpu)
            self.link_MILP_offline.append(link)
            self.time_MILP_offline.append(time)
            self.mem_MILP_offline.append(mem)
            graph.make_empty_network()

    def box_plot_save(self, approach, user_num, k, alpha, batch_size, versus_chain, versus_user, show, fomat_list):
        load_links = []
        load_CPU_nodes = []
        load_mem_nodes = []
        labels = []
        if 'HONB' in approach:
            self.cpu_heu_online_batch_list.append(sum(self.cpu_heu_online_batch) / len(self.cpu_heu_online_batch))
            self.link_heu_online_batch_list.append(sum(self.link_heu_online_batch) / len(self.link_heu_online_batch))
            self.time_heu_online_batch_list.append(sum(self.time_heu_online_batch) / len(self.time_heu_online_batch))
            self.mem_heu_online_batch_list.append(sum(self.mem_heu_online_batch) / len(self.mem_heu_online_batch))
            load_CPU_nodes.append((
                    max(self.cpu_heu_online_batch),
                    np.percentile(self.cpu_heu_online_batch, 75),
                    np.percentile(self.cpu_heu_online_batch, 50), 
                    np.percentile(self.cpu_heu_online_batch, 25), 
                    min(self.cpu_heu_online_batch))
                    )
            labels.append(('HONB/'+'t:'+str(round(sum(self.time_heu_online_batch)/len(self.time_heu_online_batch), 2))))
            load_mem_nodes.append((
                max(self.mem_heu_online_batch),
                np.percentile(self.mem_heu_online_batch, 75),
                np.percentile(self.mem_heu_online_batch, 50), 
                np.percentile(self.mem_heu_online_batch, 25), 
                min(self.mem_heu_online_batch))
                )
        
        if 'HFB' in approach:
            self.cpu_heu_fully_batch_list.append(sum(self.cpu_heu_fully_batch) / len(self.cpu_heu_fully_batch))
            self.link_heu_fully_batch_list.append(sum(self.link_heu_fully_batch) / len(self.link_heu_fully_batch))
            self.time_heu_fully_batch_list.append(sum(self.time_heu_fully_batch) / len(self.time_heu_fully_batch))
            self.mem_heu_fully_batch_list.append(sum(self.mem_heu_fully_batch) / len(self.mem_heu_fully_batch))
            load_CPU_nodes.append((
                    max(self.cpu_heu_fully_batch),
                    np.percentile(self.cpu_heu_fully_batch, 75),
                    np.percentile(self.cpu_heu_fully_batch, 50), 
                    np.percentile(self.cpu_heu_fully_batch, 25), 
                    min(self.cpu_heu_fully_batch))
                    )
            labels.append(('HFB/'+'t:'+str(round(sum(self.time_heu_fully_batch)/len(self.time_heu_fully_batch), 2))))
            load_mem_nodes.append((
                    max(self.mem_heu_fully_batch),
                    np.percentile(self.mem_heu_fully_batch, 75),
                    np.percentile(self.mem_heu_fully_batch, 50), 
                    np.percentile(self.mem_heu_fully_batch, 25), 
                    min(self.mem_heu_fully_batch))
                    )
            load_links.append((
                    max(self.link_heu_fully_batch),
                    np.percentile(self.link_heu_fully_batch, 75),
                    np.percentile(self.link_heu_fully_batch, 50), 
                    np.percentile(self.link_heu_fully_batch, 25), 
                    min(self.link_heu_fully_batch))
                    )
        
        if 'MON' in approach:            
            self.cpu_MILP_online_list.append(sum(self.cpu_MILP_online) / len(self.cpu_MILP_online))
            self.link_MILP_online_list.append(sum(self.link_MILP_online) / len(self.link_MILP_online))
            self.time_MILP_online_list.append(sum(self.time_MILP_online) / len(self.time_MILP_online))
            self.mem_MILP_online_list.append(sum(self.mem_MILP_online) / len(self.mem_MILP_online))
            load_CPU_nodes.append((
                    max(self.cpu_MILP_online),
                    np.percentile(self.cpu_MILP_online, 75),
                    np.percentile(self.cpu_MILP_online, 50), 
                    np.percentile(self.cpu_MILP_online, 25), 
                    min(self.cpu_MILP_online)
                    )
            )
            labels.append(('MON/'+'t:'+str(round(sum(self.time_MILP_online)/len(self.time_MILP_online), 2)) ))
            load_mem_nodes.append((
                    max(self.mem_MILP_online),
                    np.percentile(self.mem_MILP_online, 75),
                    np.percentile(self.mem_MILP_online, 50), 
                    np.percentile(self.mem_MILP_online, 25), 
                    min(self.mem_MILP_online)
                    )
            )
            load_links.append((
                    max(self.link_MILP_online),
                    np.percentile(self.link_MILP_online, 75),
                    np.percentile(self.link_MILP_online, 50), 
                    np.percentile(self.link_MILP_online, 25), 
                    min(self.link_MILP_online)
                    )
            )
        
        if 'MONB' in approach:
            self.cpu_MILP_batch_online_list.append(sum(self.cpu_MILP_batch_online) / len(self.cpu_MILP_batch_online))
            self.link_MILP_batch_online_list.append(sum(self.link_MILP_batch_online) / len(self.link_MILP_batch_online))
            self.time_MILP_batch_online_list.append(sum(self.time_MILP_batch_online) / len(self.time_MILP_batch_online))
            self.mem_MILP_batch_online_list.append(sum(self.mem_MILP_batch_online) / len(self.mem_MILP_batch_online))
            load_CPU_nodes.append((
                    max(self.cpu_MILP_batch_online),
                    np.percentile(self.cpu_MILP_batch_online, 75),
                    np.percentile(self.cpu_MILP_batch_online, 50), 
                    np.percentile(self.cpu_MILP_batch_online, 25), 
                    min(self.cpu_MILP_batch_online)
                    )
            )
            labels.append(('MONB/'+'t:'+str(round(sum(self.time_MILP_batch_online)/len(self.time_MILP_batch_online), 2)) ))
            load_mem_nodes.append((
                    max(self.mem_MILP_batch_online),
                    np.percentile(self.mem_MILP_batch_online, 75),
                    np.percentile(self.mem_MILP_batch_online, 50), 
                    np.percentile(self.mem_MILP_batch_online, 25), 
                    min(self.mem_MILP_batch_online)
                    )
            )
            load_links.append((
                    max(self.link_MILP_batch_online),
                    np.percentile(self.link_MILP_batch_online, 75),
                    np.percentile(self.link_MILP_batch_online, 50), 
                    np.percentile(self.link_MILP_batch_online, 25), 
                    min(self.link_MILP_online)
                    )
            )
            load_links.append((
                    max(self.link_heu_online_batch),
                    np.percentile(self.link_heu_online_batch, 75),
                    np.percentile(self.link_heu_online_batch, 50), 
                    np.percentile(self.link_heu_online_batch, 25), 
                    min(self.link_heu_online_batch))
                    )
        
        if 'MOF' in approach:    
            self.cpu_MILP_offline_list.append(sum(self.cpu_MILP_offline) / len(self.cpu_MILP_offline))
            self.link_MILP_offline_list.append(sum(self.link_MILP_offline) / len(self.link_MILP_offline))
            self.time_MILP_offline_list.append(sum(self.time_MILP_offline) / len(self.time_MILP_offline))
            self.mem_MILP_offline_list.append(sum(self.mem_MILP_offline) / len(self.mem_MILP_offline))
            load_CPU_nodes.append((
                    max(self.cpu_MILP_offline),
                    np.percentile(self.cpu_MILP_offline, 75),
                    np.percentile(self.cpu_MILP_offline, 50), 
                    np.percentile(self.cpu_MILP_offline, 25), 
                    min(self.cpu_MILP_offline)
                    )
            )
            labels.append(('MOF/'+'t:'+str(round(sum(self.time_MILP_offline)/len(self.time_MILP_offline), 2)) ))
        
            load_mem_nodes.append((
                max(self.mem_MILP_offline),
                np.percentile(self.mem_MILP_offline, 75),
                np.percentile(self.mem_MILP_offline, 50), 
                np.percentile(self.mem_MILP_offline, 25), 
                min(self.mem_MILP_online)
                )
            )
            load_links.append((
                    max(self.link_MILP_offline),
                    np.percentile(self.link_MILP_offline, 75),
                    np.percentile(self.link_MILP_offline, 50), 
                    np.percentile(self.link_MILP_offline, 25), 
                    min(self.link_MILP_offline)
                    )
            )
        
        if 'HOF' in approach:
            self.cpu_heu_offline_list.append(sum(self.cpu_heu_offline) / len(self.cpu_heu_offline))
            self.link_heu_offline_list.append(sum(self.link_heu_offline) / len(self.link_heu_offline))
            self.time_heu_offline_list.append(sum(self.time_heu_offline) / len(self.time_heu_offline))
            self.mem_heu_offline_list.append(sum(self.mem_heu_offline) / len(self.mem_heu_offline))
            load_CPU_nodes.append((
                    max(self.cpu_heu_offline),
                    np.percentile(self.cpu_heu_offline, 75),
                    np.percentile(self.cpu_heu_offline, 50), 
                    np.percentile(self.cpu_heu_offline, 25), 
                    min(self.cpu_heu_offline))
                    )
            labels.append(('HOF/'+'t:'+str(round(sum(self.time_heu_offline)/len(self.time_heu_offline), 2))))
            load_mem_nodes.append((
                    max(self.mem_heu_offline),
                    np.percentile(self.mem_heu_offline, 75),
                    np.percentile(self.mem_heu_offline, 50), 
                    np.percentile(self.mem_heu_offline, 25), 
                    min(self.mem_heu_offline))
                    )
            load_links.append((
                    max(self.link_heu_offline),
                    np.percentile(self.link_heu_offline, 75),
                    np.percentile(self.link_heu_offline, 50), 
                    np.percentile(self.link_heu_offline, 25), 
                    min(self.link_heu_offline))
                    )
        
        if 'HON' in approach:
            self.cpu_heu_online_list.append(sum(self.cpu_heu_online) / len(self.cpu_heu_online))
            self.link_heu_online_list.append(sum(self.link_heu_online) / len(self.link_heu_online))
            self.time_heu_online_list.append(sum(self.time_heu_online) / len(self.time_heu_online))
            self.mem_heu_online_list.append(sum(self.mem_heu_online) / len(self.mem_heu_online))
            load_CPU_nodes.append((
                    max(self.cpu_heu_online),
                    np.percentile(self.cpu_heu_online, 75),
                    np.percentile(self.cpu_heu_online, 50), 
                    np.percentile(self.cpu_heu_online, 25), 
                    min(self.cpu_heu_online))
                    )
            labels.append(('HON/'+'t:'+str(round(sum(self.time_heu_online)/len(self.time_heu_online), 2))))
            load_mem_nodes.append((
                    max(self.mem_heu_online),
                    np.percentile(self.mem_heu_online, 75),
                    np.percentile(self.mem_heu_online, 50), 
                    np.percentile(self.mem_heu_online, 25), 
                    min(self.mem_heu_online))
                    )
            load_links.append((
                    max(self.link_heu_online),
                    np.percentile(self.link_heu_online, 75),
                    np.percentile(self.link_heu_online, 50), 
                    np.percentile(self.link_heu_online, 25), 
                    min(self.link_heu_online))
                    )
            
        
        
        
        
        
        fig1, ax1 = plt.subplots()
        ax1.set_title('CPU load'+'/'+'user num:'+str(user_num)+'/'+'K shortest path:'+str(k)+'/'+'alpha:'+str(alpha)+'/batchSize:'+str(batch_size))
        if versus_chain:
            plt.xlabel('chains number')
        elif versus_user:
            plt.xlabel('chains number')
        plt.ylabel('cpu usage(%)')
        ax1.boxplot(load_CPU_nodes, labels=labels)
        for f in fomat_list:
            plt.savefig(self.input_cons.path_box_plot+'CPUcap_'+'usernum:'+str(user_num)+'_KSP:'+str(k)+'_alpah:'+str(alpha)+'_batchSize:'+str(batch_size)+f)
        if show:
            plt.show()
        plt.close()
        
        fig2, ax2 = plt.subplots()
        ax2.set_title('links load'+'/'+'user num:'+str(user_num)+'/'+'K shortest path:'+str(k)+'/'+'alpha:'+str(alpha)+'/batchSize:'+str(batch_size))
        if versus_chain:
            plt.xlabel('chains number')
        elif versus_user:
            plt.xlabel('chains number')
        plt.ylabel('bandwidth usage(%)')
        ax2.boxplot(load_links, labels=labels)
        for f in fomat_list:
            plt.savefig(self.input_cons.path_box_plot+'CPUcap_'+'usernum:'+str(user_num)+'_KSP:'+str(k)+'_alpah:'+str(alpha)+'_batchSize:'+str(batch_size)+f)
        if show:
            plt.show()
        plt.close()

        fig3, ax3 = plt.subplots()
        ax3.set_title('nodes memory load'+'/'+'user num:'+str(user_num)+'/'+'K shortest path:'+str(k)+'/'+'alpha:'+str(alpha)+'/batchSize:'+str(batch_size))
        if versus_chain:
            plt.xlabel('chains number')
        elif versus_user:
            plt.xlabel('chains number')
        plt.ylabel('memory usage(%)')
        ax3.boxplot(load_mem_nodes, labels=labels)
        for f in fomat_list:
            plt.savefig(self.input_cons.path_box_plot+'CPUcap_'+'usernum:'+str(user_num)+'_KSP:'+str(k)+'_alpah:'+str(alpha)+'_batchSize:'+str(batch_size)+f)
        if show:
            plt.show()
        plt.close()
        
        self.cpu_heu_online = []
        self.link_heu_online = []
        self.time_heu_online = []
        self.mem_heu_online = []
        
        self.cpu_heu_online_batch = []
        self.link_heu_online_batch = []
        self.time_heu_online_batch = []
        self.mem_heu_online_batch = []
        
        self.cpu_heu_offline = []
        self.link_heu_offline = []
        self.time_heu_offline = []
        self.mem_heu_offline = []
            
        self.cpu_heu_fully_batch = []
        self.link_heu_fully_batch = []
        self.time_heu_fully_batch = []
        self.mem_heu_fully_batch = []

        self.cpu_MILP_online = []
        self.link_MILP_online = []
        self.time_MILP_online = []
        self.mem_MILP_online = []

        self.cpu_MILP_batch_online = []
        self.link_MILP_batch_online = []
        self.time_MILP_batch_online = []
        self.mem_MILP_batch_online = []

        self.cpu_MILP_offline = []
        self.link_MILP_offline = []
        self.time_MILP_offline = []
        self.mem_MILP_offline = []
            
        
    def curve(self, approach, alpha, batch_size, k, user_list, chain_list, user_num, chain_num, format_list, show, versus_chain, versus_user):
        
        fig31, ax31 = plt.subplots()
        if versus_chain:
            # print(chain_list)
            # print(self.cpu_heu_offline_list)
            plt.xlabel('chains number')
            ax31.set_title('KSP:'+str(k)+'/'+'alpha:'+str(alpha)+'/batchSize:'+str(batch_size))
            if 'HOF' in approach:    
                plt.plot(chain_list, self.cpu_heu_offline_list, 'C2o', color='blue')
                plt.plot(chain_list, self.cpu_heu_offline_list, color='blue', label='HOF')
            if 'HFB' in approach:
                plt.plot(chain_list, self.cpu_heu_fully_batch_list, 'C2o', color='red')
                plt.plot(chain_list, self.cpu_heu_fully_batch_list, color='red', label='HFB')
            if 'HONB' in approach:
                plt.plot(chain_list, self.cpu_heu_online_batch_list, 'C2o', color='green')
                plt.plot(chain_list, self.cpu_heu_online_batch_list, color='green', label='HONB')
            if 'HON' in approach:
                plt.plot(chain_list, self.cpu_heu_online_list, 'C2o', color='m')
                plt.plot(chain_list, self.cpu_heu_online_list, color='m', label='HON')
            if 'MONB' in approach:
                plt.plot(chain_list, self.cpu_MILP_batch_online_list, 'C2o', color='black')
                plt.plot(chain_list, self.cpu_MILP_batch_online_list, color='black', label='MONB')
            if 'MON' in approach:
                plt.plot(chain_list, self.cpu_MILP_online_list, 'C2o', color='orange')
                plt.plot(chain_list, self.cpu_MILP_online_list, color='orange', label='MON')    
            if 'MOF' in approach:
                plt.plot(chain_list, self.cpu_MILP_offline_list, 'C2o', color='pink')
                plt.plot(chain_list, self.cpu_MILP_offline_list, color='pink', label='MOF')
                
            plt.ylabel('CPU usage(%)')
            plt.legend()
            plt.grid(True)
            if show:
                plt.show()
            for f in format_list:
                plt.savefig(self.input_cons.path_curve_versus_chain+'CPUvUSER_'+'cpuUsage_v_chians'+'_KSP:'+str(k)+'_alpah:'+str(alpha)+'_batchSize:'+str(batch_size)+f)
            plt.close()

        elif versus_user:
            plt.xlabel('users number')
            ax31.set_title('KSP:'+str(k)+'/'+'alpha:'+str(alpha)+'/batchSize:'+str(batch_size)+'/chains number:'+str(chain_num))
            
            if 'HOF' in approach:    
                plt.plot(user_list, self.cpu_heu_offline_list, 'C2o', color='blue')
                plt.plot(user_list, self.cpu_heu_offline_list, color='blue', label='HOF')
            if 'HFB' in approach:
                plt.plot(user_list, self.cpu_heu_fully_batch_list, 'C2o', color='red')
                plt.plot(user_list, self.cpu_heu_fully_batch_list, color='red', label='HFB')
            if 'HONB' in approach:
                plt.plot(user_list, self.cpu_heu_online_batch_list, 'C2o', color='green')
                plt.plot(user_list, self.cpu_heu_online_batch_list, color='green', label='HONB')
            if 'HON' in approach:
                plt.plot(user_list, self.cpu_heu_online_list, 'C2o', color='m')
                plt.plot(user_list, self.cpu_heu_online_list, color='m', label='HON')
            if 'MONB' in approach:
                plt.plot(user_list, self.cpu_MILP_batch_online_list, 'C2o', color='black')
                plt.plot(user_list, self.cpu_MILP_batch_online_list, color='black', label='MONB')
            if 'MON' in approach:
                plt.plot(user_list, self.cpu_MILP_online_list, 'C2o', color='orange')
                plt.plot(user_list, self.cpu_MILP_online_list, color='orange', label='MON')    
            if 'MOF' in approach:
                plt.plot(user_list, self.cpu_MILP_offline_list, 'C2o', color='pink')
                plt.plot(user_list, self.cpu_MILP_offline_list, color='pink', label='MOF')
            
            plt.ylabel('CPU usage(%)')
            plt.legend()
            plt.grid(True)
            if show:
                plt.show()
            for f in format_list:
                plt.savefig(self.input_cons.path_curve_versus_user+'CPUvUSER_'+'cpuUsage_v_usernum'+'_KSP:'+str(k)+'_alpah:'+str(alpha)+'_batchSize:'+str(batch_size)+'_chains:'+str(chain_num)+f)
            plt.close()

            
        fig32, ax32 = plt.subplots()
        if versus_chain:

            ax32.set_title('KSP:'+str(k)+'/'+'alpha:'+str(alpha)+'/batchSize:'+str(batch_size))
            
            if 'HOF' in approach:    
                plt.plot(chain_list, self.mem_heu_offline_list, 'C2o', color='blue')
                plt.plot(chain_list, self.mem_heu_offline_list, color='blue', label='HOF')
            if 'HFB' in approach:
                plt.plot(chain_list, self.mem_heu_fully_batch_list, 'C2o', color='red')
                plt.plot(chain_list, self.mem_heu_fully_batch_list, color='red', label='HFB')
            if 'HONB' in approach:
                plt.plot(chain_list, self.mem_heu_online_batch_list, 'C2o', color='green')
                plt.plot(chain_list, self.mem_heu_online_batch_list, color='green', label='HONB')
            if 'HON' in approach:
                plt.plot(chain_list, self.mem_heu_online_list, 'C2o', color='m')
                plt.plot(chain_list, self.mem_heu_online_list, color='m', label='HON')
            if 'MONB' in approach:
                plt.plot(chain_list, self.mem_MILP_batch_online_list, 'C2o', color='black')
                plt.plot(chain_list, self.mem_MILP_batch_online_list, color='black', label='MONB')
            if 'MON' in approach:
                plt.plot(chain_list, self.mem_MILP_online_list, 'C2o', color='orange')
                plt.plot(chain_list, self.mem_MILP_online_list, color='orange', label='MON')    
            if 'MOF' in approach:
                plt.plot(chain_list, self.mem_MILP_offline_list, 'C2o', color='pink')
                plt.plot(chain_list, self.mem_MILP_offline_list, color='pink', label='MOF')
            
            if versus_chain:
                plt.xlabel('chains number')
            elif versus_user:
                plt.xlabel('chains number')
            plt.ylabel('memory usage(%)')
            plt.legend()
            plt.grid(True)
            if show:
                plt.show()
            for f in format_list:
                plt.savefig(self.input_cons.path_curve_versus_chain+'memoryvUSER_'+'cpuUsage_v_usernum'+'_KSP:'+str(k)+'_alpah:'+str(alpha)+'_batchSize:'+str(batch_size)+f)
            plt.close()

        elif versus_user:
            ax32.set_title('KSP:'+str(k)+'/'+'alpha:'+str(alpha)+'/batchSize:'+str(batch_size))
            
            if 'HOF' in approach:    
                plt.plot(user_list, self.mem_heu_offline_list, 'C2o', color='blue')
                plt.plot(user_list, self.mem_heu_offline_list, color='blue', label='HOF')
            if 'HFB' in approach:
                plt.plot(user_list, self.mem_heu_fully_batch_list, 'C2o', color='red')
                plt.plot(user_list, self.mem_heu_fully_batch_list, color='red', label='HFB')
            if 'HONB' in approach:
                plt.plot(user_list, self.mem_heu_online_batch_list, 'C2o', color='green')
                plt.plot(user_list, self.mem_heu_online_batch_list, color='green', label='HONB')
            if 'HON' in approach:
                plt.plot(user_list, self.mem_heu_online_list, 'C2o', color='m')
                plt.plot(user_list, self.mem_heu_online_list, color='m', label='HON')
            if 'MONB' in approach:
                plt.plot(user_list, self.mem_MILP_batch_online_list, 'C2o', color='black')
                plt.plot(user_list, self.mem_MILP_batch_online_list, color='black', label='MONB')
            if 'MON' in approach:
                plt.plot(user_list, self.mem_MILP_online_list, 'C2o', color='orange')
                plt.plot(user_list, self.mem_MILP_online_list, color='orange', label='MON')    
            if 'MOF' in approach:
                plt.plot(user_list, self.mem_MILP_offline_list, 'C2o', color='pink')
                plt.plot(user_list, self.mem_MILP_offline_list, color='pink', label='MOF')
            
            if versus_chain:
                plt.xlabel('chains number')
            elif versus_user:
                plt.xlabel('chains number')
            plt.ylabel('memory usage(%)')
            plt.legend()
            plt.grid(True)
            if show:
                plt.show()
            for f in format_list:
                plt.savefig(self.input_cons.path_versus_chains+'memoryvUSER_'+'cpuUsage_v_usernum'+'_KSP:'+str(k)+'_alpah:'+str(alpha)+'_batchSize:'+str(batch_size)+'_users:'+str(user_num)+'_chains:'+str(chain_num)+f)
            plt.close()

        fig4, ax4 = plt.subplots()
        if versus_chain:
            ax4.set_title('KSP:'+str(k)+'/alpha:'+str(alpha)+'/batchSize:'+str(batch_size))
            
            if 'HOF' in approach:    
                plt.plot(chain_list, self.time_heu_offline_list, 'C2o', color='blue')
                plt.plot(chain_list, self.time_heu_offline_list, color='blue', label='HOF')
            if 'HFB' in approach:
                plt.plot(chain_list, self.time_heu_fully_batch_list, 'C2o', color='red')
                plt.plot(chain_list, self.time_heu_fully_batch_list, color='red', label='HFB')
            if 'HONB' in approach:
                plt.plot(chain_list, self.time_heu_online_batch_list, 'C2o', color='green')
                plt.plot(chain_list, self.time_heu_online_batch_list, color='green', label='HONB')
            if 'HON' in approach:
                plt.plot(chain_list, self.time_heu_online_list, 'C2o', color='m')
                plt.plot(chain_list, self.time_heu_online_list, color='m', label='HON')
            if 'MONB' in approach:
                plt.plot(chain_list, self.time_MILP_batch_online_list, 'C2o', color='black')
                plt.plot(chain_list, self.time_MILP_batch_online_list, color='black', label='MONB')
            if 'MON' in approach:
                plt.plot(chain_list, self.time_MILP_online_list, 'C2o', color='orange')
                plt.plot(chain_list, self.time_MILP_online_list, color='orange', label='MON')    
            if 'MOF' in approach:
                plt.plot(chain_list, self.time_MILP_offline_list, 'C2o', color='pink')
                plt.plot(chain_list, self.time_MILP_offline_list, color='pink', label='MOF')
            
            plt.xlabel('chains number')
            plt.ylabel('time (s)')
            plt.legend()
            plt.grid(True)
            if show:
                plt.show()
            for f in format_list:
                plt.savefig(self.input_cons.path_curve_versus_chain+'timevUSER_'+'cpuUsage_v_usernum'+'_KSP:'+str(k)+'_alpah:'+str(alpha)+'_batchSize:'+str(batch_size)+f)
            
            plt.close()
        elif versus_user:
            ax4.set_title('KSP:'+str(k)+'/alpha:'+str(alpha)+'/batchSize:'+str(batch_size))
            
            if 'HOF' in approach:    
                plt.plot(user_list, self.time_heu_offline_list, 'C2o', color='blue')
                plt.plot(user_list, self.time_heu_offline_list, color='blue', label='HOF')
            if 'HFB' in approach:
                plt.plot(user_list, self.time_heu_fully_batch_list, 'C2o', color='red')
                plt.plot(user_list, self.time_heu_fully_batch_list, color='red', label='HFB')
            if 'HONB' in approach:
                plt.plot(user_list, self.time_heu_online_batch_list, 'C2o', color='green')
                plt.plot(user_list, self.time_heu_online_batch_list, color='green', label='HONB')
            if 'HON' in approach:
                plt.plot(user_list, self.time_heu_online_list, 'C2o', color='m')
                plt.plot(user_list, self.time_heu_online_list, color='m', label='HON')
            if 'MONB' in approach:
                plt.plot(user_list, self.time_MILP_batch_online_list, 'C2o', color='black')
                plt.plot(user_list, self.time_MILP_batch_online_list, color='black', label='MONB')
            if 'MON' in approach:
                plt.plot(user_list, self.time_MILP_online_list, 'C2o', color='orange')
                plt.plot(user_list, self.time_MILP_online_list, color='orange', label='MON')    
            if 'MOF' in approach:
                plt.plot(user_list, self.time_MILP_offline_list, 'C2o', color='pink')
                plt.plot(user_list, self.time_MILP_offline_list, color='pink', label='MOF')
            
            if versus_chain:
                plt.xlabel('users number')
            plt.ylabel('time (s)')
            plt.legend()
            plt.grid(True)
            if show:
                plt.show()
            for f in format_list:
                plt.savefig(self.input_cons.versus_chain+'timevUSER_'+'cpuUsage_v_usernum'+'_KSP:'+str(k)+'_alpah:'+str(alpha)+'_batchSize:'+str(batch_size)+'_chains:'+str(chains_num)+f)
            
            plt.close()
            
        fig5, ax5 = plt.subplots()
        if versus_chain:
            ax5.set_title('KSP:'+str(k)+'/'+'alpha:'+str(alpha)+'/batchSize:'+str(batch_size))
            
            if 'HOF' in approach:    
                plt.plot(chain_list, self.link_heu_offline_list, 'C2o', color='blue')
                plt.plot(chain_list, self.link_heu_offline_list, color='blue', label='HOF')
            if 'HFB' in approach:
                plt.plot(chain_list, self.link_heu_fully_batch_list, 'C2o', color='red')
                plt.plot(chain_list, self.link_heu_fully_batch_list, color='red', label='HFB')
            if 'HONB' in approach:
                plt.plot(chain_list, self.link_heu_online_batch_list, 'C2o', color='green')
                plt.plot(chain_list, self.link_heu_online_batch_list, color='green', label='HONB')
            if 'HON' in approach:
                plt.plot(chain_list, self.link_heu_online_list, 'C2o', color='m')
                plt.plot(chain_list, self.link_heu_online_list, color='m', label='HON')
            if 'MONB' in approach:
                plt.plot(chain_list, self.link_MILP_batch_online_list, 'C2o', color='black')
                plt.plot(chain_list, self.link_MILP_batch_online_list, color='black', label='MONB')
            if 'MON' in approach:
                plt.plot(chain_list, self.link_MILP_online_list, 'C2o', color='orange')
                plt.plot(chain_list, self.link_MILP_online_list, color='orange', label='MON')    
            if 'MOF' in approach:
                plt.plot(chain_list, self.link_MILP_offline_list, 'C2o', color='pink')
                plt.plot(chain_list, self.link_MILP_offline_list, color='pink', label='MOF')
            
            plt.xlabel('chains number')
            plt.ylabel('bandwidth usage (%)')
            plt.legend()
            plt.grid(True)
            if show:
                plt.show()
            for f in format_list:        
                plt.savefig(self.input_cons.path_curve_versus_chain+'bandwidthvUSER_'+'cpuUsage_v_usernum'+'_KSP:'+str(k)+'_alpah:'+str(alpha)+'_batchSize:'+str(batch_size)+f)
            
            plt.close()
        elif versus_user:
            ax5.set_title('KSP:'+str(k)+'/'+'alpha:'+str(alpha)+'/batchSize:'+str(batch_size))
            
            if 'HOF' in approach:    
                plt.plot(user_list, self.link_heu_offline_list, 'C2o', color='blue')
                plt.plot(user_list, self.link_heu_offline_list, color='blue', label='HOF')
            if 'HFB' in approach:
                plt.plot(user_list, self.link_heu_fully_batch_list, 'C2o', color='red')
                plt.plot(user_list, self.link_heu_fully_batch_list, color='red', label='HFB')
            if 'HONB' in approach:
                plt.plot(user_list, self.link_heu_online_batch_list, 'C2o', color='green')
                plt.plot(user_list, self.link_heu_online_batch_list, color='green', label='HONB')
            if 'HON' in approach:
                plt.plot(user_list, self.link_heu_online_list, 'C2o', color='m')
                plt.plot(user_list, self.link_heu_online_list, color='m', label='HON')
            if 'MONB' in approach:
                plt.plot(user_list, self.link_MILP_batch_online_list, 'C2o', color='black')
                plt.plot(user_list, self.link_MILP_batch_online_list, color='black', label='MONB')
            if 'MON' in approach:
                plt.plot(user_list, self.link_MILP_online_list, 'C2o', color='orange')
                plt.plot(user_list, self.link_MILP_online_list, color='orange', label='MON')    
            if 'MOF' in approach:
                plt.plot(user_list, self.link_MILP_offline_list, 'C2o', color='pink')
                plt.plot(user_list, self.link_MILP_offline_list, color='pink', label='MOF')
            
            plt.xlabel('users number')
            plt.ylabel('bandwidth usage (%)')
            plt.legend()
            plt.grid(True)
            if show:
                plt.show()
            for f in format_list:        
                plt.savefig(self.input_cons.path_curve_versus_user+'bandwidthvUSER_'+'cpuUsage_v_usernum'+'_KSP:'+str(k)+'_alpah:'+str(alpha)+'_batchSize:'+str(batch_size)+'_users:'+str(user_num)+'_chains:'+str(chain_num)+f)
            
            plt.close()
            
        self.cpu_heu_online_batch_list = []
        self.link_heu_online_batch_list = []
        self.time_heu_online_batch_list = []
        self.mem_heu_online_batch_list = []

        self.cpu_heu_fully_batch_list = []
        self.link_heu_fully_batch_list = []
        self.time_heu_fully_batch_list = []
        self.mem_heu_fully_batch_list = []
                
        self.cpu_MILP_online_list = []
        self.link_MILP_online_list = []
        self.time_MILP_online_list = []
        self.mem_MILP_online_list = []
        
        self.cpu_MILP_batch_online_list = []
        self.link_MILP_batch_online_list = []
        self.time_MILP_batch_online_list = []
        self.mem_MILP_batch_online_list = []
        
        self.cpu_heu_offline_list = []
        self.link_heu_offline_list = []
        self.time_heu_offline_list = []
        self.mem_heu_offline_list = []
        
        self.cpu_heu_online_list = []
        self.link_heu_online_list = []
        self.time_heu_online_list = []
        self.mem_heu_online_list = []
        
        self.cpu_MILP_offline_list = []
        self.link_MILP_offline_list = []
        self.time_MILP_offline_list = []
        self.mem_MILP_offline_list = []
        