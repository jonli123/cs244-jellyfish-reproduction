# How to Run:

Everything is consistent with the implementation guidelines provided in the class doc

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
