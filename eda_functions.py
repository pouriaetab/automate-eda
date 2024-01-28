import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns

# Load a CSV file into a DataFrame
def csv_to_df(df):
    """
    Converts a CSV file to a pandas DataFrame. Assumes the CSV file is in the current working directory.

    Parameters:
    - df: str, the name of the CSV file, for example train.csv.

    Returns:
    - DataFrame: The loaded pandas DataFrame.
    """
    # Construct the full path to the CSV file
    current_dir = os.getcwd() # Gets the current working directory
    csv_file_path = os.path.join(current_dir, df)
    df = pd.read_csv(csv_file_path)
    return df

# Display the first 5 rows of the DataFrame
def display_first_five_rows(df):
    """
    Displays the first 5 rows of the given DataFrame.

    Parameters:
    - df: DataFrame, the pandas DataFrame to display.

    Returns:
    - DataFrame: The first 5 rows of the given DataFrame.
    """
    return df.head()

# Display the first 5 rows of the DataFrame
def display_info(df):
    """
    Displays basic information about the given DataFrame.

    Parameters:
    - df: DataFrame, the pandas DataFrame to display.

    Returns:
    - NoneType: Baisc information about the given DataFrame.
    """
    return df.info()

# Display descriptive statistics about the DataFrame
def display_info(df):
    """
    Displays descriptive statistics about the given DataFrame.

    Parameters:
    - df: DataFrame, the pandas DataFrame to display.

    Returns:
    - DataFrame: The table of descriptive statistics about the given DataFrame.
    """
    return df.describe()

# Display info on columns with missing values
def null_columns(df):
    """
    Display columns with missing values, the total count, and the percentage of missing values in descending order.

    Parameters:
    - df (pd.DataFrame): The input DataFrame.

    Returns:
    None (prints text).
    """
    # Calculate the number of missing values for each column
    null_counts = df.isna().sum()

    # Calculate the percentage of missing values for each column
    null_percentage = (df.isna().sum() / len(df)) * 100

    # Combine counts and percentages into a DataFrame
    null_info = pd.DataFrame({'Count_Null': null_counts, 'Percentage': null_percentage})

    # Filter columns with missing values and sort them
    null_info = null_info[null_info['Count_Null'] > 0].sort_values(by=['Count_Null'], ascending=False)

    # Format the 'Percentage' column to two decimal places with a '%' sign
    null_info['Percentage'] = null_info['Percentage'].apply(lambda x: f"{x:.2f}%")
    
    # Display user-friendly message
    if not null_info.empty:
        print("Columns with missing values, their counts, and percentages (sorted):")
        print(null_info)
    else:
        print("No columns with missing values.")

