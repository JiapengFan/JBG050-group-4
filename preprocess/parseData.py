import pandas as pd

def convertStringToTimestamp(df, str_column):
    ''' 
    Returns df with converted column.
    Arguments:
        df <class 'dataframe'>: Dataframe with column yet to be converted.
        str_column <type 'str'>: Column name of the column to be converted into timestamp type.
    Returns:
        df <class 'dataframe'>: df with converted column.

    '''
    df[str_column] = pd.to_datetime(df[str_column])     # Parse type str into type timestamp
    return df

def appendWeekColumn(df, column_name):
    ''' 
    Returns df with appended column filled with corresponding week number.
    Arguments:
        df <class 'dataframe'>: Dataframe with column yet to be converted.
        column_name <type 'str'>: Column name of the column with timestamp type values.
    Returns:
        df <class 'dataframe'>: df with appended week column.
    '''
    df['week'] = df[column_name].dt.isocalendar().week        # Convert timestamp to week number
    return df