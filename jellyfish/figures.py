import matplotlib.pyplot as plt
import jellyfish.graphs as graphs
import networkx as nx
from mininet.log import lg
import mininet.clean
from mininet.cli import CLI
import jellyfish
import numpy as np
import time
import os.path
import re
from itertools import islice
import random
from collections import defaultdict


def figure_1c(filename):
    large_jellyfish = nx.random_regular_graph(7, 98) #jellyfish(98,14,7) #nx.random_regular_graph(7, 98)#jellyfish(98,14,7)
    large_fattree = graphs.fat_tree(14)

    path_lengths = {}
    path_lengths['Jellyfish'] = np.array([0]*6)
    path_lengths['Fat-tree'] = np.array([0]*6)

    length_dict = dict(nx.shortest_path_length(large_jellyfish))
    for n in large_jellyfish.nodes:
        for m in large_jellyfish.nodes:
            if n != m:
                length = length_dict[n][m]
                if length == 12:
                    print(n,m)
                    print()
                path_lengths['Jellyfish'][length+1] += 1

    length_dict = dict(nx.shortest_path_length(large_fattree))
    for n in large_fattree.nodes:
        for m in large_fattree.nodes:
            if n != m:
                length = length_dict[n][m]
                path_lengths['Fat-tree'][length-1] += 1

    path_lengths['Jellyfish'] = [x/sum(path_lengths['Jellyfish']) for x in path_lengths['Jellyfish']]
    path_lengths['Fat-tree'] = [x/sum(path_lengths['Fat-tree']) for x in path_lengths['Fat-tree']]
    width = 0.35
    plt.bar(np.arange(2,7) - width/2,path_lengths['Jellyfish'][1:], width=width,label='Jellyfish')
    plt.bar(np.arange(2,7) + width/2,path_lengths['Fat-tree'][1:], width=width,label='Fat-tree')

    plt.yticks(np.arange(0, 1.1, step=0.1))
    plt.ylabel('Fraction of Server Pairs')
    plt.xlabel('Path length')
    plt.legend()

    plt.grid(b=True,linestyle=':')

    plt.savefig(filename)

def figure_2a(filename):
    def bisection_bandwidth(n,r):
        return (1 - np.sqrt(np.log(2)/r)) * r/2 * n/2

    def construct_line(N,k,r_range):
        line_x = []
        line_y = []
        for r in range(r_range[0],r_range[1]):
            bi_band = bisection_bandwidth(N,r)
            line_rate_bandwidth = (N * (k-r))/2 # The number of connections from servers to switches divided by 2
            num_servers = line_rate_bandwidth*2
            line_y.append(bi_band/line_rate_bandwidth)
            line_x.append(num_servers)
        return line_x, line_y

    jelly_labels = ['Jellyfish; N=2880; k=48', 'Jellyfish; N=1280; k=32','Jellyfish; N=720; k=24']
    fat_labels = ['Fat-tree; N=2880; k=48', 'Fat-tree; N=1280; k=32','Fat-tree; N=720; k=24']
    N = [2880,1280,720]
    k = [48,32,24]
    r_range = [(20,40),(11,27),(8,21)]
    labels = zip(jelly_labels,fat_labels)
    markers = ['s','o','^']
    params = zip(N,k,r_range,labels,markers)

    for N,k,r_range,label,marker in params:
        line_x, line_y = construct_line(N,k,r_range)
        #     print(line_x[0],line_x[-1])
        #     print(line_y[0],line_y[-1])
        #     print(len(line_x))
        fat_tree_servers = np.power(k,3)/4
        fat_tree_bandwidth_normalized = (np.power(k,3)/8)/(np.power(k,3)/4/ 2)
        plt.plot(line_x, line_y,label=label[0], marker=marker, markersize=5, linewidth=2)
        plt.plot(fat_tree_servers,fat_tree_bandwidth_normalized,label=label[1], marker=marker, markersize=12, linewidth=2)

    plt.xticks(np.arange(0, 80001, step=10000), labels=np.arange(0, 81, step=10))
    plt.yticks(np.arange(0.2, 1.7, step=0.2))
    plt.grid(b=True,linestyle=':')
    plt.xlim(0,80000)
    plt.ylim(0.2,1.6)
    plt.ylabel('Normalized Bisection Bandwidth')
    plt.xlabel('Number of Servers in Thousands')
    plt.legend()
    plt.savefig(filename)

