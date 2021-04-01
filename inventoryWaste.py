import pandas as pd

diff_df = pd.read_csv('.\data\diff_between_restock_updated.csv').set_index('day')
sales_df = pd.read_csv('./derivative_data/sales_03pm.csv').set_index('day')

waste_df = diff_df - sales_df
waste_df.drop(waste_df.tail(1).index,inplace=True)
print(diff_df)
print(sales_df)
print(waste_df)
waste_df.to_csv('./derivative_data/waste_03pm.csv')