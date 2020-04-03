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
                hosts = [n for n,d in G.nodes.data() if d.get('type') == 'host']
                self.assertEqual(len(hosts), n*r)

    def test_correct_degree(self):
        for n in range(12,20):
            for r in range(4):
                G = jellyfish.graphs.jellyfish(n, degree=r+2, num_hosts=r)
                switches = [n for n,d in G.nodes.data() if d.get('type') == 'switch']
                for s in switches:
                    self.assertEqual(G.degree[s], r+2)
                
if __name__ == '__main__':
    unittest.main()
