import ast 
import astpretty

code_url = "/home/samyaknj/Research/UCI Quantum Code Clone Detection Project/Dataset/sample4/sample4_type1_v1.py"
with open(code_url, 'r') as f:
    code = f.read()
print(ast.parse(code))
print(astpretty.pprint(ast.parse(code)))
