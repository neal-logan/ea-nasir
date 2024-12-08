import ibis
import pandas as pd
import numpy as np
con = ibis.connect("duckdb://")

# Merge multiple Ibis tables on the specific key
# Adding prefixes to each column based on dataset name 
def merge_tables(
        tables_to_merge : dict[str, ibis.Table],
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
    join_key = 'DATE'
    merged_tables = None

    for curr_dset_name in tables_to_merge.keys():
        
        # Get current dataset
        curr_dset = tables_to_merge[curr_dset_name]

        # Start with dates only
        if merged_tables is None:
            merged_tables = ibis.memtable(curr_dset.to_pandas()['DATE'])
        
        # df_new[str(year) + '_' + col] = df_new[col]
        # df_new = df_new.drop(col, axis='columns')

        # Rename feature columns in current dataset to include the dataset name
        for col in curr_dset.columns:
            if 'DATE' not in col:
                new_feature_name = curr_dset_name + '_' + col
                curr_dset = curr_dset.rename({new_feature_name : col})


        # Outer join the datasets on date
        merged_tables = ibis.join(
            left = merged_tables, 
            right = curr_dset,
            predicates = join_key,
            how = join_type,
            lname = '',
            rname = curr_dset_name+'_{name}')
        
        # Cross-fill date from new x_DATE column
        # to existing DATE column 
        # and drop extraneous x_DATE column
        # TODO un-hardcode this
        date_col_name = curr_dset_name + '_DATE'
        if date_col_name in merged_tables.columns: 
            merged_tables = merged_tables.mutate(
                        DATE=ibis.case()
                        .when(merged_tables.DATE.isnull(), merged_tables[date_col_name])
                        .else_(merged_tables.DATE).end())
            merged_tables = merged_tables.drop(date_col_name)
                    
    return merged_tables

def impute_forward_fill_numerics(
        data: ibis.Table, 
        sort_by : str = 'DATE') -> pd.DataFrame:
      
    # Convert to pandas, sorted by date
    df = data.to_pandas().sort_values(by='DATE')
    
    # Identify numeric columns
    numeric_cols = df.select_dtypes(include=['float64', 'float32', 'int64', 'int32']).columns
    
    # Forward fill
    df[numeric_cols] = df[numeric_cols].ffill()

    # return dataframe with forward-filled data
    return ibis.memtable(df)

    
def annual_decomposition(
        data: ibis.Table,
        decomp_features : list[str])-> ibis.Table:

    df = data.to_pandas().sort_values('DATE')
    df['DATE'] = pd.to_datetime(df['DATE'])

    years = df['DATE'].dt.year.unique()
    
    decomp_datasets = {}

    # TODO reverse these for efficiency
    for col in decomp_features:
        for year in years:
            
            df_new = data.filter(data.DATE.year() == year).to_pandas()[['DATE',col]]
            
            # Rename feature to include year
            # df_new[str(year) + '_' + col] = df_new[col]
            # df_new = df_new.drop(col, axis='columns')

            # Change date to 2000 to match merge table
            df_new['DATE'] = df_new['DATE'].apply(lambda x: x.replace(year=2000))

            decomp_datasets[str(year)] = ibis.memtable(df_new)

    table_annual_decomp = merge_tables(
        decomp_datasets,
        join_type = 'outer')
    
    return table_annual_decomp
