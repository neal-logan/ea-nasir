import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
from matplotlib import colormaps
import ibis
con = ibis.connect("duckdb://")


def plot_pairwise_time_series_matrix(
        df : pd.DataFrame, 
        figsize = (30,30),
        date_col_name : str = 'DATE',
        left_color = 'green',
        right_color = 'indigo',
        ratio_color = 'blue'):

    # Extact date column
    date_col = df[date_col_name]

    # Drop date column from main dataframe
    df = df.drop(date_col_name,axis='columns')
    
    #Get the number of columns to be plotted (excludes dates)
    n_cols = len(df.columns)

    # Create figure with subplots
    fig, axes = plt.subplots(
        nrows = n_cols,
        ncols = n_cols,
        figsize=figsize)

    # Create plot matrix
    for i in range(0,n_cols):
        for j in range(0,n_cols):

            # Diagonal: Original Data + Diff1 + Diff2?
            if i == j:
                pass
            
            # Lower triangle: ratios
            elif j < i:
                ax_left = plt.subplot(n_cols, n_cols, i*n_cols + j+1)
                    
                # Get column names
                col_name_left = df.columns[i]
                col_name_right = df.columns[j]
                
                # Calculate ratios of column i to j
                value_col = df[col_name_left]/df[col_name_right]

                # Create new label for the ratio
                ratio_label = col_name_left + ' / ' + col_name_right

                # Plot first time series on left y-axis
                ax_left.set_ylabel(ratio_label)
                line_left = ax_left.plot(
                    date_col, 
                    value_col, 
                    color=ratio_color, 
                    label=ratio_label)
                               
                # Format date and orient axis
                date_formatter = DateFormatter("%Y-%m")
                ax_left.xaxis.set_major_formatter(date_formatter)
                
                # y-params - color
                ax_left.tick_params(
                    axis='y', 
                    labelcolor=ratio_color)

                # x-params - rotation
                ax_left.tick_params(
                    axis='x', 
                    rotation=60)

                # Add legend
                lines = [line_left]
                labels = [l.get_label() for l in lines]
                ax_left.legend(
                    lines, 
                    labels, 
                    loc='upper left', 
                    fontsize='small')           
            
            # Upper triangle: Original Data
            else:
                ax_left = plt.subplot(n_cols, n_cols, i*n_cols + j+1)
                    
                # Get column names
                col_name_left = df.columns[i]
                col_name_right = df.columns[j]
                
                # Plot first time series on left y-axis
                ax_left.set_ylabel(col_name_left, color=left_color)
                line_left = ax_left.plot(date_col, df[col_name_left], color=left_color, label=col_name_left)
                
                # Create second y-axis on the same x-axis
                ax_right = ax_left.twinx()

                # Plot second time series on right y-axis
                ax_right.set_ylabel(col_name_right, color=right_color)
                line_right = ax_right.plot(
                    date_col, 
                    df[col_name_right], 
                    color=right_color, 
                    label=col_name_right)
                
                # Color the ticks
                ax_left.tick_params(axis='y', labelcolor=left_color)
                ax_right.tick_params(axis='y', labelcolor=right_color)
                
                # Format dates 
                date_formatter = DateFormatter("%Y-%m")
                ax_left.xaxis.set_major_formatter(date_formatter)

                # Orient axis
                ax_left.tick_params(axis='x', rotation=60)
                
                # Legend
                lines = [line_left, line_right]
                labels = [l.get_label() for l in lines]
                ax_left.legend(
                    lines, 
                    labels, 
                    loc='upper left', 
                    fontsize='small')

    # Wrap up and show
    plt.tight_layout()
    plt.show()

    return fig, axes




