import pandas as pd

diff_df = pd.read_csv('.\data\diff_between_restock.csv')
sales_df = pd.read_csv('.\data\sales\inventory_sales_delivery_at_12.csv')

sales_df.set_index('day', inplace=True)
diff_df = diff_df.drop(columns = ['Blauwe bessen.1', 'Rundergehakt.1', 'Unox Gelderse rookworst.1', 'Biologisch rundergehakt.1', 'before or after delivery']).set_index('day')

print(diff_df)
print(sales_df)
waste_df = diff_df - sales_df

waste_df.to_csv('./data/waste/inventory_waste_delivery_at_12.csv')
# waste_df.to_pickle('./df_inventory/inventory_waste_delivery_at_23.pkl')

# print(pd.read_pickle('./df_inventory/inventory_waste_delivery_at_23.pkl'))

print(pd.read_csv('./data/waste/inventory_waste_delivery_at_12.csv'))