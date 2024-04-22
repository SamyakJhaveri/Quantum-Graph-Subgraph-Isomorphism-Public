"""
Final Working Script to be used for Experiments. 


Script that Conducts the experiments and coordinated the activities of all the scripts 

References:
- https://towardsdatascience.com/simple-trick-to-work-with-relative-paths-in-python-c072cdc9acb9
"""

# Importing the right libraries and frameworks
import ast
import graphviz as gv # Had trouble installing graphviz to ocean virtual environment via homebrew. used pip install graphviz instead and worked like a charm
from graphviz import Digraph, Graph
import pydot
import networkx as nx
import pydotplus
import sys
import os
from sys import argv
from networkx.drawing.nx_agraph import write_dot, graphviz_layout
import itertools
import numpy as np  
import dimod
from dwave.system import LeapHybridDQMSampler 
import time
import dwave.inspector
import argparse
import astor

# Ignore errors importing matpotlib.pyplot
try:
    import matplotlib.pyplot as plt  
    import matplotlib.colors as mcolors
except ImportError:
    pass

""" Importing the scripts and their functions """

# importing 'code_to_networkx_script_for_experiment.py' script
import code_to_networkx_script_for_experiment

# importing `sgi_qccd_modified_H1_for_experiment.py`
# from SubGraph_Isomorphism_QCCD import sgi_qccd
# H1 is the baseline Hamiltonian, 
# H2 is the compact Hamiltonian (tweaked and fine tuned for the the Code Clone detection problem)
import sgi_qccd_modified_H1_for_experiment

# importing `testing_and_evaluation_for_experiment.py` script
import testing_and_evaluation_for_experiment

# importing CodeCloneGeneratorSam scripts that create Type 1, 2, and 3 clones of a given code
codeclonegeneratorsam_scripts_path = '/Users/samyakjhaveri/Desktop/Drive Folder/Research/UCI Quantum Code Clone Detection Project/1 Generating Code Clone Dataset/Trial/CodeCloneGeneratorSam'
sys.path.insert(1, codeclonegeneratorsam_scripts_path)
import codeclonegenerator
from logic import create_type_1 as type1, create_type_2 as type2, create_type_3 as type3