def figure_2b(filename):
    jelly_labels = ['Jellyfish; 24 ports', 'Jellyfish; 32 ports', 'Jellyfish; 48 ports', 'Jellyfish; 64 ports']
    fat_label = 'Fat-tree; {24,32,48,64} ports'
    num_ports = np.array([24,32,48,64])
    r = np.array([19,25,36,47])

    params = zip(num_ports,r,jelly_labels)

    for k,r,label in params:
        num_servers = np.arange(0,80001,step=10000)
        cost = k * num_servers / (k-r)
        plt.plot(num_servers,cost,label=label)


    fat_servers = np.power(num_ports,3)/4
    fat_ports = num_ports*(np.power(num_ports/2,2) + num_ports * num_ports)

    plt.scatter(fat_servers,fat_ports,marker='o', label=fat_label)

    plt.xticks(np.arange(0, 80001, step=10000), labels=np.arange(0, 81, step=10))
    plt.yticks(np.arange(0, 400001, step=50000), labels=np.arange(0, 401, step=50))
    plt.grid(b=True,linestyle=':')
    plt.xlim(0,80000)
    plt.ylim(0,400000)
    plt.ylabel('Equipment Cost [#Ports in Thousands]')
    plt.xlabel('Number of Servers in Thousands')
    plt.legend()
    plt.savefig(filename)

def figure_9(filename):

    def eight_way(paths,count):
        #print(len(paths))
        if len(paths) <= 8:
            path = random.choice(paths)
        else:
            path = random.choice(paths[:8])
        #print(path)
        for i in range(len(path)-1):
            if (path[i],path[i+1]) in count:
                count[(path[i],path[i+1])] += 1

    def sixty_four_way(paths,count):
        #print(len(paths))
        if len(paths) <= 64:
            path = random.choice(paths)
        else:
            path = random.choice(paths[:8])
        #print(path)
        for i in range(len(path)-1):
            if (path[i],path[i+1]) in count:
                count[(path[i],path[i+1])] += 1
    large_jellyfish = jellyfish.graphs.jellyfish(98,14,7)
    arr_sol = []

    edge_pairs = list(large_jellyfish.edges)+[(n2,n1) for (n1,n2) in large_jellyfish.edges]
    count_eight = dict((e,0) for e in edge_pairs)
    total_eight = 0
    for n1 in large_jellyfish.nodes:
        n2 = np.random.choice(list(large_jellyfish.nodes))
        if n1 != n2:
            paths = nx.all_shortest_paths(large_jellyfish,source=n1,target=n2)
            eight_way(list(paths),count_eight)
            total_eight += 1

    count_sixty = dict((e,0) for e in edge_pairs)
    total_sixty = 0
    for n1 in large_jellyfish.nodes:
        n2 = np.random.choice(list(large_jellyfish.nodes))
        if n1 != n2:
            paths = nx.all_shortest_paths(large_jellyfish,source=n1,target=n2)
            sixty_four_way(list(paths),count_sixty)
            total_sixty += 1

    def k_shortest_paths(G, source, target, k, weight=None):
        return list(islice(nx.shortest_simple_paths(G, source, target, weight=weight), k))

    count_eight_shortest = dict((e,0) for e in edge_pairs)
    total_eight_shortest = 0
    for n1 in large_jellyfish.nodes:
        n2 = np.random.choice(list(large_jellyfish.nodes))
        if n1 != n2:
            paths = k_shortest_paths(large_jellyfish, n1, n2, 8)
            eight_way(list(paths),count_eight_shortest)
            total_eight_shortest += 1

    plt.plot(sorted(count_eight_shortest.values()), label="8-way Shortest Paths")
    plt.plot(sorted(count_sixty.values()), label="64-way ECMP")
    plt.plot(sorted(count_eight.values()), label="8-way ECMP")
    plt.legend()
    plt.savefig(filename)

