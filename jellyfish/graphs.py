import networkx as nx
import fnss

def jellyfish(n, degree, num_hosts):
    """
    Generates a Jellyfish graph

    Parameters
    ----------
    n: int
      Number of switches
    
    degree: int
      degree for each switch (# of ports)
      Called "k" in jellyfish paper

    num_hosts: int
      number of edges dedicated to hosts per switch. Called "r" in jellyfish paper
      (k - r edges per switch go to other switches).

    Returns
    -------
    networkx.Graph
      A jellyfish graph
    """

    # TODO: implement this
    raise Exception("not implemented")

def fat_tree(k):
    """
    Generates a fat tree topology using: https://fnss.readthedocs.io/en/latest/apidoc/generated/fnss.topologies.datacenter.fat_tree_topology.html
    
    Parameters
    ----------
    k: int
      Number of ports per switch

    Returns
    -------
    fnss.DatacenterTopology
    """
    
    # Hacky patch to get fnss to work with networkx 2.3. a better
    # patch is submitted to fnss https://github.com/fnss/fnss/pull/27
    fnss.DatacenterTopology.node = property(lambda self: self.nodes)
    
    return fnss.fat_tree_topology(k)

def complete(n):
    """
    Generates a complete graph
    
    Parameters
    ----------
    n: int
      Number of nodes

    Returns
    -------
    networkx.Graph
      A complete graph
    """
    return nx.complete_graph(n)
