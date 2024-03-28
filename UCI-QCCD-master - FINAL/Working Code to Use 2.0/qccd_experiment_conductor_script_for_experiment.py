"""
Final Working Script to be used for Experiments. 

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
import dwave.inspector
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

def generate_code_clone_graph(G1_file_path, output_path, clone_type):
    """
    Function to generate a NetworkX Graph of the given input code, 
    based on the the type of clone that the user wants to generate. 

    Arguments:
    - G1_file_path: File path location of the code file you want to generate a clone of
    - (seems redundant, can remove?) output_path: File path location where you want to 
    store the output code clone generated
    - clone_type: The type of clone that is requested to be generated of the the 
    given input source code. 

    Returns:
    - NXGraph_G1: NetworkX Graph version of the input source Code 
    - NXGraph_G2: NetworkX Graph version of the type <clone_type> code clone of the the input Source code file
    """

    print("\nSTART OF TYPE {} ------------------------".format(clone_type))
    if clone_type == 1:
        code_clone_ast = type1.create_type_1_clone(G1_file_path, output_path)   
    elif clone_type == 2:
        code_clone_ast = type2.create_type_2_clone(G1_file_path, output_path)
    elif clone_type == 3:
        code_clone_ast = type3.create_type_3_clone(G1_file_path, output_path)
    print("END OF TYPE {} --------------------------\n".format(clone_type))

    # Generating Network X Graphs of the Original Code and the Code Clone 
    # by converting them into ASTs as per our way 
    NXGraph_G1 = code_to_networkx_script_for_experiment.parse_ast_to_networkx_graph(ast.parse(code_to_networkx_script_for_experiment.get_code_from_storage(G1_file_path)))
    NXGraph_G2 = code_to_networkx_script_for_experiment.parse_ast_to_networkx_graph(code_clone_ast)
    return NXGraph_G1, NXGraph_G2

if __name__ == "__main__":
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--ogcodefile', help = 'The Original Code File you want to generate clone of and test on the QCCD', type = str)
    parser.add_argument('--clonecodefile', help = 'Code Clone Type', type = str)
    args = parser.parse_args()
    """
    """
    # Output directory for all files
    _OUTPUT_DIR = '/Users/samyakjhaveri/Desktop/Drive Folder/Research/UCI Quantum Code Clone Detection Project/Experiment Result Data/'
    _TYPE_1_OUTPUT_DIR = 'type1'
    _TYPE_2_OUTPUT_DIR = 'type2'
    _TYPE_3_OUTPUT_DIR = 'type3'

    # Create output directory if it doesn't exist
    type1_output_path = os.path.join(_OUTPUT_DIR, _TYPE_1_OUTPUT_DIR)
    type2_output_path = os.path.join(_OUTPUT_DIR, _TYPE_2_OUTPUT_DIR)
    type3_output_path = os.path.join(_OUTPUT_DIR, _TYPE_3_OUTPUT_DIR)
    if not os.path.exists(_OUTPUT_DIR):
        os.makedirs(_OUTPUT_DIR)
        os.makedirs(type1_output_path)
        os.makedirs(type2_output_path)
        os.makedirs(type3_output_path)
    """
    """
    # OG Code = Larger Code = Target Graph = Main Graph
    # Example of G1_file_url = '/Users/samyakjhaveri/Desktop/Drive Folder/Research/UCI Quantum Code Clone Detection Project/Graph - Subgraph test codes/test_graph_code.py'
    G1_file_path = args.ogcodefile
    # G1_file_path = os.path.join(G1_folder_path, G1_filename)
    G2_file_path = args.clonecodefile

    NXGraph_G1 = code_to_networkx_script_for_experiment.parse_ast_to_networkx_graph(ast.parse(code_to_networkx_script_for_experiment.get_code_from_storage(G1_file_path)))
    NXGraph_G2 = code_to_networkx_script_for_experiment.parse_ast_to_networkx_graph(ast.parse(code_to_networkx_script_for_experiment.get_code_from_storage(G2_file_path)))
    """
    """
    clone_type = int(args.clone_type)
    if clone_type == 1:
        NXGraph_G1, NXGraph_G2 = generate_code_clone_graph(G1_file_path, type1_output_path, 1)
    elif clone_type == 2:
        NXGraph_G1, NXGraph_G2 = generate_code_clone_graph(G1_file_path, type2_output_path, 2)
    elif clone_type == 3:
        NXGraph_G1, NXGraph_G2 = generate_code_clone_graph(G1_file_path, type3_output_path, 3)    
    """
        
    """
    Printing Basic Information about the two Graphs
    """
    """
    print("Number of NODES in Larger Code:{}".format(NXGraph_G1.number_of_nodes()))
    print("Number of EDGES in Larger Code:{}".format(NXGraph_G1.number_of_edges()))

    print("Number of NODES in Smaller Code:{}".format(NXGraph_G2.number_of_nodes()))
    print("Number of EDGES in Smaller Code:{}".format(NXGraph_G2.number_of_edges()))

    print("G1 Graph - Original Code: {}".format((NXGraph_G1)))  
    print("G2 Graph - Code Clone: {}".format((NXGraph_G2)))
    
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
    
    # plt.savefig(os.path.splitext(G2_file_path)[0] + ".png")
    plt.show() # is commented out so that it doesn't interrupt the flow of the experiment
    """
    """ THE SUBGGRAPH ISOMORPHISM Problem Implemented for Quantum Code Clone Detection Solved on the DWave """
    """
    G1, G2, sampleset = sgi_qccd_H1_for_experiment.find_isomorphism(NXGraph_G1, NXGraph_G2) 
    sgi_qccd_H1_for_experiment.present_results(G1, G2, sampleset)
    
    # Here, `annealing_results` in the form of 
    # [G1, G2, results] - A list which has 
    #   First element - G1 graph
    #   Second element - G2 graph
    #   Third Element - results - Resultant mappings from 
    # G2 graph to G2 graph
    # Made a separate `annealing_results` object so that I could use it with the last step of 
    # 'Storing the results and generating a report of each experiment`
    

    # Saving the Results 
    logging_result_data_folder_path = '/Users/samyakjhaveri/Desktop/Drive Folder/Research/UCI Quantum Code Clone Detection Project/Experiment Result Data'
    logging_result_data_file_path = logging_result_data_folder_path + 'qccd_H1_experiment_result_data.csv'
    """
    """ Testing and Evaluating the Results """    
    """
    n1 = G1.number_of_nodes() # 'number of nodes in G1'
    n2 = G2.number_of_nodes() # 'number of nodes in G2'
    e1 = G1.number_of_edges() # 'number of edges in G1'
    e2 = G2.number_of_edges() # 'number of edges in G2'
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
        'best mapping energy',
        'runtime', 
        'charge time', 
        'qpu access time', 
        'dwave leap problem id',
        'number of annealing cycles',
        'duration per anneal cycle'
    ]

    result_data_for_csv = [{
        'key': key,
        'experiment label': experiment_label,  
        'number of nodes in G1': n1,
        'number of edges in G1': e1, 
        'number of nodes in G2': n2, 
        'number of edges in G2': e2,
        'clone type': clone_type, 
        'best mapping from G2 to G1': best_mapping, 
        'best mapping energy': best_mapping_energy,
        'runtime': runtime,
        'charge time': charge_time,
        'qpu access time': qpu_access_time, 
        'dwave leap problem id': dwave_leap_problem_id,
        'number of annealing cycles': no_annealing_cycles,
        'duration per anneal cycle': duration_per_anneal_cycle
        }]


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

# ---------- x ---------- x ---------- x ---------- 
    """ Part of the experiment conductor for conducting experiments o n the generated programs.csv dataset, 
    on the server(styx or openlab)"""
    absolute_path = os.path.split(os.getcwd())[0]
    print(absolute_path)
    #inputfile_relative_path = "programs.csv"
    inputfile_relative_path = "programs.csv"
    inputfilepath = os.path.join(absolute_path, inputfile_relative_path)
    same_results1_relative_path = "same_results1.csv"
    same_results1_file_path = os.path.join(absolute_path, same_results1_relative_path)
    same_results2_relative_path = "same_results2.csv"
    same_results2_file_path = os.path.join(absolute_path, same_results2_relative_path)
    same_results3_relative_path = "same_results3.csv"
    same_results3_file_path = os.path.join(absolute_path, same_results3_relative_path)
    diff_results1_relative_path = "diff_results1.csv"
    diff_results1_file_path = os.path.join(absolute_path, diff_results1_relative_path)
    diff_results2_relative_path = "diff_results2.csv"
    diff_results2_file_path = os.path.join(absolute_path, diff_results2_relative_path)
    diff_results3_relative_path = "diff_results3.csv"
    diff_results3_file_path = os.path.join(absolute_path, diff_results3_relative_path)
    bigresults_relative_path = "bigresults.csv"
    bigresults_file_path = os.path.join(absolute_path, bigresults_relative_path)
    
    # inputfilepath = os.path.abspath(inputfilepath)
    print("inputfilepath:{}".format(inputfilepath))
    data = []
    count = 1
    columns = [
            'experiment label', 
            'number of nodes in G1', 
            'number of edges in G1', 
            'number of nodes in G2', 
            'number of edges in G2', 
            'best mapping energy',
            'best mapping from G2 to G1', 
            'runtime', 
            'charge time', 
            'qpu access time', 
            'dwave leap problem id',
    ]

    with open(inputfilepath, 'r') as inputfile:
        csvreader = csv.reader(inputfile)
        ncs = [nc for nc in csvreader]
    inputfile.close()
    for i in range(len(ncs)):
        for j in range(i + 1, len(ncs)):
            print(ncs[i][1])
            print(ncs[j][1])
            NXGraph_G1 = code_to_networkx_script_for_experiment.parse_ast_to_networkx_graph(ast.parse(ncs[i][1]))
            NXGraph_G2 = code_to_networkx_script_for_experiment.parse_ast_to_networkx_graph(ast.parse(ncs[j][1]))
            """ THE SUBGGRAPH ISOMORPHISM Problem Implemented for Quantum Code Clone Detection Solved on the DWave """
            G1, G2, sampleset = sgi_qccd_H1_for_experiment.find_isomorphism(NXGraph_G1, NXGraph_G2) 
            #sgi_qccd_H1_for_experiment.present_results(G1, G2, sampleset)
            """
            n1 = G1.number_of_nodes() # 'number of nodes in G1'
            n2 = G2.number_of_nodes() # 'number of nodes in G2'
            e1 = G1.number_of_edges() # 'number of edges in G1'
            e2 = G2.number_of_edges() # 'number of edges in G2'
            key = ncs[i][0] + "with" + [j][0]
            # experiment_label =  'qccd_H1_experiment_result_data_' + key
            """
            best_mapping = sampleset.first.sample # the resultant mapping obtained form the annealing process (Could store 5 of these for averging out the result by running the script 5 times)
            best_mapping_energy = sampleset.first.energy 
            """
            runtime = sampleset.info["run_time"] # time, in microseconds, of the run time (see description of runtime in Notes and 'testing_and_evaluation_script')
            charge_time = sampleset.info["charge_time"] # time, in microseconds, of the charge time (see description of chargetime in Notes and 'testing_and_evaluation_script')
            qpu_access_time = sampleset.info["qpu_access_time"] # time, in microseconds, of the qpu access time (see description of qpu access time in Notes and 'testing_and_evaluation_script')
            dwave_leap_problem_id = sampleset.info["problem_id"] # get DWave problem ID from 'testing_and_evaluation_Script'
            result_data_for_csv = [{
                # 'experiment label': experiment_label,  
                'key': key,
                'number of nodes in G1': n1,
                'number of edges in G1': e1, 
                'number of nodes in G2': n2, 
                'number of edges in G2': e2,
                'best mapping energy': best_mapping_energy, 
                'best mapping from G2 to G1': best_mapping, 
                'runtime': runtime,
                'charge time': charge_time,
                'qpu access time': qpu_access_time, 
                'dwave leap problem id': dwave_leap_problem_id,
                }]
            """
            row = [ncs[i][0], ncs[j][0], best_mapping_energy]
            G1_nodes = list(G1.nodes)
            print("Corresponding mapping:{}".format(best_mapping))
            updated_best_mapping = {k: G1_nodes[v] for k, v in best_mapping.items()}
            print("\nupdated_best_mapping:{}".format(updated_best_mapping))
            data.append(row)
            print(data)
            print(len(data))
            time.sleep(5)        
            count += 1
        print("--x--")

    print(count)
    with open(bigresults_file_path, 'w', newline = '') as output_file:
        print("inside bigresults.csv")
        csvwriter = csv.writer(output_file, quoting = csv.QUOTE_MINIMAL)   
        for row in data:
            print("writing to bigresults.csv")
            csvwriter.writerow(row) 