def figure_1c_mininet(filename):
    # TODO: implement this
    lg.setLogLevel('info')

    if not os.path.isfile('jelly_bins.npy'):
        jelly = jellyfish.graphs.jellyfish(8, 4, 2)
        mininet.clean.cleanup()
        net = jellyfish.mininet.make_mininet(jelly)
        time.sleep(4)
        net.start()
        time.sleep(4)
        net.waitConnected()
        data = net.pingAllFull()
        net.stop()
        arr_ping = []
        for _,_,t in data:
            rtt = t[3]
            print(rtt)
            arr_ping.append(rtt)

        jelly_plot = [0]*5
        for p in arr_ping:
            if p < 150:
                jelly_plot[int(p/30)] += 1
        jelly_plot = [x/sum(jelly_plot) for x in jelly_plot]
        np.save('jelly_bins.npy', jelly_plot)
    else:
        jelly_plot = np.load('jelly_bins.npy')

    if not os.path.isfile('fat_tree_bins.npy'):
        fat_tree = jellyfish.graphs.fat_tree(6) #jellyfish.graphs.jellyfish(16, 4, 1)
        mininet.clean.cleanup()
        net = jellyfish.mininet.make_mininet(fat_tree)
        time.sleep(4)
        net.start()
        time.sleep(4)
        net.waitConnected()
        data = net.pingAllFull()
        net.stop()
        arr_ping = []
        for _,_,t in data:
            rtt = t[3]
            print(rtt)
            arr_ping.append(rtt)

        bin_plot = [0]*5
        for p in arr_ping:
            if p < 150:
                bin_plot[int(p/30)] += 1
        bin_plot = [x/sum(bin_plot) for x in bin_plot]
        np.save('fat_tree_bins.npy', bin_plot)
    else:
        bin_plot = np.load('fat_tree_bins.npy')


    width = 0.35
    plt.bar(np.arange(2,7) - width/2,jelly_plot, width=width,label='Jellyfish')

    plt.bar(np.arange(2,7) + width/2,bin_plot, width=width,label='Fat-tree')
    plt.yticks(np.arange(0, 1.1, step=0.1))
    plt.ylabel('Fraction of Server Pairs')
    plt.xlabel('Path length')
    plt.legend()
    plt.grid(b=True,linestyle=':')
    #plt.hist(arr_ping,bins=5,range=(0,150))
    plt.savefig(filename)


# def table_1(filename):
#     graph = jellyfish.graphs.fat_tree(2)
#     mininet.clean.cleanup()
#     net = jellyfish.mininet.make_mininet(graph)
#     net.start()
#     #dumpNodeConnections(net.hosts)
#     net.waitConnected()
#     results = {}
#     port = 5000
#     for host1 in net.hosts:
#         host2 = host1
#         while host2 == host1:
#             host2 = random.choice(net.hosts)
#         host2.cmd('iperf -s -p ' + str(port) + ' -1 &')
#         result = host1.cmd('iperf -c ' + host2.IP() + ' -p ' + str(port))
#         host_pair = (host1.name, host2.name)
#         results[host_pair] = result
#         port += 1
#         print(result)
#     net.stop()

def table_1(filename):
    lg.setLogLevel('info')
    fat_results = {}
    jelly_results = {}
    if not os.path.isfile('fat_results.npy'):
        jelly = jellyfish.graphs.fat_tree(10)
        mininet.clean.cleanup()
        net = jellyfish.mininet.make_mininet(jelly)
        net.start()
        net.waitConnected()
        port = 2000
        for host in net.hosts:
            client = host
            while host == client:
                client = random.choice(net.hosts)
            client.cmd('iperf -s -p ' + str(port) + ' -1 &')
            val = host.cmd('iperf -c ' + client.IP() + ' -p ' + str(port))
            port += 1
            host_pair = (host.name, client.name)
            fat_results[host_pair] = val
        net.stop()
        np.save('fat_results.npy',fat_results)
    else:
       fat_results = np.load('fat_results.npy',allow_pickle=True).item()

    if not os.path.isfile('jelly_results.npy'):
        #lg.setLogLevel('info')
        jelly = jellyfish.graphs.jellyfish(98, 14, 7)
        mininet.clean.cleanup()
        net = jellyfish.mininet.make_mininet(jelly)
        net.start()
        net.waitConnected()
        port = 5000
        for host in net.hosts:
            client = host
            while host == client:
                client = random.choice(net.hosts)
            client.cmd('iperf -s -p ' + str(port) + ' -1 &')
            val = host.cmd('iperf -c ' + client.IP() + ' -p ' + str(port))
            port += 1
            host_pair = (host.name, client.name)
            jelly_results[host_pair] = val
        net.stop()
        np.save('jelly_results.npy',jelly_results)
    else:
       jelly_results = np.load('jelly_results.npy',allow_pickle=True).item()

    speed_arr = []
    for value in fat_results.values():
        speed = re.findall(r'(\d+.\d+) \wbits\/sec', value)
        if speed:
            speed_arr.append(float(speed[0]))
    fat_avg = sum(speed_arr)/len(speed_arr)

    speed_arr = []
    for value in jelly_results.values():
        speed = re.findall(r'(\d+.\d+) \wbits\/sec', value)
        if speed:
            speed_arr.append(float(speed[0]))
    jelly_avg = sum(speed_arr)/len(speed_arr)

    with open(filename, 'a') as f:
        f.write('Congestion control\t Fat-Tree ECMP\t Jellyfish ECMP\n')
        f.write('TCP 1 Flow\t '+ str(10*fat_avg) + '\t' + str(10*jelly_avg) +'\n')
