"""
Final Working Script to be used for Experiments. 

Converts input given as Path to Code file into a NetworkX graph that can be used by the 
SGI algorithm.
Path to Pyton code file --> Extract AST of the Python code --> Visit AST such that a NetworkX grapoh is generated

References: 
- https://stackoverflow.com/questions/73171700/subgraph-isomorphism-in-networkx-graphs-from-python-asts
"""

# Imports
import ast
import matplotlib.pyplot as plt
import graphviz as gv  # Used `pip install graphviz` to install graphviz
from graphviz import Digraph, Graph
import pydot
import networkx as nx
import pydotplus
import sys
import os
from networkx.drawing.nx_agraph import write_dot, graphviz_layout
import argparse


class GetNXgraphFromAST(ast.NodeVisitor):
    def __init__(self):
        self.stack = []
        self.graph = nx.Graph()

    def generic_visit(self, stmt):
        node_name = stmt
        parent_name = None

        if self.stack:
            parent_name = self.stack[-1]

        self.stack.append(node_name)
        self.graph.add_node(node_name)

        if parent_name:
            self.graph.add_edge(node_name, parent_name)

        super(self.__class__, self).generic_visit(stmt)
        self.stack.pop()


def get_code_from_storage(file_url):
    """
    Function to get Code file of a given file_url from the Storage
    Args:
        - file_url
    Returns:
        - Code file
    """
    with open(file_url, "r") as fin:
        srcCode = fin.read()
    fin.close()
    return srcCode


def parse_ast_to_networkx_graph(nodes):
    graph = nx.Graph()
    # nodes = ast.parse(src_Code)
    for node in ast.walk(nodes):
        for field, value in ast.iter_fields(node):
            if isinstance(value, ast.AST):
                graph.add_edge(node, value)
            elif isinstance(value, list):
                for item in value:
                    if isinstance(item, ast.AST):
                        graph.add_edge(node, item)

    return graph


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--folder", help="the folder path of Graph-SubGraph Test Codes", type=str
    )
    args = parser.parse_args()

    """ 
    The Pieces of code whose AST needs to be generated
    """
    # Larger Code = Target Graph = Main Graph
    G1_file_url = os.path.join(args.folder, "test_graph_code.py")
    src_G1 = get_code_from_storage(G1_file_url)

    # Smaller Code = Graph to Embed = Sub-Graph
    G2_file_url = os.path.join(args.folder, "test_subgraph_code.py")
    src_G2 = get_code_from_storage(G2_file_url)

    NXGraph_G1 = parse_ast_to_networkx_graph(src_G1)
    NXGraph_G2 = parse_ast_to_networkx_graph(src_G2)

    """
    Printing Basic Information about the two Graphs
    """
    print("Number of NODES in Larger Code:{}".format(NXGraph_G1.number_of_nodes()))
    print("Number of EDGES in Larger Code:{}".format(NXGraph_G1.number_of_edges()))

    print("Number of NODES in Smaller Code:{}".format(NXGraph_G2.number_of_nodes()))
    print("Number of EDGES in Smaller Code:{}".format(NXGraph_G2.number_of_edges()))

    print("G1 Graph - Undirected: {}".format((NXGraph_G1)))

    print("G2 Graph - Undirected: {}".format((NXGraph_G2)))

    f, axes = plt.subplots(1, 2, figsize=[20, 10])

    nx.draw(
        NXGraph_G1,
        ax=axes[0],
        node_color="tab:blue",
        font_color="black",
        with_labels=True,
    )

    nx.draw(
        NXGraph_G2,
        ax=axes[1],
        node_color="tab:red",
        font_color="black",
        with_labels=True,
    )
    plt.savefig("sgi_qccd_result.png")
    # Don't have to show the graphs when this script serves the conductor script,
    # its just part of the pipeline.
    # plt.show()


# Commenting out Quantum Annealing part because that is going to be handled by the conductor
# script.
"""
Quantum Annealing Part:
The Labeled NetworkX graphs are sent over to the Sub graph isomorphism code script `sgi_qccd_modified_H1.py`
to check whether the smaller code is a subgraph of the larger code, and to find out
the mapping from the smaller code's graph to the larger code's graph. 
"""
# sgi_qccd_modified_H1.present_results(sgi_qccd_modified_H1.find_isomorphism([NXGraph_G, NXGraph_SG]))