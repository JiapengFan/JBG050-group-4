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

def appendDateTime(dates: list, times: list):
    '''
    Returns df with appended column containing date and time of the type datetime.
    '''

    date_times = []
    for idx, date in enumerate(dates):
            try: 
                date_times.append(datetime.strptime(date + ' ' + times[idx], '%d-%m-%Y %H:%M:%S'))
            except:
                date_times.append(datetime.strptime(date + ' ' + times[idx], '%m/%d/%Y %H:%M:%S'))

    return date_times

def convertDayToTimestamp(delivery_day: list, delivery_time_monday: str, delivery_time_tuesday: str):
    '''
    Returns df with appended column filled with corresponding timestamp.

    Arguments:
        delivery_day <class 'list'>: Day numbers of delivery.
        delivery_time <type 'str'> (hour:minute:second format): The time of delivery.
    '''
    
    # Initialize year 
    year = '2018'

    date_time = []
    for idx, day_num in enumerate(delivery_day):
        if idx % 2 == 0:
            date_time.append(datetime.strptime(year + '-' + day_num + ' ' + delivery_time_monday, '%Y-%j %H:%M:%S'))
        else:
            date_time.append(datetime.strptime(year + '-' + day_num + ' ' + delivery_time_tuesday, '%Y-%j %H:%M:%S'))

    return date_time

def handleNaNTrans(transactions_df,  products_df):
    for i in transactions_df[transactions_df['day'].isnull()].index:
        transactions_df['day'][i] = transactions_df['day'][i-1]
    
    for i in transactions_df[transactions_df['time'].isnull()].index:
        transactions_df['time'][i] = transactions_df['time'][i-1]
    
    for i in transactions_df[transactions_df['product_id'].isnull()].index:
        for a in range(len(products_df)):
            if transactions_df['description'][i] == products_df['description'][a]:
                transactions_df['product_id'][i] = products_df['product_id'][a]
                
    for i in transactions_df[transactions_df['description'].isnull()].index:
        for a in range(len(products_df)):
            if transactions_df['product_id'][i] == products_df['product_id'][a]:
                transactions_df['description'][i] = products_df['description'][a]

    return transactions_df