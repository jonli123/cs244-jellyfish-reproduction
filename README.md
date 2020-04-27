# How to Run:

Everything is consistent with the implementation guidelines provided in the class doc

Before running any of the make commands, make sure to start a pox controller with
```
~/pox/pox.py --verbose openflow.spanning_tree --no-flood --hold-down openflow.discovery forwarding.l2_learning
```

In order to generate figures:
```
sudo make figures
```
Figure generation has a cache: .npy files are saved and loaded in some functions. 
These functions are: 
```
def figure_1c_mininet(filename)
def table_1(filename)
```
If you want to run these functions doing the full mininet simluation, you must delete the following files
```
fat_results.npy
jelly_results.npy
```
To make the table_1 figure and
```
jelly_bins.npy
fat_tree_bins.npy
```
To make the figure_1c_mininet figure.

In order to run tests:
```
make
```
The fourth test may take a significant amount of time to run if the pings are spotty. 

Logging is turned on for all functions.

Scratchwork was done inside a jupyter notebook in
```
notebooks/Graph Implementations.ipynb
```

