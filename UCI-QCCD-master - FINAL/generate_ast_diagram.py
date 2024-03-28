import ast
import pprint
import networkx as nx  
import matplotlib.pyplot as plt  
import graphviz as gv
from graphviz import Digraph, Graph
""" General in-built Python Libraries """
import sys 
# from astmonkey import visitors, transformers # astmonkey is a set of tools to 
# play with Python AST.
# from astmonkey.visitors import GraphNodeVisitor
#import astor # astor is designed to allow easy manipulation of Python source 
# via the AST
from _ast import AST
import astunparse # An AST unparser for Python.
#import astpretty # Pretty print the output of python stdlib ast.parse. 
# astpretty is intended to be a replacement for ast.dump.

# Using GraphViz
def visit(node, nodes, pindex, g):
    """ Function to visit the nodes of the AST """

    print(f"pindex: {pindex}")
    
    name = str(type(node).__name__)
    print(f"name:{name}")
    
    index = len(nodes)
    print(f"index: {index}")

    nodes.append(index)
    print(f"nodes: {nodes}")

    g.node(str(index), name)
    print(f"g: {g}")

    if index != pindex: # check to see if there is  
        g.edge(str(index), str(pindex))
    
    for n in ast.iter_child_nodes(node):
        visit(n, nodes, index, g) # recursively traverse the AST to go over the nodes and register them into the graph



# (sample2_type1_v1, sample2_type1_v1), (sample2_type2_v1, sample2_type3_v1) 
# (sample4_type1_v1, sample4_type1_v1), (sample4_type2_v1, sample4_type3_v1)

graph_1_file_url = '/home/samyaknj/Research/UCI Quantum Code Clone Detection Project/visualize_ast.py'
with open(graph_1_file_url, 'r') as fin1:
    src1 = fin1.read()

"""
graph_2_file_url = '/home/samyaknj/Research/UCI Quantum Code Clone Detection Project/Dataset/sample4/sample4_type3_v1.py'
with open(graph_2_file_url, 'r') as fin2:
    src2 = fin2.read()
"""
node1 = ast.parse(src1)
#node2 = ast.parse(src2)


graph1 = Digraph(format = "png") # declaring GraphViz Graph
visit(node1, [], 0, graph1)
graph1.render("sample4_type1_v1") # renders the graph obtained

"""
graph2 = Digraph(format = "png") # declaring GraphViz Graph
visit(node2, [], 0, graph2)
graph2.render("sample4_type3_v1") # renders the grapp obtained
"""
