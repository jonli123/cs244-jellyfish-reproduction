import unittest
import jellyfish
from mininet.log import lg
import mininet.clean

class TestRouting(unittest.TestCase):

    def test_jellyfish_hosts_reachable(self):
        """
        Create a jellyfish network and check that all hosts can ping each other.
        """

        # You can uncomment this to have mininet print out more debugging information
        # lg.setLogLevel('info')

        mininet.clean.cleanup()
        
        # Some hints for this:
        # * The Mininet waitConnected() method waits until all switches connect
        #   to a controller, which helps with test reliability.
        # * The Mininet pingAll() method runs a ping between all hosts and
        #   returns the percentage of packet loss. You can assert that this is zero
        # * If this fails every once in a while because pox hasn't set up routes,
        #   that's not ideal but acceptable.
        raise Exception("Not implemented")
        
if __name__ == '__main__':
    unittest.main()
