import nbformat
from nbconvert.preprocessors import ExecutePreprocessor
from nbformat.v4 import new_notebook, new_code_cell
import sys
import os
import inspect
import importlib.util

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


# Get first function name from eda_functions.py
def get_first_function_name(module_path):
    spec = importlib.util.spec_from_file_location("module.name", module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    functions = inspect.getmembers(module, inspect.isfunction)
    first_function_name = functions[0][0] if functions else None
    return first_function_name

first_function_name = get_first_function_name(python_file_path)

# Add a cell to load the CSV file using the first_function_name function
if first_function_name:
    nb.cells.append(new_code_cell(f"df = {first_function_name}('{csv_file}')"))

# Dynamically add cells for each function in the module
for name, obj in inspect.getmembers(module, inspect.isfunction):
    # Skip csv_to_df since it's already called
    if name == 'csv_to_df':
        continue
    # Create a cell for each function, assuming they take a DataFrame as the only argument
    nb.cells.append(new_code_cell(f"{name}(df)"))

# Define the path for the new notebook
notebook_path = os.path.join(os.getcwd(), "generated_notebook.ipynb")

# Write the notebook to the file
with open(notebook_path, 'w', encoding='utf-8') as f:
    nbformat.write(nb, f)

def execute_notebook(notebook_path):
    with open(notebook_path) as f:
        nb = nbformat.read(f, as_version=4)
    ep = ExecutePreprocessor(timeout=600, kernel_name='python3')
    ep.preprocess(nb, {'metadata': {'path': './'}})  # Adjust the path as needed
    with open(notebook_path, 'wt') as f:
        nbformat.write(nb, f)

# Execute the notebook
execute_notebook(notebook_path)

# Open JupyterLab with the newly created notebook
os.system(f"jupyter lab {notebook_path}")
