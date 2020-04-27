import click
import jellyfish
import networkx as nx
import matplotlib.pyplot as plt

@click.group()
def main():
    pass

def make_graph(graph, n, k, r):
    if graph == 'jellyfish':
        if n is None:
            raise click.UsageError("Missing option '-n'")
        if k is None:
            raise click.UsageError("Missing option '-k'")
        if r is None:
            raise click.UsageError("Missing option '-r'")

        return jellyfish.graphs.jellyfish(n,k,r)
    elif graph == 'complete':
        if n is None:
            raise click.UsageError("Missing option '-n'")

        return jellyfish.graphs.complete(n)
    elif graph == 'fat_tree':
        if k is None:
            raise click.UsageError("Missing option '-k'")

        return jellyfish.graphs.fat_tree(k)
    else:
        raise Exception('unknown graph type %s, must be one of jellyfish, complete, fat_tree'%(graph))


@main.command(help='Draw a graph')
@click.option('-n', required=False, help="Number of switches", type=int)
@click.option('-k', required=False, help="Degree of switch", type=int)
@click.option('-r', required=False, help="Number of servers per switch", type=int)
@click.option('--graph', required=True, help="Type of graph to draw", type=str)
@click.argument('filename')
def draw(n,k,r,filename,graph):
    G = make_graph(graph, n, k, r)
    if graph == 'jellyfish':
        node_color_array = ['#1f78b4']*n + ['#b41f96']*n
        nx.draw_networkx(G,node_color=node_color_array,node_size=25,with_labels=False)
        plt.savefig(filename)
    elif graph == 'complete':
        nx.draw(G)
        plt.savefig(filename)
    elif graph == 'fat_tree':
        G = jellyfish.graphs.fat_tree(4)
        node_color_array = ['#1f78b4']*len(G.nodes)
        node_color_array[-16:] = ['#b41f96']*16
        nx.draw_networkx(G,node_color=node_color_array,node_size=25,with_labels=False)
        plt.savefig(filename)
    else:
        raise Exception('unknown graph type %s, must be one of jellyfish, complete, fat_tree'%(graph))

@main.command(help='Start a mininet interpreter for a graph')
@click.option('-n', required=False, help="Number of switches", type=int)
@click.option('-k', required=False, help="Degree of switch", type=int)
@click.option('-r', required=False, help="Number of servers per switch", type=int)
@click.option('--graph', required=True, help="Type of graph to draw", type=str)
def mn(n,k,r,graph):
    G = make_graph(graph, n, k, r)
    jellyfish.mininet.run(G)

@main.command(help="Make figure 1c (path lengths)")
@click.argument('filename')
def figure_1c(filename):
    jellyfish.figures.figure_1c(filename)

@main.command(help="Make figure 2a (bisection bandwidth)")
@click.argument('filename')
def figure_2a(filename):
    jellyfish.figures.figure_2a(filename)

@main.command(help="Make figure 2b (equipment cost)")
@click.argument('filename')
def figure_2b(filename):
    jellyfish.figures.figure_2b(filename)

@main.command(help="Make figure 9 (ecmp)")
@click.argument('filename')
def figure_9(filename):
    jellyfish.figures.figure_9(filename)

@main.command(help="Make figure 1c (path lengths) using mininet")
@click.argument('filename')
def figure_1c_mininet(filename):
    jellyfish.figures.figure_1c_mininet(filename)

@main.command(help="Make table 1 (TCP throughput)")
@click.argument('filename')
def table_1(filename):
    jellyfish.figures.table_1(filename)
