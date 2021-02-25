import pandas as pd
import numpy as np
from datetime import datetime 

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

def appendDateTime(df, column_name_date, column_name_time):
    '''
    Returns df with appended column containing date and time of the type datetime.

    Arguments:
        df <class 'dataframe'>: Target dataframe to append the column.
        column_name_date <type 'str'>: Column name of the column containing date of type str.
        column_name_date <type 'str'>: Column name of the column containing time of type str.

    Returns:
        df <class 'dataframe'>: df with appended column with date and time.
    '''

    def toDateTime(x):
        if not isinstance(x[1], float) and not isinstance(x[0], float):
            try: 
                return datetime.strptime(x[0] + ' ' + x[1], '%d-%m-%Y %H:%M:%S')
            except:
                return datetime.strptime(x[0] + ' ' +  x[1], '%d/%m/%Y %H:%M:%S')
    
    df['date_time'] = df[[column_name_date, column_name_time]].apply(lambda x: toDateTime(x), axis = 1)

    return df

def convertDayToTimestamp(df, column_name_day, column_name_before_after, inventarize_time_before, inventarize_time_after):
    '''
    Returns df with appended column filled with corresponding timestamp.

    Arguments:
        df <class 'dataframe'>: Dataframe with column yet to be converted.
        column_name_day <type 'str'>: Column name of the column with day numbers.
        column_name_before_after <type 'str'>: Column name of the column indicating whether it's before or after delivery.
        inventarize_time_before <type 'str'> (hour:minute:second format): The fixed time to update inventory backlog before delivery.
        inventarize_time_before <type 'str'> (hour:minute:second format): The fixed time to update inventory backlog after delivery.

    Returns:
        df <class 'dataframe'>: df with appended timestamp column.
    '''
    
    # Initialize year 
    year = '2018'

    def convertToDateAndTime(x):
        if x[1] == 'before':
            return datetime.strptime(year + '-' + str(x[0] + 1) + ' ' + inventarize_time_before, '%Y-%j %H:%M:%S')
        else:
            return datetime.strptime(year + '-' + str(x[0] + 1) + ' ' + inventarize_time_after, '%Y-%j %H:%M:%S')
    
    # Converting to date and set given time
    df['date_time'] = df[[column_name_day, column_name_before_after]].apply(lambda x: convertToDateAndTime(x), axis = 1)
    
    return df