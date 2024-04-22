"""
Final Experiment Code 

Script that Conducts the experiments and coordinated the activities of all the scripts 

References:
- https://towardsdatascience.com/simple-trick-to-work-with-relative-paths-in-python-c072cdc9acb9
"""

# Importing the right libraries and frameworks
import ast
import networkx as nx
import os
import csv
from networkx.drawing.nx_agraph import write_dot, graphviz_layout
import numpy as np  
import pandas as pd
import dimod
from dwave.system import LeapHybridDQMSampler 
import time
# import dwave.inspector
import argparse
import pickle

# Ignore errors importing matpotlib.pyplot
try:
    import matplotlib.pyplot as plt  
    import matplotlib.colors as mcolors
except ImportError:
    pass

""" Importing the scripts and their functions """

# importing 'code_to_networkx_script_for_experiment.py' script
import code_to_networkx_script_for_experiment


# H1 is the baseline Hamiltonian, 
import sgi_qccd_H1_for_experiment

# importing `sgi_qccd_H2_for_experiment.py`
# H2 is the compact Hamiltonian (tweaked and fine tuned for the the Code Clone detection problem)
import sgi_qccd_H2_for_experiment

# importing `testing_and_evaluation_for_experiment.py` script
import testing_and_evaluation_for_experiment

# importing CodeCloneGeneratorSam scripts that create Type 1, 2, and 3 clones of a given code
from logic import create_type_1 as type1, create_type_2 as type2, create_type_3 as type3


