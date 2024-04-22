"""
Final Experiment Code. 


Main Script that has the SubGraph Isomorphism Algorithm that creates a DQM Hamiltonian 
Equation to solve on the DWave LeapHybridDQMSampler(). 
This script also has funtions that present the results of the Annealing visually as 
plotted graphs and in text form on the Terminal.
This script is named with 'H1' as it has the baseline Hamiltonian algorithm and not 
the compact one, as inspired from Zick's paper on 'Experimental Quantum Annealing...'
The script with the modified compact Hamilotnian equation will be with 'H2' in its name. 
"""

# Import Stuff
import itertools
import numpy as np
import networkx as nx
import dimod
from dwave.system import LeapHybridDQMSampler
import time
import sys
import ast

# importing `testing_and_evaluation_for_experiment.py` script
import testing_and_evaluation_for_experiment

# importing 'code_to_networkx_script_for_experiment.py' script
import code_to_networkx_script_for_experiment

# Ignore errors importing matpotlib.pyplot
try:
    import matplotlib.pyplot as plt
    import matplotlib.colors as mcolors
except ImportError:
    pass


def create_graph_helper_function(edges):
    """
    Generate Graph from edges list

    Args:
        - edges: List of node pairs that have edges between them

    Returns:
        Graph (NetworkX)
    """
    G = nx.Graph()
    G.add_edges_from(edges)
    return G


def create_dqm_helper_function(G1, G2):
    """
    Construct DQM based on two graphs

    Create a discrete quadratic model
    to represent the problem of finding an isomorphism between the two graphs

    Args:
        G1 Target Graph (networkx.Graph)
        G2 Graph to Embed (networkx.Graph)

    Returns:
        DiscreteQuadraticModel
    """

    n1 = G1.number_of_nodes()
    n2 = G2.number_of_nodes()

    if n1 < n2:
        raise ValueError(
            "Custom message in 'create_dqm_helper_function()': n1 must be greater than or equal to n2."
        )

    G1_nodes = list(G1.nodes)
    G1_edges = list(G1.edges)
    G2_nodes = list(G2.nodes)
    G2_edges = list(G2.edges)

    print("G1 nodes:{}".format(len(G1_nodes)))
    print("G1 nodes:{}".format(G1_nodes))
    print("G2 nodes:{}".format(len(G2_nodes)))
    # print("G1 edges:{}".format(G1_edges))
    print("G2 nodes:{}".format(G2_nodes))
    # print("G2 edges:{}".format(G2_edges))

    dqm = dimod.DiscreteQuadraticModel()

    # In this formulation, the offset is equal to the number of nodes (multiplied by
    # the penalty coefficient A, currently taken to be 1.
    # Note that in a BQM formualtion, the offset would be twice as much due to the
    # need to use a penalty model for each direction of the bijection constraint.

    # The loop below ensures that each node in the graph G1 is chosen,
    # and it is chosen once - i.e. it takes care of bijectivity.
    # However, for Sub-Graph Isomorphism, bijectivity does not work. Injectivity works.
    # Therefore, every node in the smaller graph G2 has to be mapped to a node in the
    # larger graph G1, but every node in graph G1 need not be mapped to a node in
    # graph G2.
    """ Updated DQM creator code from Crista's suggestions. (better?) (Feb 25 2023)"""
    dqm.offset = n2  # This has to be n2 since the lowest energy threshold (offset) has to be equal to the number of nodes in the smaller (G2) Graph

    for node in G2.nodes:
        # Discrete Variable for node i in Graphe G1, with cases
        # representing the nodes in Graph G2
        dqm.add_variable(n1, label=node)

    # set up each coefficients associated with the constraints that
    # each node in G2 is chosen once. this representsthe H_A
    # component of the energy function
    # no two nodes in G2 should map to the same node in G1
    for node in G2.nodes:
        dqm.set_linear(node, np.repeat(-1.0, n1))
    for itarget in range(n1):
        for ivar, node1 in enumerate(G2_nodes):
            for node2 in G2_nodes[ivar + 1 :]:
                dqm.set_quadratic_case(node1, itarget, node2, itarget, 2.0)

    # Set up the constraints associated with the constraints that
    # selected edges must appear in both the graphs, which is the H_B
    # component of the eneryg function. The penality coeeficient B
    # controls the weight of H_B relative to H_A in the energy
    # function.
    B = 2.0

    # For all edges in G2, penalizes mappings to edges not in G1
    for edge2 in G2.edges:
        node2_indices = (G2_nodes.index(edge2[0]), G2_nodes.index(edge2[1]))
        for e1 in itertools.combinations(G1.nodes, 2):
            node1_indices = (G1_nodes.index(e1[0]), G1_nodes.index(e1[1]))
            if e1 in G1.edges:
                continue

            # dqm.set_quadratic_case(comb1[0], node2_indices[0], comb1[1], node2_indices[1], B)
            # dqm.set_quadratic_case(comb1[0], node2_indices[1], comb1[1], node2_indices[0], B)
            dqm.set_quadratic_case(
                edge2[0], node1_indices[0], edge2[1], node1_indices[1], B
            )
            dqm.set_quadratic_case(
                edge2[0], node1_indices[1], edge2[1], node1_indices[0], B
            )

    return dqm


