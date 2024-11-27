import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter

def plot_time_series_diffs(
        df: pd.DataFrame,
        date_column: str = 'DATE',
        number_of_diffs: int = 4,
        figsize=(30, 30),
        colors=['orange','green','blue','violet','indigo']):
    """
    Plot each numeric column in the dataframe with its original data and successive differences.
    
    Parameters:
    -----------
    df : pandas.DataFrame
        Input dataframe containing time series data
    date_column : str
        Name of the column containing dates
    number_of_diffs : int
        Number of differences to compute and plot
    figsize : tuple
        Size of the figure (width, height)
    colors : list
        List of colors to use for the original data and differences
    
    Returns:
    --------
    tuple : (matplotlib.figure.Figure, numpy.ndarray)
        The created figure and array of axes objects containing all subplots
    """
    
    # Get numeric columns excluding the date column
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    numeric_cols = [col for col in numeric_cols if col != date_column]
    
    # Calculate number of rows (one per numeric column) and columns (original + diffs)
    n_rows = len(numeric_cols)
    n_cols = number_of_diffs + 1
    
    # Create figure and subplots
    fig, axes = plt.subplots(n_rows, n_cols, figsize=figsize)
    
    # If there's only one numeric column, wrap axes in a list to make it 2D
    if n_rows == 1:
        axes = np.array([axes])
    
    # Create date formatter
    date_formatter = DateFormatter("%Y-%m-%d")

    # Ensure dates are in datetime format
    dates = pd.to_datetime(df[date_column])

    # Iterate through each numeric column
    for row, col_name in enumerate(numeric_cols):
        # Get the original data
        feature = df[col_name].copy()
        
        # Plot original data
        axes[row, 0].plot(dates, feature, color=colors[0], label='Original')
        axes[row, 0].set_title(f'{col_name} - Original')
        axes[row, 0].grid(True)
        axes[row, 0].xaxis.set_major_formatter(date_formatter)
        axes[row, 0].tick_params(axis='x', rotation=45)
        axes[row, 0].legend()
        
        # Calculate and plot differences
        for diff in range(1, number_of_diffs + 1):
            feature = feature.diff()
            axes[row, diff].plot(dates, feature, color=colors[diff % len(colors)], 
                               label=f'{diff} Difference')
            axes[row, diff].set_title(f'{col_name} - {diff} Difference')
            axes[row, diff].grid(True)
            axes[row, diff].xaxis.set_major_formatter(date_formatter)
            axes[row, diff].tick_params(axis='x', rotation=45)
            axes[row, diff].legend()

    # Adjust layout to prevent overlapping
    plt.tight_layout()
    plt.show()
    return fig, axes

# Example usage:
"""
# Create sample data
dates = pd.date_range(start='2023-01-01', end='2023-12-31', freq='D')
df = pd.DataFrame({
    'DATE': dates,
    'Value1': np.random.normal(0, 1, len(dates)).cumsum(),
    'Value2': np.sin(np.linspace(0, 4*np.pi, len(dates))) * 10
})

# Create the plot
fig = plot_time_series_diffs(df, date_column='DATE', number_of_diffs=2)
plt.show()
"""


def plot_pairwise_time_series_matrix(
        df : pd.DataFrame, 
        figsize = (30,30),
        datecol : str = 'DATE',
        i_color = 'violet',
        j_color = 'indigo'):

    dates = df[datecol]
    df = df.drop(datecol,axis='columns')
    n_cols = len(df.columns)

    # Create figure with subplots
    fig, axes = plt.subplots(n_cols,n_cols,figsize=figsize)

    
    # Create plot matrix
    for i in range(0,n_cols):
        for j in range(0,n_cols):

            # Diagonal: Original Data + Diff1 + Diff2?
            if i == j:
                pass
            
            # Lower triangle: Diff1 pairwise
            elif j < i:
                pass                
                # ax1 = plt.subplot(n_cols, n_cols, i*n_cols + j+1)

                # # Get column names
                # col1 = df.columns[j]
                # col2 = df.columns[i]
                
                # feature1 = df[col1].copy()
                # feature2 = df[col2].copy().diff()

                # # Plot first time series on left y-axis
                # ax1.set_ylabel(col1, color=i_color)
                # line1 = ax1.plot(dates, feature1, color=i_color, label=col1)
                # ax1.tick_params(axis='y', labelcolor=i_color)
                
                # # Create second y-axis and plot second time series
                # ax2 = ax1.twinx()
                # ax2.set_ylabel(col2, color=j_color)
                # line2 = ax2.plot(dates, feature2, color=j_color, label=col2)
                # ax2.tick_params(axis='y', labelcolor=j_color)
                
                # # Format date on x-axis
                # date_formatter = DateFormatter("%Y-%m-%d")
                # ax1.xaxis.set_major_formatter(date_formatter)
                # plt.xticks(rotation=45)
                
                # # Add legend
                # lines = line1 + line2
                # labels = [l.get_label() for l in lines]
                # ax1.legend(lines, labels, loc='upper left', fontsize='small')
                
                # # Make axis labels smaller
                # ax1.tick_params(axis='x', labelsize=8)
                # ax1.tick_params(axis='y', labelsize=8)
                # ax2.tick_params(axis='y', labelsize=8)
            
            # Upper triangle: Original Data
            else:
                ax1 = plt.subplot(n_cols, n_cols, i*n_cols + j+1)
                    
                # Get column names
                col1 = df.columns[i]
                col2 = df.columns[j]
                
                # Plot first time series on left y-axis
                ax1.set_ylabel(col1, color=i_color)
                line1 = ax1.plot(dates, df[col1], color=i_color, label=col1)
                ax1.tick_params(axis='y', labelcolor=i_color)
                
                # Create second y-axis and plot second time series
                ax2 = ax1.twinx()
                ax2.set_ylabel(col2, color=j_color)
                line2 = ax2.plot(dates, df[col2], color=j_color, label=col2)
                ax2.tick_params(axis='y', labelcolor=j_color)
                
                # Format date on x-axis
                date_formatter = DateFormatter("%Y-%m-%d")
                ax1.xaxis.set_major_formatter(date_formatter)
                plt.xticks(rotation=45)
                
                # Add legend
                lines = line1 + line2
                labels = [l.get_label() for l in lines]
                ax1.legend(lines, labels, loc='upper left', fontsize='small')
                
                # Make axis labels smaller
                ax1.tick_params(axis='x', labelsize=8)
                ax1.tick_params(axis='y', labelsize=8)
                ax2.tick_params(axis='y', labelsize=8)

    plt.tight_layout()
    plt.show()
    return fig, axes

    