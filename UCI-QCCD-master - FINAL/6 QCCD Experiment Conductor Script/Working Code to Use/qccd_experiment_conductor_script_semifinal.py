"""
Semi-Final Script. Works perfectly well but not used in the Final version of the Experiment.
Final Script is 'Working Code to Use' Folder with the other scripts and the conductor script.

Script that Conducts the experiments and coordinated the activities of all the scripts 

References:
- https://towardsdatascience.com/simple-trick-to-work-with-relative-paths-in-python-c072cdc9acb9
- Using Pickle - https://ianlondon.github.io/blog/pickling-basics/
- Appending a new row of information to an existing csv file -https://www.youtube.com/watch?v=sHf0CJU8y7U
- https://blog.finxter.com/how-to-append-a-new-row-to-a-csv-file-in-python/

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
import pandas as pd


# Ignore errors importing matpotlib.pyplot
try:
    import matplotlib.pyplot as plt  
    import matplotlib.colors as mcolors
except ImportError:
    pass

""" Importing the scripts and their functions """

# importing 'codeclonegenerator_semifinal.py' script
codeclonegenerator_semifinal_path = '/Users/samyakjhaveri/Desktop/Drive Folder/Research/UCI Quantum Code Clone Detection Project/1 Generating Code Clone Dataset/Working Code to Use/CodeCloneGeneratorSam/'
sys.path.insert(1, codeclonegenerator_semifinal_path)
import codeclonegenerator_semifinal
from logic.common import construct_output_file


# importing 'code_to_networkx_script_semifinal.py' script
code_to_networkx_script_semifinal_path = '/Users/samyakjhaveri/Desktop/Drive Folder/Research/UCI Quantum Code Clone Detection Project/2 Code to Networkx Graph/Working Code to Use'
sys.path.insert(1, code_to_networkx_script_semifinal_path)
import code_to_networkx_script_semifinal

# importing `sgi_qccd_modified_H1_semifinal.py`
sgi_qccd_modified_H1_semifinal_path = '/Users/samyakjhaveri/Desktop/Drive Folder/Research/UCI Quantum Code Clone Detection Project/3 SubGraph_Isomorphism_QCCD/Working Code to Use'
sys.path.insert(1, sgi_qccd_modified_H1_semifinal_path)
# from SubGraph_Isomorphism_QCCD import sgi_qccd
# H1 is the baseline Hamiltonian, 
# H2 is the compact Hamiltonian (tweaked and fine tuned for the the Code Clone detection problem)
import sgi_qccd_modified_H1_semifinal

# importing `testing_and_evaluation_semifinal.py` script
testing_and_evaluation_semifinal_path = '/Users/samyakjhaveri/Desktop/Drive Folder/Research/UCI Quantum Code Clone Detection Project/4 Testing and Evaluation/Working Code to Use'
sys.path.insert(1, testing_and_evaluation_semifinal_path)
import testing_and_evaluation_semifinal

"""
# importing PyClone scripts that create Type 1, 2, and 3 clones of a given code
pyclone_scripts_path = '/Users/samyakjhaveri/Desktop/Drive Folder/Research/UCI Quantum Code Clone Detection Project/1 Generating Code Clone Dataset/Trial/PycloneTestBankCreatorSam'
sys.path.insert(1, pyclone_scripts_path)
import creator
"""

from logic import create_type_1 as type1, create_type_2 as type2, create_type_3 as type3

# importing `logging_results_data_seminfinal.py` script 
logging_results_data_seminfinal_path = '/Users/samyakjhaveri/Desktop/Drive Folder/Research/UCI Quantum Code Clone Detection Project/5 Logging Results Data/Working Code to Use/'
sys.path.insert(1, logging_results_data_seminfinal_path)
import logging_results_data_seminfinal


if __name__ == "__main__":
    print("Enter the file path of the original code and the code clone type you want to check:")
    print("Format: python <qccd_experiment...> --t <clone_type> --file_path <'file path of original code'>")
    parser = argparse.ArgumentParser()
    parser.add_argument("--t")
    parser.add_argument("--file_path")
    args = parser.parse_args()

    # Output directory for all files
    _OUTPUT_DIR = 'output'
    _TYPE_1_OUTPUT_DIR = 'type1_clones'
    _TYPE_2_OUTPUT_DIR = 'type2_clones'
    _TYPE_3_OUTPUT_DIR = 'type3_clones'

    # Create output directory if it doesn't exist
    type1_output_path = os.path.join(_OUTPUT_DIR, _TYPE_1_OUTPUT_DIR)
    print("Type 1 OUTPUT Path:", type1_output_path)
    type2_output_path = os.path.join(_OUTPUT_DIR, _TYPE_2_OUTPUT_DIR)
    print("Type 2 OUTPUT Path:", type1_output_path)
    type3_output_path = os.path.join(_OUTPUT_DIR, _TYPE_3_OUTPUT_DIR)
    print("Type 3 OUTPUT Path:", type1_output_path)
    
    if not os.path.exists(_OUTPUT_DIR):
        os.makedirs(_OUTPUT_DIR)
        os.makedirs(type1_output_path)
        os.makedirs(type2_output_path)
        os.makedirs(type3_output_path)
    
    # OG Code = Larger Code = Target Graph = Main Graph
    # G1_folder_path = argv[1]
    # G1_filename = 'test_graph_code.py'
    # G1_file_path = os.path.join(G1_folder_path, G1_filename)
    original_file_path = args.file_path
    G1_file_path = original_file_path
    
    # Generating AST Dump of Original Code as per the technique of PyClone
    # G1_ast = astor.dump_tree(astor.code_to_ast.parse_file(G1_file_path))
    srcG1 = code_to_networkx_script_semifinal.get_code_from_storage(G1_file_path)
    G1_ast = ast.parse(srcG1)

    NXGraphG1Ini = code_to_networkx_script_semifinal.GetNXgraphFromAST()
    NXGraphG1Ini.visit(G1_ast)
    NXGraph_G1 = NXGraphG1Ini.graph

    if args.t == "1":
        print("\nSTART OF TYPE 1 ------------------------")
        type1_code_clone_ast = type1.create_type_1_clone(original_file_path, type1_output_path)
        print("Type 1 Code Clone AST:{}".format(type1_code_clone_ast))
        print("Type 1 Code Clone Output path:{}".format(type1_output_path))
        output_path = type1_output_path
        code_clone_type = 1
        mod_code_clone_ast = type1_code_clone_ast
        print("END OF TYPE 1 --------------------------\n")
    elif args.t == "2":
        print("\nSTART OF TYPE 2 ------------------------")
        type2_code_clone_ast = type2.create_type_2_clone(original_file_path, type2_output_path)
        print("Type 2 Code Clone AST: {}".format(type2_code_clone_ast))
        print("Type 2 Code Clone Output path:{}".format(type2_output_path))
        output_path = type2_output_path
        code_clone_type = 2
        mod_code_clone_ast = type2_code_clone_ast
        print("END OF TYPE 2 --------------------------\n")
    elif args.t == "3":
        print("\nSTART OF TYPE 3 ------------------------")
        type3_code_clone_ast = type3.create_type_3_clone(original_file_path, type3_output_path)
        print("Type 3 Code Clone AST: {}".format(type3_code_clone_ast))
        print("Type 3 Code Clone Output path:{}".format(type3_output_path))
        output_path = type3_output_path
        code_clone_type = 3
        mod_code_clone_ast = type3_code_clone_ast
        print("END OF TYPE 3 --------------------------\n")
    
    NXGraphG2Ini = code_to_networkx_script_semifinal.GetNXgraphFromAST()
    NXGraphG2Ini.visit(mod_code_clone_ast)
    NXGraph_G2 = NXGraphG2Ini.graph
    
    new_file_path = construct_output_file(original_file_path, output_path, code_clone_type)
    codeclonegenerator_semifinal.store_code_clone(new_file_path, mod_code_clone_ast, code_clone_type)    

    """
    Printing Basic Information about the two Graphs
    """
    print("Number of NODES in Larger Code:{}".format(NXGraph_G1.number_of_nodes()))
    print("Number of EDGES in Larger Code:{}".format(NXGraph_G1.number_of_edges()))

    print("Number of NODES in Smaller Code:{}".format(NXGraph_G2.number_of_nodes()))
    print("Number of EDGES in Smaller Code:{}".format(NXGraph_G2.number_of_edges()))

    f, axes = plt.subplots(1, 2, figsize = [20, 10])

    nx.draw(NXGraph_G1, 
            ax = axes[0],
            node_color = "tab:blue", 
            font_color = "black",
            with_labels = True)
    nx.draw(NXGraph_G2, 
            ax = axes[1],
            node_color = "tab:red", 
            font_color = "black",
            with_labels = True)

    # plt.savefig("sgi_qccd_result.png") is commented out because saving and storing 
    # results and data about the experiment happens in the later part of this script. 
    
    plt.savefig(os.path.splitext(output_path)[0] + ".png")
    plt.show() # is commented out so that it doesn't interrupt the flow of the experiment


    """ THE SUBGGRAPH ISOMORPHISM Problem Implemented for Quantum Code Clone Detection Solved on the DWave """
    G1_G2_sampleset = sgi_qccd_modified_H1_semifinal.find_isomorphism([NXGraph_G1, NXGraph_G2])
    
    sgi_qccd_modified_H1_semifinal.present_results(G1_G2_sampleset)

    # Here, `annealing_results` in the form of 
    # [G1, G2, results] - A list which has 
    #   First element - G1 graph
    #   Second element - G2 graph
    #   Third Element - results - Resultant mappings from 
    # G2 graph to G1 graph
    # Made a separate `annealing_results` object so that I could use it with the last step of 
    # 'Storing the results and generating a report of each experiment`
    
    """ Testing and Evaluating the Results """
    
    sampleset = G1_G2_sampleset[2]
    n1 = NXGraph_G1.number_of_nodes() # 'number of nodes in G1'
    e1 = NXGraph_G1.number_of_edges() # 'number of edges in G1'
    n2 = NXGraph_G2.number_of_nodes() # 'number of nodes in G2'
    e2 = NXGraph_G2.number_of_edges() # 'number of edges in G2'
    key = "G1(" + str(n1) + ")_G2(" + str(n2) + ")_type_" + str(code_clone_type) + "_clone"  # example: "G1(32)_G2(28)_type_1_clone"
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

    
    """ Logging the results and generating a report of each experiment """
    
    columns = [
        'key', 
        'experiment label', 
        'number of nodes in G1', 
        'number of edges in G1', 
        'number of nodes in G2', 
        'number of edges in G2',
        'code clone type', 
        'best mapping from G2 to G1', 
        'best mapping energy',
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
        'code clone type': [code_clone_type], 
        'best mapping from G2 to G1': [best_mapping], 
        'best mapping energy': [best_mapping_energy],
        'runtime': [runtime],
        'charge time': [charge_time],
        'qpu access time': [qpu_access_time], 
        'dwave leap problem id': [dwave_leap_problem_id],
        'number of annealing cycles': [no_annealing_cycles],
        'duration per anneal cycle': [duration_per_anneal_cycle]
    }

    logging_result_data_folder_path = '/Users/samyakjhaveri/Desktop/Drive Folder/Research/UCI Quantum Code Clone Detection Project/Experiment Result Data'
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
    