.PHONY: all
all: test figures/figure_1a.png figures/figure_1b.png figures/figure_1c.png figures/figure_2a.png figures/figure_2b.png figures/figure_9.png figures/figure_1c_mininet.png figures/table_1.txt

.PHONY: test
test:
# Mininet requires running as root
	sudo python tests/test_routing.py
	python tests/test_jellyfish.py

figures/figure_1a.png:
	jellyfish draw --graph='fat_tree' -k 4 figures/figure_1a.png

figures/figure_1b.png:
	jellyfish draw --graph='jellyfish' -n 16 -k 4 -r 2 figures/figure_1b.png

figures/figure_1c.png:
	jellyfish figure_1c figures/figure_1c.png

figures/figure_2a.png:
	jellyfish figure_2a figures/figure_2a.png

figures/figure_2b.png:
	jellyfish figure_2b figures/figure_2b.png

figures/figure_9.png:
	jellyfish figure_9 figures/figure_9.png

figures/figure_1c_mininet.png:
	jellyfish figure_1c_mininet figures/figure_1c_mininet.png

figures/table_1.txt:
	jellyfish table_1 figures/table_1.txt
