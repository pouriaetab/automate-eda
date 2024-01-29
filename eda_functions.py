import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# %load_ext autoreload
# %autoreload 2

# Define the maximum number of rows to display
# MAX_ROWS_TO_DISPLAY = 100

# === Markdown Start ===
# 
# **Load a CSV file into a DataFrame**
# === Markdown End ===
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

# === Markdown Start ===
# 
# **Display the first few rows of the DataFrame**
# === Markdown End ===
def display_first_few_rows(df):
    """
    Displays the first few rows of DataFrame.

    Parameters: 
    - df: DataFrame, the pandas DataFrame to display.

    Returns:
    - DataFrame: The first few rows of the given DataFrame.
    """
    return df.head(10)

# === Markdown Start ===
# 
# **Display basic information about the given DataFrame**
# === Markdown End ===
def display_info(df):
    """
    Displays basic information about the given DataFrame.

    Parameters:
    - df: DataFrame, the pandas DataFrame to display.

    Returns:
    - NoneType: Baisc information about the given DataFrame.
    """
    return df.info()

# === Markdown Start ===
# 
# **Display descriptive statistics about the DataFrame**
# === Markdown End ===
def display_descriptive_statistics(df):
    """
    Displays descriptive statistics about the given DataFrame.

    Parameters:
    - df: DataFrame, the pandas DataFrame to display.

    Returns:
    - DataFrame: The table of descriptive statistics about the given DataFrame.
    """
    return df.describe()

# === Markdown Start ===
# 
# **Display info on columns with missing values**
# === Markdown End ===
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

# === Markdown Start ===
# 
# **Display descriptive statistics about the DataFrame2**
# === Markdown End ===
def display_descriptive_statistics2(df):
    """
    Displays descriptive statistics about the given DataFrame.

    Parameters:
    - df: DataFrame, the pandas DataFrame to display.

    Returns:
    - DataFrame: The table of descriptive statistics about the given DataFrame.
    """
    return df.describe()

# === Markdown Start ===
# 
# **Display information on duplicated rows**
# === Markdown End ===
def duplicate_percentage(df):
    """
    Print the percentage of duplicated rows in a DataFrame.

    Parameters:
    - df: DataFrame, the input DataFrame.

    Returns:
    None (prints texts).
    """
    dup_sum = df.duplicated().sum()
    dup_pct = (dup_sum / len(df)) * 100
    print(f"Total duplicated rows: {dup_sum: .2f}. \nPercentage of duplicated rows: {dup_pct: .2f}%")


# === Markdown Start ===
# 
# **Display outliers**
# === Markdown End ===
def find_and_display_outliers(df, display_info=True):
    """
    Find and display outliers in non-binary and non-object columns of a DataFrame.

    Parameters:
    - df: DataFrame, the input DataFrame.
    - display_info: bool, set to True to print information, False to suppress printing.

    Returns:
    - None (prints texts about outlier)
    """
    # Select non-binary and non-object columns
    numeric_columns = df.select_dtypes(['float64', 'int64']).columns

    # Filter out binary features
    non_binary_columns = [col for col in numeric_columns if df[col].nunique() > 2]

    # Dictionaries to store lower and upper limits for each column
    lower_limits = {}
    upper_limits = {}
    
    for column_name in non_binary_columns:
        # Calculate 25th and 75th percentiles
        q25 = df[column_name].quantile(0.25)
        q75 = df[column_name].quantile(0.75)

        # Calculate interquartile range (IQR)
        iqr = q75 - q25

        # Define lower and upper limits for outliers
        lower_limit = q25 - 1.5 * iqr
        upper_limit = q75 + 1.5 * iqr

        # Identify rows containing outliers
        outliers = df[(df[column_name] < lower_limit) | (df[column_name] > upper_limit)]
        total_outliers = len(outliers)
        if total_outliers > 0:
            lower_limits[column_name] = lower_limit
            upper_limits[column_name] = upper_limit

        # Display information only if display_info is True and outliers are found
        if display_info and total_outliers > 0:
            print(f"\nColumn: '{column_name}'")
            print(f"25th Percentile: {q25}")
            print(f"75th Percentile: {q75}")
            print(f"IQR: {iqr}")
            print(f"Lower Limit for Outliers: {lower_limit}")
            print(f"Upper Limit for Outliers: {upper_limit}")
            print(f"Total Rows with Outliers: {total_outliers}")
    
    if display_info and total_outliers == 0:
        print("There are no outliers in any of the columns.")



# === Markdown Start ===
# 
# **Correlation heatmap**
# === Markdown End ===
def display_corr_heatmap(df):
    """
    Displays correlation heatmap of the given DataFrame, dynamically adjusting the figure size
    based on the number of numerical variables, with a limit of 100 numerical variables.

    If there are more than 100 numerical variables, informs the user about the number of omitted variables.

    Parameters:
    - df: DataFrame, the pandas DataFrame to display.

    Returns:
    - Heatmap plot of the dataframe.
    """
    # Filter for numerical variables only
    var_num_limit = 45
    df_numeric = df.select_dtypes(include=['number'])
    num_variables_total = df_numeric.shape[1]
    num_variables_used = min(num_variables_total, var_num_limit)

    if num_variables_total > var_num_limit:
        print(f"The dataset contains {num_variables_total} numerical variables. Only the first {var_num_limit} are used in the correlation table.")
        print(f"There are {num_variables_total - var_num_limit} numerical variables not included in the heatmap.")
        df_numeric = df_numeric.iloc[:, :var_num_limit]

    # Calculate figure size based on the number of variables
    fig_width = 30 / 40 * num_variables_used
    fig_height = 16 / 40 * num_variables_used

    plt.figure(figsize=(fig_width, fig_height))
    heatmap = sns.heatmap(df_numeric.corr(), vmin=-1, vmax=1, annot=True, fmt=".2f", 
                          cmap=sns.color_palette("coolwarm", as_cmap=True), linewidths=0.5, 
                          cbar_kws={"shrink": 0.5},)
    plt.xticks(rotation=45, ha='right', fontsize=8)
    plt.yticks(fontsize=8)
    heatmap.set_title('Correlation Heatmap', fontdict={'fontsize':8}, pad=11)
    cbar = heatmap.collections[0].colorbar
    cbar.ax.tick_params(labelsize=8)
    plt.show()