if __name__ == "__main__":
    # Output directory for all files
    _OUTPUT_DIR = '/Users/samyakjhaveri/Desktop/Drive Folder/Research/UCI Quantum Code Clone Detection Project/Experiment Result Data'
    _TYPE_1_OUTPUT_DIR = 'type1'
    _TYPE_2_OUTPUT_DIR = 'type2'
    _TYPE_3_OUTPUT_DIR = 'type3'
    if len(argv) < 2:
        print('you must pass python filename to the script')
        exit(-1)

    # Create output directory if it doesn't exist
    type1_output_path = os.path.join(_OUTPUT_DIR, _TYPE_1_OUTPUT_DIR)
    type2_output_path = os.path.join(_OUTPUT_DIR, _TYPE_2_OUTPUT_DIR)
    type3_output_path = os.path.join(_OUTPUT_DIR, _TYPE_3_OUTPUT_DIR)
    if not os.path.exists(_OUTPUT_DIR):
        os.makedirs(_OUTPUT_DIR)
        os.makedirs(type1_output_path)
        os.makedirs(type2_output_path)
        os.makedirs(type3_output_path)

    # OG Code = Larger Code = Target Graph = Main Graph
    # G1_file_url = '/Users/samyakjhaveri/Desktop/Drive Folder/Research/UCI Quantum Code Clone Detection Project/Graph - Subgraph test codes/test_graph_code.py'
    G1_file_path = argv[1]
    # G1_file_path = os.path.join(G1_folder_path, G1_filename)
    
    """ Type 1 Clone """
    """
    # Creating a Type 1 Clone of the Original Code
    original_file_path = os.path.join(G1_folder_path, G1_filename)
    print("\nSTART OF TYPE 1 ------------------------")
    G2_file_path = type1.create_type_1(original_file_path, type1_output_path)
    print("END OF TYPE 1 --------------------------\n")
    #G2_file_url = '/Users/samyakjhaveri/Desktop/Drive Folder/Research/UCI Quantum Code Clone Detection Project/1 Generating Code Clone Dataset/Trial/pyclone github version/PycloneTestBankCreator/output/type1/test'
    
    # Generating Network X Graphs of the Original Code and the Type 1 Clone 
    # by converting them into ASTs as per our way 
    NXGraph_G1 = code_to_networkx_script_for_experiment.parse_ast_to_networkx_graph(code_to_networkx_script_for_experiment.get_code_from_storage(G1_file_path))
    NXGraph_G2 = code_to_networkx_script_for_experiment.parse_ast_to_networkx_graph(code_to_networkx_script_for_experiment.get_code_from_storage(G2_file_path))
    """

    """ Type 2 Clone """
    
    # Creating a Type 2 Clone of the Original Code
    print("\nSTART OF TYPE 2 ------------------------")
    # G3_ast = type2.create_type_2(G1_file_path)
    G3_ast = type2.create_type_2_clone(G1_file_path, type2_output_path)
    print("\nType of G3_ast:{}".format(type(G3_ast)))
    print("END OF TYPE 2 --------------------------\n")
    
    # Generating AST Dump of Original Code as per the technique of PyClone
    # G1_ast = astor.dump_tree(astor.code_to_ast.parse_file(G1_file_path))
    NXGraph_G1 = code_to_networkx_script_for_experiment.parse_ast_to_networkx_graph(code_to_networkx_script_for_experiment.get_code_from_storage(G1_file_path))

    NXGraphG3Ini = code_to_networkx_script_for_experiment.GetNXgraphFromAST()
    NXGraphG3Ini.visit(G3_ast)
    NXGraph_G3 = NXGraphG3Ini.graph

    """
    Printing Basic Information about the two Graphs
    """
    print("Number of NODES in Larger Code:{}".format(NXGraph_G1.number_of_nodes()))
    print("Number of EDGES in Larger Code:{}".format(NXGraph_G1.number_of_edges()))

    # print("Number of NODES in Smaller Code:{}".format(NXGraph_G2.number_of_nodes()))
    # print("Number of EDGES in Smaller Code:{}".format(NXGraph_G2.number_of_edges()))

    
    print("Number of NODES in Smaller Code:{}".format(NXGraph_G3.number_of_nodes()))
    print("Number of EDGES in Smaller Code:{}".format(NXGraph_G3.number_of_edges()))

    # print("Number of NODES in Smaller Code:{}".format(NXGraph_G4.number_of_nodes()))
    # print("Number of EDGES in Smaller Code:{}".format(NXGraph_G4.number_of_edges()))
    

    print("G1 Graph - Original Code: {}".format((NXGraph_G1)))  
    # print("G2 Graph - Type 1 Code Clone: {}".format((NXGraph_G2)))
    print("G3 Graph - Type 2 Code Clone: {}".format((NXGraph_G3)))
    # print("G4 Graph - Type 3 Code Clone: {}".format((NXGraph_G4)))

    f, axes = plt.subplots(1, 2, figsize = [20, 10])

    nx.draw(NXGraph_G1, 
            ax = axes[0],
            node_color = "tab:blue", 
            font_color = "black",
            with_labels = True)
    
    """
    nx.draw(NXGraph_G2, 
            ax = axes[1],
            node_color = "tab:red", 
            font_color = "black",
            with_labels = True)
    """
    nx.draw(NXGraph_G3, 
            ax = axes[1],
            node_color = "tab:red", 
            font_color = "black",
            with_labels = True)
    
    """
    nx.draw(NXGraph_G4, 
            ax = axes[1],
            node_color = "tab:red", 
            font_color = "black",
            with_labels = True)
    """

    # plt.savefig("sgi_qccd_result.png") is commented out because saving and storing 
    # results and data about the experiment happens in the later part of this script. 
    
    # plt.savefig(os.path.splitext(G2_file_path)[0] + ".png")
    # plt.savefig(os.path.splitext(G3_file_path)[0] + ".png")
    # plt.savefig(os.path.splitext(G4_file_path)[0] + ".png")
    plt.show() # is commented out so that it doesn't interrupt the flow of the experiment

    """ THE SUBGGRAPH ISOMORPHISM Problem Implemented for Quantum Code Clone Detection Solved on the DWave """
    
    # G1_G2_sampleset = sgi_qccd_modified_H1_for_experiment.find_isomorphism([NXGraph_G1, NXGraph_G2])
    G1_G3_sampleset = sgi_qccd_modified_H1_for_experiment.find_isomorphism([NXGraph_G1, NXGraph_G3])
    # G1_G4_sampleset = sgi_qccd_modified_H1_for_experiment.find_isomorphism([NXGraph_G1, NXGraph_G4])
    
    # sgi_qccd_modified_H1_for_experiment.present_results(G1_G2_sampleset)
    sgi_qccd_modified_H1_for_experiment.present_results(G1_G3_sampleset)
    # sgi_qccd_modified_H1_for_experiment.present_results(G1_G4_sampleset)
    """
    # Here, `annealing_results` in the form of 
    # [G1, G2, results] - A list which has 
    #   First element - G1 graph
    #   Second element - G2 graph
    #   Third Element - results - Resultant mappings from 
    # G2 graph to G2 graph
    # Made a separate `annealing_results` object so that I could use it with the last step of 
    # 'Storing the results and generating a report of each experiment`
    """

    """ Type 2 Code Clone """
    """
    # Creating a Type 2 Clone of the Original Code
    print("\nSTART OF TYPE 1 ------------------------")
    type1.create_type_1(G1_file_url, type1_output_path)
    print("END OF TYPE 1 --------------------------\n")
    G2_file_url = type1_output_path
    """

    """ Generating Code Clone Dataset """
    # Still in Trial Phase
    # Will add when I get a working code to use

    # parser = argparse.ArgumentParser()
    # parser.add_argument("--original_code_url")
    # args = parser.parse_args()
    """
    # Larger Code = Target Graph = Main Graph
    G1_file_url = '/Users/samyakjhaveri/Desktop/Drive Folder/Research/UCI Quantum Code Clone Detection Project/Graph - Subgraph test codes/test_graph_code.py'
    srcG1 = code_to_networkx_script_trial_2.get_code_from_storage(G1_file_url)

    # Smaller Code = Graph to Embed = Sub-Graph
    G2_file_url = '/Users/samyakjhaveri/Desktop/Drive Folder/Research/UCI Quantum Code Clone Detection Project/Graph - Subgraph test codes/test_subgraph_code.py'
    srcG2 = code_to_networkx_script_trial_2.get_code_from_storage(G2_file_url)

    NXGraph_G1 = code_to_networkx_script_trial_2.parse_ast_to_networkx_graph(srcG1)
    NXGraph_G2 = code_to_networkx_script_trial_2.parse_ast_to_networkx_graph(srcG2)
    """
    
    
    """ Testing and Evaluating the Results """
    """
    sampleset = G1_G2_sampleset[2]
    n1 = G1_G2_sampleset[0].number_of_nodes() # 'number of nodes in G1'
    n2 = G1_G2_sampleset[1].number_of_nodes() # 'number of nodes in G2'
    e1 = G1_G2_sampleset[0].number_of_edges() # 'number of edges in G1'
    e2 = G1_G2_sampleset[1].number_of_edges() # 'number of edges in G2'
    clone_type = 1 # could be Type 1, 2, or 3 clone depending on the input codes. 
    key = "G1(" + str(n1) + ")_G2(" + str(n2) + ")_type_" + str(clone_type) + "_clone"  # example: "G1(32)_G2(28)_type_1_clone"
    experiment_label =  'qccd_H1_experiment_result_data_' + key
    best_mapping = sampleset.first.sample # the resultant mapping obtained form the annealing process (Could store 5 of these for averging out the result by running the script 5 times)
    best_mapping_energy = sampleset.first.energy 
    runtime = sampleset.info["run_time"] # time, in microseconds, of the run time (see description of runtime in Notes and 'testing_and_evaluation_script')
    charge_time = sampleset.info["charge_time"] # time, in microseconds, of the charge time (see description of chargetime in Notes and 'testing_and_evaluation_script')
    qpu_access_time = sampleset.info["qpu_access_time"] # time, in microseconds, of the qpu access time (see description of qpu access time in Notes and 'testing_and_evaluation_script')
    dwave_leap_problem_id = sampleset.info["problem_id"] # get DWave problem ID from 'testing_and_evaluation_Script'
    no_annealing_cycles = 100 # placeholder valuefor 'number of annealing cycles'
    duration_per_anneal_cycle = 20 # placeholder value, in microseconds, for the 'duration of each anneal cycle'
    # solver_information = Commented out because there a re a lot of data points, they are present in the 'testing_and_evaluation_script' 

    """
    """ Logging the results and generating a report of each experiment """
    """
    columns = [
        'key', 
        'experiment label', 
        'number of nodes in G1', 
        'number of edges in G1', 
        'number of nodes in G2', 
        'number of edges in G2',
        'clone type', 
        'best mapping from G2 to G1', 
        'best_mapping_energy',
        'runtime', 
        'charge time', 
        'qpu access time', 
        'dwave leap problem id',
        'number of annealing cycles',
        'duration per anneal cycle'
    ]

    result_data_for_csv = {
        'key': [key],
        'experiment label': [experiment_label], 
         
        'number of nodes in G1': [n1],
        'number of edges in G1': [e1], 
        'number of nodes in G2': [n2], 
        'number of edges in G2': [e2],
        'clone type': [clone_type], 
        'best mapping from G2 to G1': [best_mapping], 
        'best_mapping_energy', [best_mapping_energy]
        'runtime': [runtime],
        'charge time': [charge_time],
        'qpu access time': [qpu_access_time], 
        'dwave leap problem id': [dwave_leap_problem_id],
        'number of annealing cycles': [no_annealing_cycles],
        'duration per anneal cycle': [duration_per_anneal_cycle]
    }

    logging_result_data_folder_path = '/Users/samyakjhaveri/Desktop/Drive Folder/Research/UCI Quantum Code Clone Detection Project/Experiment Result Data/'
    logging_result_data_file_path = logging_result_data_folder_path + 'qccd_modified_H1_experiment_result_data.csv'
    

    if not os.path.exists(logging_result_data_folder_path):
        os.makedirs(logging_result_data_folder_path)
        df_for_csv = pd.DataFrame(result_data_for_csv, columns = columns)
        df_for_csv.to_csv(logging_result_data_file_path, header = False, index = False)
        print("CSV Created!")
    
    # Create another row and append row (as df) to existing CSV
    #row = [{'A':'X1', 'B':'X2', 'C':'X3'}]
    df_new_row = pd.DataFrame(result_data_for_csv)
    df_new_row.to_csv(logging_result_data_file_path, mode='a', header=False, index=False)
    print("Row added to DataFrame!")
    

    df_from_csv = pd.read_csv(logging_result_data_file_path)
    print(df_from_csv)
    """
    