def plot_graphs_helper_function(G1, G2, node_mapping):
    """
    Plot the Larger, Parent Graph G1 with the
    resultant mappings from G2 -> G1 derived from the annealing process
    drwn on top of G1.

    The provided mapping specifies how the nodes in Graph G2 correspond
    to the nodes in Graph G1. The nodes in each graph are colored using matcing colors
    based on the specififed mappings.

    Args:
        G1 (NetworkX Graph) - Target Graph
        G2 (NetworkX Graph) - Graph to Embed
        node_mapping (dict) - Dictionary that defines the correspondence between nodes
                            in graph 1 and nodes in graph 2. The keys are the names of nodes in
                            graph 1, and the values are the names of nodes in graph 2.
    """
    # from the G/SGMorph plotting function
    # invert the mapping so it is fromthe target graph TO the graph to embed nodes
    # Snippet taken from:
    # https://stackoverflow.com/a/483833

    inv_node_mapping = {v: k for k, v in node_mapping.items()}
    print("inv_node_mapping:{}".format(inv_node_mapping))

    # relabel the nodes in the target graph with the node labels from the graph to embed
    updated_nodes = nx.relabel_nodes(G1, inv_node_mapping, copy=True)
    print("updated_nodes:{}".format(updated_nodes.nodes))
    # Get the same fixed position as usec before
    pos = nx.spring_layout(updated_nodes, seed=1000)

    # Highlight the nodes that have been relabeled
    nx.draw(
        updated_nodes,
        pos,
        with_labels=True,
        font_color="red",
        nodelist=[key for key in node_mapping.keys()],
        node_color="tab:red",
    )

    # Difference between two lists:
    # https://stackoverflow.com/a/3462160
    nx.draw(
        updated_nodes,
        pos,
        with_labels=True,
        font_color="black",
        nodelist=list(set(updated_nodes.nodes()) - set(node_mapping.keys())),
        node_color="tab:blue",
    )

    plt.show()


