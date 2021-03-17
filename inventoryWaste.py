import pandas as pd

diff_df = pd.read_csv('.\data\diff_between_restock.csv')
sales_df = pd.read_csv('./data/sales_03pm.csv').set_index('day')

diff_df = diff_df.drop(columns = ['Blauwe bessen.1', 'Rundergehakt.1', 'Unox Gelderse rookworst.1', 'Biologisch rundergehakt.1', 'before or after delivery']).set_index('day')

waste_df = diff_df - sales_df
print(diff_df)
print(sales_df)
print(waste_df)
waste_df.to_csv('./data/waste_03pm.csv')