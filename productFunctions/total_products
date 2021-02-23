import pandas as pd
import numpy as np
import re


def total_products(data): #takes the dataframe of products before the delivery
    df = data
    
    for s in df:
        for p in df.index:
            string = df[s][p]
            list_string = re.findall(r'\d+', string)
            list_int = list(np.int_(list_string))
            relevant_values = [i for i in list_int if list_int.index(i)/2 - list_int.index(i)//2 != 0]
            total = sum(relevant_values)
            df[s][p] = total
            
    return df