def plot_feature_correlation_matrix(
        df : pd.DataFrame, 
        figsize=(15,15),
        gridsize=15,
        hexbin_cmap = 'plasma',
        dist_color = 'violet',
        dist_edge_color = 'indigo',
        scatter_color = 'indigo',
        scatter_alpha = 0.3):
    
    # Get all column names
    cols = df.columns
    n_cols = len(cols)
    
    # Create figure with subplots
    fig, axes = plt.subplots(
        nrows = n_cols, 
        ncols = n_cols, 
        figsize=figsize)
    
    # Create plot matrix
    for i in range(n_cols):
        for j in range(n_cols):
            ax = axes[i, j]
            
            # Diagonal: Single-feature distributions
            if i == j:
                ax.hist(
                    df[cols[i]], 
                    bins=40,
                    color = dist_color,
                    edgecolor=dist_edge_color)
                ax.set_title(f'Distribution of {cols[i]}')
            
            # Lower triangle
            elif j < i:
                
                # Plot hexbins
                ax.hexbin(
                        df[cols[j]], 
                        df[cols[i]], 
                        gridsize=gridsize, 
                        cmap=hexbin_cmap, 
                        mincnt=1)
                
                # Set labels
                ax.set_xlabel(cols[j])
                ax.set_ylabel(cols[i])
            
            # Upper triangle
            else:

                # Scatterplots
                ax.scatter(
                        df[cols[j]], 
                        df[cols[i]], 
                        alpha=scatter_alpha,
                        color=scatter_color,
                        edgecolor='none')
                ax.set_xlabel(cols[j])
                ax.set_ylabel(cols[i])
    
    # Wrap up and show
    plt.tight_layout()
    plt.show()

    return fig, axes


def plot_time_series_diffs(
        df: pd.DataFrame,
        date_col_name: str = 'DATE',
        num_diffs: int = 2,
        figsize=(30, 30),
        colors=['orange','green','blue','violet','indigo']):
    
    # Extact date column in datetime format
    dates = pd.to_datetime(df[date_col_name])

    # Drop date column from main dataframe
    df = df.drop(date_col_name,axis='columns')
    
    #Get the number of columns to be plotted (excludes dates)
    cols = df.columns
    n_cols = len(cols)
    
    # Create figure and subplots
    fig, axes = plt.subplots(
        nrows = n_cols, 
        ncols = num_diffs + 1,
        figsize=figsize)
        
    # Create date formatter
    date_formatter = DateFormatter("%Y-%m")

    # Iterate through each numeric column
    for row_num, col_name in enumerate(cols):
        # Get the original data
        feature = df[col_name].copy()
        
        # Plot original data
        axes[row_num, 0].plot(
            dates, 
            feature, 
            color=colors[0], 
            label='Original')
        
        axes[row_num, 0].set_title(f'{col_name} - Original')
        axes[row_num, 0].grid(True)
        axes[row_num, 0].xaxis.set_major_formatter(date_formatter)
        axes[row_num, 0].tick_params(axis='x', rotation=60)
        axes[row_num, 0].legend()
        
        # Calculate and plot differences
        for diff_num in range(1, num_diffs + 1):
            feature = feature.diff()
            axes[row_num, diff_num].plot(dates, feature, color=colors[diff_num % len(colors)], 
                               label=f'{diff_num} Difference')
            axes[row_num, diff_num].set_title(f'{col_name} - {diff_num} Difference')
            axes[row_num, diff_num].grid(True)
            axes[row_num, diff_num].xaxis.set_major_formatter(date_formatter)
            axes[row_num, diff_num].tick_params(axis='x', rotation=60)
            axes[row_num, diff_num].legend()

    plt.tight_layout()
    plt.show()
    return fig, axes    


def plot_decomp(data : ibis.Table,
        date_col : str = 'DATE',
        cmap = 'plasma',):

    # Move to dataframe, sorted by date
    df = data.to_pandas().sort_values(date_col)

    # Separate date and feature columns
    dates = df[date_col]
    df = df.drop(date_col, axis='columns')

    # Establish colorset & align features
    num_features = len(df.columns)
    cmap = colormaps['plasma'] 
    colorset = [cmap(i/num_features) for i in range(num_features)]
    feature_names_sorted = sorted(df.columns)

    # Set figure size
    plt.figure(figsize=(12, 6))

    # Plot the features
    for i in range(num_features):
        plt.plot(dates,
                df[feature_names_sorted[i]],
                '-',
                color = colorset[i])


    # Format date
    date_formatter = DateFormatter("%b")
    ax=plt.gca()
    ax.xaxis.set_major_formatter(date_formatter)

    # Customize the plot
    plt.xlabel('Date', fontsize=12)
    plt.ylabel('Value', fontsize=12)

    # Rotate x-axis labels for better readability
    plt.xticks(rotation=45)

    plt.tight_layout()
    plt.show()
