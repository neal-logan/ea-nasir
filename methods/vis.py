import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter

def plot_feature_correlation_matrix(
        df : pd.DataFrame, 
        figsize=(15,15),
        gridsize=15,
        hexbin_cmap = 'plasma',
        dist_color = 'violet',
        dist_edge_color = 'indigo',
        scatter_color = 'indigo',
        scatter_alpha = 0.3):

    cols = df.columns
    n_cols = len(cols)
    
    # Create figure with subplots
    fig, axes = plt.subplots(n_cols, n_cols, figsize=figsize)
    
    # Create plot matrix
    for i in range(n_cols):
        for j in range(n_cols):
            ax = axes[i, j]
            
            # Diagonal: single-feature distribution
            if i == j:
                ax.hist(
                    df[cols[i]], 
                    bins=40,
                    color = dist_color,
                    edgecolor=dist_edge_color)
                ax.set_title(f'Distribution of {cols[i]}')
            
            # Lower triangle: hexbin plots
            elif j < i:
                ax.hexbin(
                        df[cols[j]], 
                        df[cols[i]], 
                        gridsize=gridsize, 
                        cmap=hexbin_cmap, 
                        mincnt=1)
                ax.set_xlabel(cols[j])
                ax.set_ylabel(cols[i])
            
            # Upper triangle: scatterplots
            else:
                ax.scatter(
                        df[cols[j]], 
                        df[cols[i]], 
                        alpha=scatter_alpha,
                        color=scatter_color,
                        edgecolor='none')
                ax.set_xlabel(cols[j])
                ax.set_ylabel(cols[i])
    
    plt.tight_layout()
    plt.show()



def plot_pairwise_time_series_matrix(
        df : pd.DataFrame, 
        figsize = (30,30),
        i_color = 'violet',
        j_color = 'indigo'):

    dates = df['DATE']
    df = df.drop('DATE',axis='columns')
    n_cols = len(df.columns)

    # Create figure with subplots
    fig, axes = plt.subplots(n_cols,n_cols,figsize=figsize)

    
    # Create plot matrix
    for i in range(0,n_cols):
        for j in range(0,n_cols):

        

            # Diagonal: Original Data + Diff1 + Diff2?
            if i == j:
                pass
            
            # Lower triangle: Original Data Pairwise
            # TODO switch to diff1
            elif j < i:
                pass
                # ax1 = plt.subplot(n_cols, n_cols, (i-1)*n_cols + j)
                    
                # # Get column names
                # col1 = df.columns[i]
                # col2 = df.columns[j]
                
                # # Plot first time series on left y-axis
                # ax1.set_ylabel(col1, color=i_color)
                # line1 = ax1.plot(dates, df[col1], color=i_color, label=col1)
                # ax1.tick_params(axis='y', labelcolor=i_color)
                
                # # Create second y-axis and plot second time series
                # ax2 = ax1.twinx()
                # ax2.set_ylabel(col2, color=j_color)
                # line2 = ax2.plot(dates, df[col2], color=j_color, label=col2)
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

    