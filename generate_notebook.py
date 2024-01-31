import nbformat
from nbconvert.preprocessors import ExecutePreprocessor
from nbformat.v4 import new_notebook, new_code_cell, new_markdown_cell
import re
import sys
import os
import inspect
import importlib.util

# Utility function to geberate function calls with arguments
def generate_function_call_with_defaults(function_name, module):
    import inspect
    function = getattr(module, function_name)
    sig = inspect.signature(function)
    args_str = []
    for name, param in sig.parameters.items():
        if param.default is inspect.Parameter.empty:
            args_str.append(name)
        else:
            default_value = repr(param.default)
            args_str.append(f"{name}={default_value}")
    return f"{function_name}({', '.join(args_str)})"

# Load the module dynamically
module_name = 'eda_functions'
module = importlib.import_module(module_name)

# Get the CSV file name from the command line arguments
csv_file = sys.argv[1]

# Create a new notebook object
nb = new_notebook()

python_file_path = os.path.join('./', 'eda_functions.py')

# Get import statements from eda_functions.py
def get_import_statements(python_file_path):
    import_statements = []
    with open(python_file_path, 'r') as file:
        for line in file:
            if line.startswith('import ') or line.startswith('from '):
                import_statements.append(line.strip())
            else:
                break
    return import_statements

import_statements = get_import_statements(python_file_path)
imports_cell_content = '\n'.join(import_statements)
nb.cells.append(new_code_cell(imports_cell_content))

# Import all functions from module_name
nb.cells.append(new_code_cell(f"from {module_name} import *"))

def add_markdown_blocks_with_functions(python_file_path, notebook, csv_file):
    with open(python_file_path, 'r') as file:
        content = file.read()

    # Split the content by function definitions and markdown blocks
    pattern = re.compile(r'# === Markdown Start ===\n(.*?)# === Markdown End ===\n(.*?)def\s+(\w+)\(', re.DOTALL)
    matches = pattern.findall(content)

    first_function_name = get_first_function_name(python_file_path)
    
    for match in matches:
        markdown_content, function_def, function_name = match
        # Clean up the markdown content
        markdown_content = re.sub(r'^#\s?', '', markdown_content, flags=re.MULTILINE).strip()
        # Add markdown cell to the notebook
        notebook.cells.append(new_markdown_cell(markdown_content))
        
        # Determine the appropriate code cell content
        if function_name == first_function_name:
            code_cell_content = f"df = {function_name}('{csv_file}')"
            notebook.cells.append(new_code_cell(code_cell_content))
        else:
            #code_cell_content = f"{function_name}(df)"
            function_call_string = generate_function_call_with_defaults(function_name, module)
            notebook.cells.append(new_code_cell(function_call_string))
        # Add code cell for the function
        #notebook.cells.append(new_code_cell(code_cell_content))

# Get first function name from eda_functions.py
def get_first_function_name(module_path):
    spec = importlib.util.spec_from_file_location("module.name", module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    functions = inspect.getmembers(module, inspect.isfunction)
    first_function_name = functions[0][0] if functions else None
    return first_function_name

# Call the function to add markdown blocks and functions to the notebook
add_markdown_blocks_with_functions(python_file_path, nb, csv_file)

# Define the path for the new notebook
notebook_path = os.path.join(os.getcwd(), "generated_notebook.ipynb")

# Check if the notebook aleady exists and delete it if it does
if os.path.exists(notebook_path):
    os.remove(notebook_path)
    print(f"Deleted existing notebook: {notebook_path}")

# Write the notebook to the file
with open(notebook_path, 'w', encoding='utf-8') as f:
    nbformat.write(nb, f)

def execute_notebook(notebook_path):
    with open(notebook_path) as f:
        nb = nbformat.read(f, as_version=4)
    ep = ExecutePreprocessor(timeout=600, kernel_name='python3')
    ep.preprocess(nb, {'metadata': {'path': './'}})
    with open(notebook_path, 'wt') as f:
        nbformat.write(nb, f)

# Execute the notebook
execute_notebook(notebook_path)

# Open JupyterLab with the newly created notebook
os.system(f"jupyter lab {notebook_path}")
