# Automate-EDA

Automate-EDA is a repository dedicated to providing scripts and tools for automating the process of Exploratory Data Analysis (EDA). This project aims to streamline the initial data analysis phase, making it quicker and more efficient for data scientists and analysts. Thus, it would save time on repetitive tasks when working from one dataset to the next and there is always a need to explore the data, mostly using the same codes.

## Features

- **Dynamic Function Execution**: Automatically execute EDA functions from a specified Python module.
- **Notebook Generation**: Dynamically generate Jupyter Notebooks with pre-filled EDA code blocks.
- **Flexible Data Input**: Process CSV file dynamically, applying EDA functions directly to your dataset.
- **Customizable Workflow**: Easily extendable to include more complex EDA functions and data visualizations.

## Getting Started

### Prerequisites

Ensure you have Python 3.x installed on your system along with JupyterLab. This project also requires `pandas`, `nbformat`, and `nbconvert`.

You can install the required packages using:

```bash
pip install pandas nbformat nbconvert jupyterlab
```
### Installation
Clone this repository to your local machine:
```bash
git clone https://github.com/pouriaetab/automate-eda.git
cd automate-eda
```
### Usage
1. **Prepare Your EDA Functions Or Utilize the Default Functions**: To get started, you can either place your custom EDA functions in a Python file (e.g., eda_functions.py), making sure that the first function is tailored to read a CSV file and return a pandas DataFrame. Alternatively, you have the option to directly utilize the default functions provided.

2. **Generate and Execute Notebook**: Run the provided script with the name of your CSV file as an argument to generate and execute a Jupyter Notebook:

```bash
python3 generate_notebook.py your_dataset.csv
```

### Contributing
Please feel free to submit issues, pull requests, or suggestions to enhance the functionality or documentation.

### License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.






