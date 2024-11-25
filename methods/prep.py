import ibis
import pandas as pd
con = ibis.connect("duckdb://")

# Merge multiple Ibis tables on the specific key
# Adding prefixes to each column based on dataset name 
def merge_tables(
        tables_to_merge : dict[str, ibis.Table],
        join_key : str,
        join_type : str) -> ibis.Table:
    
    """
    Merge multiple Ibis tables with column name prefixing based on dataset names.

    Parameters:
    -----------
    tables_to_merge : dict[str, ibis.Table]
        Dictionary of tables to merge, with dataset names as keys
    join_key : str, default 'DATE'
        Column name used for joining tables
    join_type : str, default 'innter'
        Type of join to perform (e.g., 'inner', 'left', 'right', 'outer')

    Returns:
    --------
    ibis.Table
        A single merged table with columns prefixed by their original dataset names, 
        joined on the specified join key using the specified join type
    
    Notes:
    ------
    - Columns with the join key are not prefixed
    - Duplicate column names are handled by prefixing with dataset names
    """
    merged_tables = None

    for dataset_name in tables_to_merge.keys():
        
        # Get current dataset
        current_dataset = tables_to_merge[dataset_name]

        #Base case
        if merged_tables is None:
            merged_tables = current_dataset 
        else:
            # Outer join the datasets on date
            merged_tables = ibis.join(
                left = merged_tables, 
                right = current_dataset,
                predicates = join_key,
                how = join_type,
                lname = '',
                rname = dataset_name+'_{name}')
            
            # Cross-fill date from new x_DATE column
            # to existing DATE column 
            # and drop extraneous x_DATE column
            col_name = dataset_name + '_DATE'
            if col_name in merged_tables.columns: 
                merged_tables = merged_tables.mutate(
                            DATE=ibis.case()
                            .when(merged_tables.DATE.isnull(), merged_tables[col_name])
                            .else_(merged_tables.DATE).end())
                merged_tables = merged_tables.drop(col_name)
                    
    return merged_tables

def impute_forward_fill(
        data: ibis.Table, 
        sort_by : str = 'DATE') -> pd.DataFrame:
    """
    Impute missing values in time series data using the most recent previous valid data.

    Parameters:
    -----------
    data : ibis.Table
        Input time series data with a date key and numeric features
    
    Returns:
    --------
    ibis.Table
        Data table with NaNs filled using the most recent previous valid data
    """
      
    # Convert to pandas, sorted by date
    df = data.to_pandas().sort_values(by='DATE')
    
    # Identify numeric columns
    numeric_cols = df.select_dtypes(include=['float64', 'float32', 'int64', 'int32']).columns
    
    # Forward fill
    df[numeric_cols] = df[numeric_cols].ffill()

    # return dataframe with forward-filled data
    return ibis.memtable(df)


    
    
