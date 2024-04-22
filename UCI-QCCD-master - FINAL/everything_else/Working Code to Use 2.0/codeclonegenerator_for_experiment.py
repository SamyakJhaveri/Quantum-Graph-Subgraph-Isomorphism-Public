"""
Final Working Script to be used for Experiments. 
"""

import sys
from sys import argv
import os
import argparse
import ast
import astunparse
from logic.common import construct_output_file
from logic import create_type_1 as type1, create_type_2 as type2, create_type_3 as type3
import pickle 

# Output directory for all files
_OUTPUT_DIR = 'output'
_TYPE_1_OUTPUT_DIR = 'type1_clones'
_TYPE_2_OUTPUT_DIR = 'type2_clones'
_TYPE_3_OUTPUT_DIR = 'type3_clones'

def access_stored_code_clone(code_clone_file_path):
    """
    Function to access ASTs of code clones stored in the `output` folder. Unpickle them. 
    Args:
        - code_clone_file_path: File Path of the Requested Code Clone that needs 
        to be accessed from storage
    Returns:
        - AST of the Code Clone stored in the File
    """
    try: 
        with open(code_clone_file_path, "rb") as f:
                print("Loaded {} pickle file from storage.".format(code_clone_file_path))
                return pickle.load(f)
    except Exception as ex:
            print("Error during unpickling object (Possible unsupported).", ex)

def store_code_clone(new_file_path, mod_code_clone_ast, code_clone_type):
    """
    Function to store the code clone 
    Args:
        - new_file_path: File path of the newly generated code clone ast file
        - mod_code_clone_ast: Modified AST of the Generated Code Clone
        - code_clone_type: The Type of Code Clone, as modified from the original code
    """
    try:
        with open(new_file_path, "wb") as nfp:
            pickle.dump(mod_code_clone_ast, nfp, protocol = pickle.HIGHEST_PROTOCOL)
            print("Stored AST of Type {} Code Clone as :{}.".format(code_clone_type, new_file_path))
    except Exception as ex:
        print("Error during pickling object (Possibly unsupported).", ex)

def main():
    print("Please enter the type of clone you want and the path to the file")
    parser = argparse.ArgumentParser()
    parser.add_argument("--t")
    parser.add_argument("--file_path")
    args = parser.parse_args()
    
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
    
    original_file_path = args.file_path

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
        print("Type 3 Code Clone AST:{}".format(type3_code_clone_ast))
        print("Type 3 Code Clone Output path:{}".format(type3_output_path))
        output_path = type3_output_path
        code_clone_type = 3
        mod_code_clone_ast = type3_code_clone_ast
        print("END OF TYPE 3 --------------------------\n")
    
    new_file_path = construct_output_file(original_file_path, output_path, code_clone_type)
    store_code_clone(new_file_path, mod_code_clone_ast, code_clone_type)    

if __name__ == '__main__':
    main()
