"""
(Did not need to use this separate script as I integrated all the functionality of this into the conductor script to make things simpler and smoother)
Semi-Final Script. Works perfectly well but not used in the Final version of the Experiment.
Final Script is 'Working Code to Use' Folder with the other scripts and the conductor script. 


Script to Log data about every experiment
References:
- https://stackoverflow.com/questions/35992556/storing-and-analysing-experimental-data-in-efficient-way-sql-python
- https://codeburst.io/copy-pastable-logging-scheme-for-python-c17efcf9e6dc
- https://www.geeksforgeeks.org/exporting-pandas-dataframe-to-json-file/
- https://www.projectpro.io/recipes/save-pandas-dataframe-as-csv-file

"""
# Importing Stuff
import time
import os
import datetime
import pandas as pd

def store_experiment_data(result_data_for_csv, columns, file_url):
    df_for_csv = pd.DataFrame(result_data_for_csv, columns = columns)
    df_for_csv.to_csv(file_url, index = True)
    print("File saved!")

def retreive_experiment_data(file_url):
    df_from_csv = pd.read_csv(file_url)
    print(df_from_csv)


if __name__ == "__main__":

    """ Creating a data dictionary to store """
    # Coudl store it as a JSON or a CSV or a Python Dictionary Object however we want
    # using the 'json' library or Pandas

    n1 = 28 # placeholder value for 'number of nodes in G1'
    n2 = 11 # placeholder value for 'number of nodes in G2'
    e1 = 50 # placeholder value for 'number of edges in G1'
    e2 = 20 # placeholder value for 'number of edges in G2'
    clone_type = 1 # could be Type 1, 2, or 3 clone depending on the input codes. 
    key = "G1(" + str(n1) + ")_G2(" + str(n2) + ")_type_" + str(clone_type) + "_clone"  # example: "G1(32)_G2(28)_type_1_clone"
    experiment_label =  'qccd_H1_experiment_result_data_' + key
    dwave_leap_problem_id = "0e9f2a89-a536-4d48-9ab2-42bf76e2c7be" # get DWave problem ID from 'testing_and_evaluation_Script'
    best_mapping = {17: 8, 18: 18, 19: 3, 20: 20, 21: 9, 22: 4, 23: 22, 24: 11, 25: 21, 26: 26, 27: 6} # the resultant mapping obtained form the annealing process (Could store 5 of these for averging out the result by running the script 5 times) 
    # mapping_energy =
    runtime = 4944170 # placeholder value for time, in microseconds, of the run time (see description of runtime in Notes and 'testing_and_evaluation_script')
    charge_time = 5000000 # placeholder value for time, in microseconds, of the charge time (see description of chargetime in Notes and 'testing_and_evaluation_script')
    qpu_access_time = 180000 # placeholder value for time, in microseconds, of the qpu access time (see description of qpu access time in Notes and 'testing_and_evaluation_script')
    no_annealing_cycles = 100 # placeholder valuefor 'number of annealing cycles'
    duration_per_anneal_cycle = 20 # placeholder value, in microseconds, for the 'duration of each anneal cycle'
    # solver_information = Commented out because there a re a lot of data points, they are present in the 'testing_and_evaluation_script' 

    columns = [
        'experiment label', 
        'key', 
        'number of nodes in G1', 
        'number of edges in G1', 
        'number of nodes in G2', 
        'number of edges in G2',
        'clone type', 
        'dwave leap problem id', 
        'best mapping from G2 to G1', 
        'runtime', 
        'charge time', 
        'qpu access time', 
        'number of annealing cycles',
        'duration per anneal cycle'
    ]

    result_data_for_csv = {
        'experiment label': [experiment_label], 
        'key': [key], 
        'number of nodes in G1': [n1],
        'number of edges in G1': [e1], 
        'number of nodes in G2': [n2], 
        'number of edges in G2': [e2],
        'clone type': [clone_type], 
        'dwave leap problem id': [dwave_leap_problem_id],
        'best mapping from G2 to G1': [best_mapping], 
        'runtime': [runtime],
        'charge time': [charge_time],
        'qpu access time': [qpu_access_time], 
        'number of annealing cycles': [no_annealing_cycles],
        'duration per anneal cycle': [duration_per_anneal_cycle]
    }
            
    # JSON
    """
    result_data_for_json = [[
        experiment_label, key, n1, e1, n2, e2, isomorphic_pair, 
        dwave_leap_problem_id, mapping, runtime, charge_time, 
        qpu_access_time, no_annealing_cycles, duration_per_anneal_cycle]]

    df_for_json = pd.DataFrame(result_data_for_json, columns = columns)
    df_for_json.to_json(experiment_label + '.json', orient = 'split', compression = 'infer', index = 'true')

    df_from_json = pd.read_json(experiment_label + '.json', orient ='split', compression = 'infer')
    # print(df_from_json)
    """

    # CSV
    # Storing Experiment log data
    folder_url = '/Users/samyakjhaveri/Desktop/Drive Folder/Research/USC Internship Quantum Virtual Network Embedding Project 2022/Experiment Result Data'
    store_experiment_data(result_data_for_csv, columns, folder_url)

    """
    # Retreiving Experiment log data
    file_url = folder_url + '/' + result_data_for_csv['experiment label'][0] + '.csv'
    retreive_experiment_data(file_url)
    """


""" References:
- https://stackoverflow.com/questions/35992556/storing-and-analysing-experimental-data-in-efficient-way-sql-python
- https://codeburst.io/copy-pastable-logging-scheme-for-python-c17efcf9e6dc
- https://www.geeksforgeeks.org/exporting-pandas-dataframe-to-json-file/
- https://www.projectpro.io/recipes/save-pandas-dataframe-as-csv-file
"""