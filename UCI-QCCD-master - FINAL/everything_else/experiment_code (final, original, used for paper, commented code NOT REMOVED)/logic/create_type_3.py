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


class RemoveName(ast.NodeTransformer):
    """
    Class that has method that can remove a statement from the AST of a code
    """

    def visit_Name(self, node):
        """
        Function that Removes a Node from the AST
        """
        print("inside visit_Name() to remove a node")
        return None


class RemoveForLoop(ast.NodeTransformer):
    """This class has methods that can remove a For Loop from a code

    How to use these functions:"
    t = MyTransformer()
    mod_tree = t.visit(tree)
    mod_tree = ast.fix_missing_locations(mod_tree) to fix the
    locations of the line nos. in the ast

    Compiling the code:
    print("computing...")
    codeobj = compile(mod_tree, '<string>', 'exec')
    exec(codeobj)
    """

    def iterate_children(self, node):
        print("inside iterate_childen()")
        """
        helper
        """
        children = ast.iter_child_nodes(node)
        for c in children:
            self.visit(c)

    def generic_visit(self, node):
        print("inside generic_visit()")
        """
        default behaviour
        """
        super().generic_visit(node)
        print("Visiting:", node.__class__.__name__)
        self.iterate_children(node)
        return node

    def visit_For(self, node):
        """
        For nodes: replace with nothing
        """
        print("inside visit_For()")
        print("Removing a For Loop Node")
        return None


class RemoveAssignmentStatement(ast.NodeTransformer):
    """
    Class that has two functions are to remove Assignment operations
    """

    def visit_Assign(Self, node):
        return None

    def visit_AugAssign(self, node):
        return None


class RemoveFunctionCallStatement(ast.NodeTransformer):
    """
    Removing a Function Call
    """

    def visit_Call(self, node, func):
        print("inside visit_Call")
        # here, func = name of the particualr function whose
        # occuerences you want to remove from the code's AST
        # How to use this function :
        # new_tree = RemoveMethod('bar').visit(tree) where
        # `bar` is the name of the function you want to remove
        transform = node
        try:
            if node.func.attr == func:
                if not len(node.args):
                    transform = node.func.value
        except AttributeError:
            pass
        return ast.copy_location(transform, node)


class ChangeBinOpToMultStatement(ast.NodeTransformer):
    """
    Class that has Methods that can Change/ Modify the Statements from the AST of a code

    In this example, changing the `Add` BinOp operation to `Mult` BinOp operation.
    Everything else including the variable names stays the same for this particular
    example, but in a Type 3 clone, variable names and constant values can be changed as
    well. In some cases, the order in which the variables appear, or the operations
    take places in a single statement or the ordering of the statement itself can be
    different in a type 3 clone.

    """

    def visit_BinOp(self, node):
        """
        Function that can Change a Binary Operation to Multiplication
        """
        print(node.__dict__)
        node.op = ast.Mult()
        print(node.__dict__)
        return node

    # Could add a method that changes the datatype of the variable


# def create_type_3_clone(tree):
def create_type_3_clone(file_path, output_path):
    """
    Function to get Code file of a given file_url from the Storage
    Args:
        - file_url
    Returns:
        - Code file
    """
    with open(file_path, "r") as fin:
        srcCode = fin.read()
    fin.close()

    tree = ast.parse(srcCode)
    mod_tree = tree

    """
    #1
    rn = RemoveName()
    # `rs` is object of `RemoveStatement` class that is used to 
    # remove statements from the AST of the input code
    mod_tree = rn.visit(mod_tree)
    """
    # 2
    rfl = RemoveForLoop()
    # `rfl` is object of `RemoveForLoop` class that is used to
    # remove For Loops from the AST of the input code
    mod_tree = rfl.visit(mod_tree)
    """
    #3
    ras = RemoveAssignmentStatement()
    # `ras` is object of `RemoveAssignmentStatement` class that is used to 
    # remove assignemnt statements from the AST of the input code
    mod_tree = ras.visit(mod_tree)
    
    #4
    rfcs = RemoveFunctionCallStatement()
    # `rfcs` is object of `RemoveFunctionCallStatement` class that is used to 
    # remove Function Call statements from the AST of the input code
    mod_tree = rfcs.visit(mod_tree)
    
    #5
    cbotms = ChangeBinOpToMultStatement()
    # `cbotms` is object of `ChangeBinOpToMultStatement` class that is used to 
    # change the binary operations in the AST of an input code into Mult Binary Operation 
    mod_tree = cbotms.visit(mod_tree)
    """
    # mod_tree = ast.fix_missing_locations(mod_tree)

    print("Original Code:")
    print(srcCode)
    print("AST of Original Code:")
    print(ast.dump(tree, indent=4))
    print("Type 3 Code Clone in Code form:")
    print(ast.unparse(mod_tree))
    print("Type 3 Clone's AST:")
    print(ast.dump(mod_tree, indent=4))
    # Have two options here:
    # 1. Store the AST 'mod_tree' in the 'output_path' path
    #    and return that 'output_path' back to the experiment conductor
    # 2. (going with this option for now) Return the `mod_tree` AST directly to the experiment conductor
    #    without storing it anywhere.
    return mod_tree


if __name__ == "__main__":
    print("Please enter the filepath you want to generate the type 3 clone of:")
    # file_path = sys.argv[1]
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--file_path",
        help="the file path of the code you want to generate type 3 clone of",
        type=str,
    )
    args = parser.parse_args()

    create_type_3_clone(convert_code_to_ast(args.file_path))
