"""
ast.NodeTransformer is a subclass of ast.NodeVisitor that walks through an ast tree 
and can apply transformations to any node in the tree.

NodeTransformer allows you to override the visit methods, and modifying the 
method’s return value allows you to transform the node as the programmer wishes. 
If the return value is set to None, then that node is removed from the tree. 
If no replacement is done to the return value, the return value will be the original node.
"""



# from logic.common import construct_output_file
from logic.common import construct_output_file
import ast 
import astunparse
import random 
import sys
import string
# import args 
# import argv
import argparse

class ChangeConstantValue(ast.NodeTransformer):
    def visit_Constant(self, node):
        new_value = random.randint(0, 1000)
        new_node = ast.Constant(new_value)
        print("Replacing constant {} --> {} at line number {}.".format(node.value, new_value, node.lineno))
        return new_node

class ChangeVariableName(ast.NodeTransformer):
    def __init__(self):
        self.variables = {} # {old_variable name: new_variable_name}
    
    def visit_Name(self, node):
        # names = sorted({node.id for node in ast.walk(root) if isinstance(node, ast.Name)})
        
        if node.id not in self.variables.keys():
            new_var_name = node.id + "_" + random.choice(string.ascii_letters)
            self.variables[node.id] = new_var_name
            return ast.Name(**{**node.__dict__, 'id':new_var_name})
        elif node.id in self.variables.keys():
            return ast.Name(**{**node.__dict__, 'id':self.variables[node.id]})            

        # return copy_location(, node)
    

# def create_type_2_clone(tree):
def create_type_2_clone(file_path, output_path):
    """
    Function to get Code file of a given file_url from the Storage
    and manipulate its AST to generate its Type 2 Clone 
    Args:
        - file_path of Original Code
        - output_path
    Returns: 
        - Modified AST  
    """  
    with open(file_path, 'r') as fin:
        srcCode = fin.read()
    fin.close()
    
    tree = ast.parse(srcCode)
    mod_tree = tree
    cvn = ChangeVariableName()
    mod_tree = cvn.visit(mod_tree)

    print("Original Code:")
    print(srcCode)
    print("AST of Original Code:")
    print(ast.dump(tree, indent = 4))
    print("Type 2 Code Clone in Code form (Variable Name Changed):")
    # print("Type 2 Code Clone in Code form (Constant Value Changed):")
    print(ast.unparse(mod_tree))
    print("Type 2 Clone's AST (Variable Name Changed):")
    print(ast.dump(mod_tree, indent = 4))
    # Have two options here:
    # 1. Store the AST 'mod_tree' in the 'output_path' path 
    #    and return that 'output_path' back to the experiment conductor
    # 2. (going with this option for now) Return the `mod_tree` AST directly to the experiment conductor 
    #    without storing it anywhere.
    return mod_tree

if __name__ == "__main__":
    print("Please enter the filepath you want to generate the type 2 clone of:")
    #file_path = sys.argv[1]
    parser = argparse.ArgumentParser()
    parser.add_argument('--file_path', help = 'the file path of the code you want to generate type 2 clone of', type = str)
    args = parser.parse_args()

    create_type_2_clone(convert_code_to_ast(args.file_path))