if __name__ == "__main__":
# ---------- x ---------- x ---------- x ---------- 
    """ Part of the experiment conductor for conducting experiments o n the generated programs.csv dataset, 
    on the server(styx or openlab)"""
    root_path = os.path.split(os.getcwd())[0]
    print("root_path:{}".format(root_path))

    input_folder_path = os.path.join(root_path, 'programs')
    print("input_folder_path:{}".format(input_folder_path))
    
    input_file_name = "programs_sample4_9.csv"
    input_file_path = os.path.join(root_path, input_folder_path)
    input_file_path = os.path.join(input_folder_path, input_file_name)
    print("input_file_path:{}".format(input_file_path))
    
    output_folder_path = os.path.join(root_path, 'new_results')
    print("output_folder_path:{}".format(output_folder_path))

    output_file_name_energy = "new_results_sample4_9_energy_without_nodetype_comparison_#10.csv"
    output_file_path_energy = os.path.join(output_folder_path, output_file_name_energy)
    print("output_file_path_energy:{}".format(output_file_path_energy))

    output_file_name_timing = "new_results_sample4_9_timing_without_nodetype_comparison_#10.csv"
    output_file_path_timing = os.path.join(output_folder_path, output_file_name_timing)
    print("output_file_path_timing:{}".format(output_file_path_timing))
    
    output_file_name_minnode = "new_results_sample4_9_minnode_without_nodetype_comparison_#10.csv"
    output_file_path_minnode = os.path.join(output_folder_path, output_file_name_minnode)
    print("output_file_path_minnode:{}".format(output_file_path_minnode))

    output_file_name_mapping = "new_results_sample4_9_mapping_without_nodetype_comparison_#10.csv"
    output_file_path_mapping = os.path.join(output_folder_path, output_file_name_mapping)
    print("output_file_path_mapping:{}".format(output_file_path_mapping))
    
    count = 1
    
    with open(input_file_path, 'r') as inputfile:
        csvreader = csv.reader(inputfile)
        ncs = [nc for nc in csvreader]
    
    with open(output_file_path_energy, 'w', newline = '') as output_file_energy,\
         open(output_file_path_timing, 'w', newline = '') as output_file_timing,\
         open(output_file_path_minnode, 'w', newline = '') as output_file_minnode,\
         open(output_file_path_mapping, 'w', newline = '') as output_file_mapping:
        csvwriter_energy = csv.writer(output_file_energy, quoting = csv.QUOTE_MINIMAL) 
        csvwriter_timing = csv.writer(output_file_timing, quoting = csv.QUOTE_MINIMAL)
        csvwriter_minnode = csv.writer(output_file_minnode, quoting = csv.QUOTE_MINIMAL)
        csvwriter_mapping = csv.writer(output_file_mapping, quoting = csv.QUOTE_MINIMAL)

        header_energy = ['']
        header_timing = ['']
        header_minnode = ['']
        header_mapping = ['']
        for j in range(len(ncs)): # j is column number
            NXGraph_G2 = code_to_networkx_script_for_experiment.parse_ast_to_networkx_graph(ast.parse(ncs[j][1]))
            col = ncs[j][0] + "(" + str(NXGraph_G2.number_of_nodes()) + ")" 
            #header.append(ncs[j][0])
            header_energy.append(col)
            header_timing.append(col)
            header_minnode.append(col)
            header_mapping.append(col)

        csvwriter_energy.writerow(header_energy)
        csvwriter_timing.writerow(header_timing)
        csvwriter_minnode.writerow(header_minnode)
        csvwriter_mapping.writerow(header_mapping)
        
        for i in range(len(ncs)): # i is row number
            data_energy = []
            data_timing = []
            data_minnode = []
            data_mapping = []
            for j in range(i + 1): # j is column number
                
                print(ncs[i][0],",", ncs[j][0])
                print(ncs[i][1])
                print(ncs[j][1])

                NXGraph_G1 = code_to_networkx_script_for_experiment.parse_ast_to_networkx_graph(ast.parse(ncs[i][1]))
                NXGraph_G2 = code_to_networkx_script_for_experiment.parse_ast_to_networkx_graph(ast.parse(ncs[j][1]))
                print(f'Isomorphic? {nx.is_isomorphic(NXGraph_G1, NXGraph_G2)}')
                # THE SUBGGRAPH ISOMORPHISM Problem Implemented for Quantum Code Clone Detection Solved on the DWave
                if NXGraph_G1.number_of_nodes() >= NXGraph_G2.number_of_nodes():
                    resG1, resG2, sampleset = sgi_qccd_H1_for_experiment.find_isomorphism(NXGraph_G1, NXGraph_G2) 
                    print("\nMappping {0} with {1} nodes onto {2} with {3} nodes".format(ncs[j][0], NXGraph_G2.number_of_nodes(), ncs[i][0], NXGraph_G1.number_of_nodes()))
                else:
                    resG1, resG2, sampleset = sgi_qccd_H1_for_experiment.find_isomorphism(NXGraph_G2, NXGraph_G1)
                    print("\nMappping {0} with {1} nodes onto {2} with {3} nodes".format(ncs[i][0], NXGraph_G1.number_of_nodes(), ncs[j][0], NXGraph_G2.number_of_nodes()))
                
                best_mapping = sampleset.first.sample # the resultant mapping obtained form the annealing process (Could store 5 of these for averging out the result by running the script 5 times)
                best_mapping_energy = sampleset.first.energy 
                qpu_access_time = sampleset.info["qpu_access_time"]
                
                G1_nodes = list(resG1.nodes)
                print("Corresponding mapping:{}".format(best_mapping))
                updated_best_mapping = {k: G1_nodes[v] for k, v in best_mapping.items()}
                print("\nupdated_best_mapping:{}".format(updated_best_mapping))
                data_energy.append(best_mapping_energy)
                data_timing.append(qpu_access_time)
                data_minnode.append(min(resG1.number_of_nodes(), resG2.number_of_nodes()))
                data_mapping.append(updated_best_mapping)
                print("Energy: {0}, Timing: {1}, Minimum Node:{2}".format(data_energy, data_timing, data_minnode))
                print(len(data_energy))

                time.sleep(5)
                count += 1
            print("--x--")
            row_energy = [ncs[i][0] + "(" + str(NXGraph_G1.number_of_nodes()) + ")"] + data_energy
            csvwriter_energy.writerow(row_energy)
            row_timing = [ncs[i][0] + "(" + str(NXGraph_G1.number_of_nodes()) + ")"] + data_timing
            csvwriter_timing.writerow(row_timing)
            row_minnode = [ncs[i][0] + "(" + str(NXGraph_G1.number_of_nodes()) + ")"] + data_minnode
            csvwriter_minnode.writerow(row_minnode)
            row_mapping = [ncs[i][0] + "(" + str(NXGraph_G1.number_of_nodes()) + ")"] + data_mapping
            csvwriter_mapping.writerow(row_mapping)
