import os
import random
import ast

import astunparse
from logic.common import construct_output_file

def create_type_1_clone(original_file_path, output_path):
    """
    Function to get Code file of a given file_url from the Storage
    and manipulate its AST to generate its Type 1 Clone 
    Args:
        - file_path of Original Code
        - output_path
    Returns: 
        - Modified AST  
    """  

    with open(original_file_path, 'r') as fin:
        srcCode = fin.read()
    fin.close()
    
    
    # Parsing the code into its AST representation
    # and then unparsing it back into its code form
    # removes all the comments form the code automatically
    # This piece of code, with its comments removed
    # could be categorized as a Type 1 clone of the Original 
    # Code (ask Crista for validation)
    tree = ast.parse(srcCode)
    mod_tree = tree

    print("Original Code:")
    print(srcCode)
    print("AST of Original Code:")
    print(ast.dump(tree, indent = 4))
    print("Type 1 Code Clone in Code form:")
    print(ast.unparse(mod_tree))
    print("Type 1 Clone's AST:")
    print(ast.dump(mod_tree, indent = 4))

    G2_file_path = construct_output_file(original_file_path, output_path, 1)

    # Have two options here:
    # 1. Store the AST 'mod_tree' in the 'output_path' path 
    #    and return that 'output_path' back to the experiment conductor
    # 2. (going with this option for now) Return the `mod_tree` AST directly to the experiment conductor 
    #    without storing it anywhere.
    return mod_tree

"""
def create_type_1_clone(original_file_path, output_path):
    #original_file_path = os.path.join(folder_path, filename)
    with open(original_file_path) as fp:
        # print('\noriginal file name: ' + original_file_path)
        print(os.path.splitext(original_file_path))
        # Construct the output file
        print("Inside create_type_1")
        print("Original File Path:", original_file_path)
        print("output_path:", output_path)
        new_file_path = construct_output_file(original_file_path, output_path, 1)

        with open(new_file_path, 'w') as fw:
            print('printing clone of ' + original_file_path + ' to: ' + new_file_path)
            line = fp.readline()
            linenumber = 1
            newlinenumber = 1
            while line:
                random.randint(1, 5)
                if random.randint(1, 5) == 1:
                    print('Adding a newline at line #: ' + str(newlinenumber))
                    newlinenumber += 1
                    fw.write("\n")
                if not line.strip().startswith('#'):
                    fw.write(line)
                else:
                    print('Stripping in-line comment line #: ' + str(linenumber))
                line = fp.readline()
                newlinenumber += 1
                linenumber += 1
            print('finished printing clone of ' + original_file_path + ' to: type1clones/' + new_file_path + '.py')
    return new_file_path
"""