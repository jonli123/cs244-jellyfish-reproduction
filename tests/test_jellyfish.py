import unittest
import jellyfish

class TestJellyfishGenerator(unittest.TestCase):
    """Some very basic sanity checks for a Jellyfish graph"""
    
    def test_correct_number_switches(self):
        for n in range(3,10):
            G = jellyfish.graphs.jellyfish(n,degree=2,num_hosts=0)
            self.assertEqual(len(G.nodes), n)

    def test_correct_number_hosts(self):
        for n in range(12,20):
            for r in range(4):
                G = jellyfish.graphs.jellyfish(n, degree=r+2, num_hosts=r)
                
                # It'll useful to be able to distinguish hosts and switches
                # for the mininet section. You can add data to a node when creating it.
                # e.g.
                #  G = nx.Graph()
                #  G.add_node(1, type='host')
                # Check out the networkx documentation for more information.
                hosts = [n for n,d in G.nodes.data() if d.get('type') == 'host']
                
                self.assertEqual(len(hosts), n*r)

    def test_correct_degree(self):
        for n in range(12,20):
            for r in range(4):
                G = jellyfish.graphs.jellyfish(n, degree=r+2, num_hosts=r)
                
                # See above comment about adding data to nodes.
                switches = [n for n,d in G.nodes.data() if d.get('type') == 'switch']
                for s in switches:
                    self.assertIn(G.degree[s], [r+1, r+2])
                
if __name__ == '__main__':
    unittest.main()