def edges_to_graph():
    """
    Function to convert edges into a NetworkX Graph

    Returns:
        - [G1, G2] - Pair of Target Graph G1 and Graph to Embed G2 in lsit form
    """
    # GRAPH G1 - TARGET GRAPH
    # 1. Square wwith four vertices, an edge connecting all vertices to make a square and a diagonal edge that connects two opposite corner vertices
    # edges_1 = [(0, 1), (0, 3), (1, 2), (1, 3), (2, 3)]

    # 2. Pentagon with 5 vertices, an edge connecting al the vertices to make a pentagon, and a horizontal edge between two opposite verices such that there are two distinct visible
    # geometrical shapes - one triangle and one trapezium
    # edges_1 = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 0), (1, 4)]

    # 3. A Graph I found on the internet with
    # edges_1 = [(0, 1), (0, 2), (0, 3),  (0, 4), (1, 2), (2, 3), (3, 4), (1, 5), (1, 6), (3, 5), (4, 6), (5, 6)]

    # 4. Graph G1
    # edges_1 = [(0, 1), (1, 2), (0, 2), (3, 4), (4, 5), (3, 5), (2, 5)]

    # 5 Graph G1 i got from internet
    edges_1 = [
        (0, 1),
        (1, 2),
        (2, 3),
        (3, 4),
        (4, 5),
        (5, 0),
        (1, 3),
        (1, 4),
        (1, 5),
        (2, 4),
    ]

    # GRAPH G2 - GRAPH TO EMBED
    # 1. Triangle graph that IS an Isomorphic Sub-Graph of Graph G1 Target Graph
    edges_2 = [(0, 1), (1, 2), (2, 0)]

    # 2. Square Graph with four vertices, an edge connecting all vertices to make a square
    # edges_2 = [(0, 1), (1, 2), (2, 3), (3, 0)]

    # 3. Sub graph of Grpah 1 of number 3
    # edges_2 = [(0, 1), (0, 2), (0, 3), (1, 2), (2, 3), (1, 4), (1, 5), (3, 4), (3, 5)]

    # 4. Triangle graph that IS an Isomorphic Sub-Graph of Graph G1 Target Graph
    # edges_2 = [(0, 1), (1, 2), (2, 0), (1, 3)]

    # 5. Graph G2 Sub Graph of G1 of #5
    # edges_2 = [(0, 1),(1, 2),(1, 3),(1, 4),(4, 0)]

    edges_1 = [(0, 4), (1, 3), (2, 5), (1, 4), (4, 5), (1, 6), (3, 6), (4, 7), (6, 8)]
    # edges_2 = [(1, 2),(2, 3),(2, 4),(3, 4)]
    edges_2 = [("a", "b"), ("b", "c"), ("b", "d"), ("c", "d")]

    G1 = create_graph_helper_function(edges_1)
    G2 = create_graph_helper_function(edges_2)

    nx.draw(G1, with_labels=True)
    plt.show()
    nx.draw(G2, with_labels=True)
    plt.show()

    return [G1, G2]


def find_isomorphism(G1, G2):
    # def find_isomorphism(G1_G2_pair_list):
    """
    Search for isomorpshim between two graphs

    Args:
        G_list - Pair of G1 and G2 in list form G1 Target Graph
        (NetworkX Graph), G2 Graph to Embed (NetworkX Graph)

    Returns:
        [G1, G2, results] - A list which has
                            First element - G1 graph
                            Second element - G2 graph
                            results - Resultant mappings from
                            G2 graph to G2 graph

        If no isomorphism is found, returns None.
        Otherwise, returns dict with keys as nodes
        from graph 1 and values as corresponding nodes from graph 2.
    """
    # G1 = G1_G2_pair_list[0]
    # G2 = G1_G2_pair_list[1]

    dqm = create_dqm_helper_function(G1, G2)
    sampler = LeapHybridDQMSampler()
    sampleset = sampler.sample_dqm(
        dqm, label="Example - Quantum Code Clone Detection using Sub Graph Isomorphism"
    )

    # Generating and Presenting testing and evaluation data using the separate script
    # testing_and_evaluation_for_experiment.get_solver_sampler_information(sampler)
    # testing_and_evaluation_for_experiment.get_current_solution_sampleset_evaluation_data(sampleset)

    return G1, G2, sampleset


# def present_results(G1_G2_sampleset):
def present_results(G1, G2, sampleset):
    """
    Function to present the resultant mappings
    and plot the graphs

    Args:
        G1_G2_sampleset - A list which has
                        First element - G1 graph
                        Second element - G2 graph
                        sampleset - Resultant mappings and other important informationabout the
                        execution of the annealing process from G2 graph to G1 graph
    """
    # G1, G2 = G1_G2_sampleset[0], G1_G2_sampleset[1]
    # sampleset = G1_G2_sampleset[2]
    results = sampleset

    print("Sub-GI Mappings Results from G2 --> G1 are \n :{}".format(results))
    print("Type of 'results':{}".format(type(results)))

    updated_best_mapping = {}

    if np.isclose(results.first.energy, 0.0):
        # 'best_mapping' is the top most mapping that has 0.0 energy, from nodes in G2 to nodes in G1
        print("G2 is a Sub-Graph of G1. Yay!")
        best_mapping = results.first.sample
        print("best_mapping:{}".format(best_mapping))
        G1_nodes = list(G1.nodes)
        updated_best_mapping = {k: G1_nodes[v] for k, v in best_mapping.items()}
        print("\nupdated_best_mapping:{}".format(updated_best_mapping))
        plot_graphs_helper_function(G1, G2, updated_best_mapping)

    else:
        print("NO, G2 is not a Subgraph of G1")


