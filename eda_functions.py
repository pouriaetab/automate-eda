import pandas as pd
import pyarrow
import os
import matplotlib.pyplot as plt
import seaborn as sns

# %load_ext autoreload
# %autoreload 2

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
def display_first_few_rows(df, rows=10):
    """
    Displays the first few rows of DataFrame.

    Parameters: 
    - df: DataFrame, the pandas DataFrame to display.

    Returns:
    - DataFrame: The first few rows of the given DataFrame.
    """
    return df.head(rows)

# === Markdown Start ===
# 
# **Display basic information about the given DataFrame**
# === Markdown End ===
def display_info(df, rows=50):
    """
    Displays basic information about the given DataFrame.

    Parameters:
    - df: DataFrame, the pandas DataFrame to display.

    Returns:
    - None (displays baisc information about the given DataFrame columns).
    """
    # Check if the DataFrame has more columns than the specificed numbers as rows
    if len(df.columns)> rows:
        # If so, limit the DataFrame to the first specified numbers of rows
        print(f"Dataframe has more columns than default numbers of {rows}. Displaying info for the first {rows} columns only.")
        info_df = df.iloc[:, :rows]
    else:
        info_df = df
    return info_df.info()

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
# **Display up to 40 boxplots**
# === Markdown End ===
def display_boxplots(df, max_num_plots=40):
    """
    Create static boxplots for non-binary and non-object features with an optional 
    defualt limit on the maximum number of plots to display.

    Parameters:
    - df: DataFrame, the input DataFrame.
    - max_num_plots: int, optional (default=40)
      The maximum number of boxplots to display

    Returns:
    None (displays the plots).
    """
    # Get non-object columns
    numeric_columns = df.select_dtypes(['float64', 'int64']).columns

    # Count the number of binary features
    num_binary_features = sum(df[col].nunique() <= 2 for col in numeric_columns)

    # Count the number of object/str features
    num_object_features = sum(df[col].dtype == 'object' for col in df.columns)

    # Define an accessible color palette
    colors = sns.color_palette("colorblind")

    # Filter out binary features
    non_binary_columns = [col for col in numeric_columns if df[col].nunique() > 2]

    # Apply the limit 40
    non_binary_columns[:max_num_plots]

    # Print information about the features
    print(f'Binary Features: {num_binary_features}')
    print(f'Object/Str Features: {num_object_features}')
    print(f'Total Generated Boxplots: {len(non_binary_columns)}')
    
    # Create subplots with two boxplots per row (handle odd number of boxplots)
    num_plots = len(non_binary_columns)
    num_rows = (num_plots + 2) // 3
    fig, axes = plt.subplots(num_rows, 3, figsize=(8, 1.5 * num_rows))
    fig.suptitle("Boxplots for Numeric Features", y=1.02, fontsize=8)

    # Flatten axes array for easier indexing
    axes = axes.flatten()

    # Plot each boxplot
    for idx, col_name in enumerate(non_binary_columns):
        sns.boxplot(x=df[col_name], ax=axes[idx], color=colors[idx % len(colors)])
        axes[idx].set_title(col_name, fontsize=8)
        axes[idx].set_xlabel(col_name,fontsize=8)

    # Remove any unused subplots
    for idx in range(num_plots, len(axes)):
        fig.delaxes(axes[idx])

    plt.tight_layout()
    fig.subplots_adjust(hspace=1.7)
    plt.show()

# === Markdown Start ===
# 
# **Display outliers**
# === Markdown End ===
def find_and_display_outliers(df, display_info=True, max_num_cols_with_outliers=10):
    """
    Find and display outliers in non-binary and non-object columns of a DataFrame.

    Parameters:
    - df: DataFrame, the input DataFrame.
    - display_info: bool, set to True to print information, False to suppress printing.
    - max_num_cols_with_outliers: int, optional (default=10), the maximum number of columns 
      for which to display outliers information.

    Returns:
    - None (prints text about outliers).
    """
    # Select non-binary and non-object columns
    numeric_columns = df.select_dtypes(['float64', 'int64']).columns

    # Filter out binary features
    non_binary_columns = [col for col in numeric_columns if df[col].nunique() > 2]

    # Dictionaries to store lower and upper limits for each column
    lower_limits = {}
    upper_limits = {}
    
    columns_shown = 0 # Counter for the number of columns shown

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

            # Increment columns_shown only if outliers are found
            columns_shown += 1

            # Display information only if display_info is True and outliers are found
            if display_info and total_outliers > 0:
                print(f"\nColumn: '{column_name}'")
                print(f"25th Percentile: {q25}")
                print(f"75th Percentile: {q75}")
                print(f"IQR: {iqr}")
                print(f"Lower Limit for Outliers: {lower_limit}")
                print(f"Upper Limit for Outliers: {upper_limit}")
                print(f"Total Rows with Outliers: {total_outliers}")
        # Break the loop if the limit is reached
        if columns_shown >= max_num_cols_with_outliers:
            break
        
    if display_info and total_outliers == 0:
        print("There are no outliers in any of the columns.")

# === Markdown Start ===
# 
# **Correlation heatmap**
# This correlation heatmap is configured to display up to 40 variables for optimal readability and performance. 
# In cases where the dataset contains more than 45 variables, alternative strategies are recommended to gain 
# insights into the data without simultaneously visualizing all variables. Some effective methods include:
#   - Segmentation: Analyzing smaller, categorized subsets of variables.
#   - Principal Component Analysis (PCA): Reducing dimensionality to capture essential information with fewer variables.
#   - Feature Importance: Using machine learning models to identify and focus on the most influential variables.
#   - Partial Correlation and Conditional Independence Tests: Investigating relationships between variables while controlling for others.
#   - Cluster Analysis: Grouping variables based on similarity measures to identify patterns or relationships.
# These approaches allow for a comprehensive analysis of datasets with a large number of variables, ensuring that
# critical insights are derived efficiently and effectively.
# === Markdown End ===
def display_corr_heatmap(df, var_num_limit=40):
    """
    Displays correlation heatmap of the given DataFrame, dynamically adjusting the figure size
    based on the number of numerical variables, with a limit of 40 numerical variables.

    If there are more than 100 numerical variables, informs the user about the number of omitted variables.

    Parameters:
    - df: DataFrame, the pandas DataFrame to display.
    - var_num_limit: int, optional (default=40), the maximum number of numerical variables for creating 
      the heatmap table.

    Returns:
    - Heatmap plot of the dataframe.
    """
    # Filter for numerical variables only
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