if __name__ == "__main__":
    # start = time.time()
    # G1, G2 = edges_to_graph()

    # May have to modify the links as per your file structure
    with open(
        "~/Dataset/sample4/sample4_type1_v1.py",
        "r",
    ) as f1, open(
        "~/Dataset/sample4/sample4_type3_v2.py",
        "r",
    ) as f2:
        code1 = f1.read()
        code2 = f2.read()

    NXGraph_G1 = code_to_networkx_script_for_experiment.parse_ast_to_networkx_graph(
        ast.parse(code1)
    )
    NXGraph_G2 = code_to_networkx_script_for_experiment.parse_ast_to_networkx_graph(
        ast.parse(code2)
    )

    # THE SUBGGRAPH ISOMORPHISM Problem Implemented for Quantum Code Clone Detection Solved on the DWave
    if NXGraph_G1.number_of_nodes() >= NXGraph_G2.number_of_nodes():
        resG1, resG2, sampleset = find_isomorphism(NXGraph_G1, NXGraph_G2)
        print(
            "\nMappping {0} with {1} nodes onto {2} with {3} nodes".format(
                ncs[j][0],
                NXGraph_G2.number_of_nodes(),
                ncs[i][0],
                NXGraph_G1.number_of_nodes(),
            )
        )
    else:
        resG1, resG2, sampleset = find_isomorphism(NXGraph_G2, NXGraph_G1)
        print(
            "\nMappping {0} with {1} nodes onto {2} with {3} nodes".format(
                ncs[i][0],
                NXGraph_G1.number_of_nodes(),
                ncs[j][0],
                NXGraph_G2.number_of_nodes(),
            )
        )

    best_mapping = (
        sampleset.first.sample
    )  # the resultant mapping obtained form the annealing process (Could store 5 of these for averging out the result by running the script 5 times)
    best_mapping_energy = sampleset.first.energy
    qpu_access_time = sampleset.info["qpu_access_time"]
    G1_nodes = list(resG1.nodes)
    print("Corresponding mapping:{}".format(best_mapping))
    updated_best_mapping = {k: G1_nodes[v] for k, v in best_mapping.items()}
    print("\nupdated_best_mapping:{}".format(updated_best_mapping))
    print("best_mapping_energy:{}".format(best_mapping_energy))
    print("qpu_access_time:{}".format(qpu_access_time))
    print(
        "min(resG1, resG2):{}".format(
            min(resG1.number_of_nodes(), resG2.number_of_nodes())
        )
    )
    print("updated_best_mapping:{}".format(updated_best_mapping))
    print(
        "Energy: {0}, Timing: {1}, Minimum Node:{2}".format(
            data_energy, data_timing, data_minnode
        )
    )
    print(len(data_energy))

    present_results(find_isomorphism(edges_to_graph()))

    end = time.time()
    print(
        "\nTotal Time taken by Script to run(including the visuals): {}".format(
            str(end - start)
        )
    )
    print(
        "\nTotal Time taken by Script to run(excluding the visuals): {}".format(
            str(end - start)
        )
    )

    axes = plot_graphs(G1, G2, best)
    axes[0].set_title("Graph G2 (Graph to Embed) mapped onto Graph G1 (Target Graph)")

    # only finding isomorphism between two graphs for now
    """
    results = find_isomorphism(G1, G2)
    if results is None:
        print("No Isomorphism Found")
    else:
        print("The Two Graphs are Isomorphic!")
        for r1, r2 in results.items():
            print("{} --> {}".format(r2, r1))
        
        axes = plot_graphs(G1, G2, results)
        axes[0].set_title('Graph 1 - Target Graph')
        axes[1].set_title('Graph 2 - Graph to Embed')
        
        plt.show()
        filename = 'sub-gi.png'
        plt.savefig(filename, bbox_inches = 'tight')
        print("Plot saved to:", filename)  
        if args.save_plot:
            filename = 'circuit_equivalence.png'
            plt.savefig(filename, bbox_inches='tight')
            print('Plot saved to:', filename)
        """
