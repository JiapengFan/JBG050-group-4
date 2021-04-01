import pandas as pd
import numpy as np
from preprocess.dataAttr import DataSet
from preprocess.parseData import convertStringToTimestamp, appendWeekColumn, convertDayToTimestamp, appendDateTime, handleNaNTrans
from productFunctions.singletonProductFunctions import productYearlyThroughput, productWeeklyDiscountANDThroughput, convertProductIDToName, convertNameToProductID 
from datetime import datetime 

inventory_df = pd.read_csv('.\data\inventory.csv')
products_df = pd.read_csv('.\data\products.csv')
promotions_df = pd.read_csv('.\data\promotions.csv')
transactions_df = pd.read_csv('.\data\\transactions.csv')

# transaction_df_clean = transactions_df.dropna(subset=['day', 'time'])
transaction_df_clean = handleNaNTrans(transactions_df, products_df)

# Parse date or time string into datetime instances
transaction_dates = transaction_df_clean['day'].tolist()
transaction_times = transaction_df_clean['time'].tolist()

transaction_df_clean['date_time'] = appendDateTime(transaction_dates, transaction_times)

inventory_df_no_duplicate_day = inventory_df[inventory_df['before or after delivery'] == 'before']
day_num = inventory_df_no_duplicate_day['day'].tolist()
day_num = [str(x + 1) for x in day_num]

inventory_df_no_duplicate_day['date_time'] = convertDayToTimestamp(day_num, '9:00:00', '15:00:00')

inventory_count = inventory_df_no_duplicate_day['date_time'].tolist()

sales_df = inventory_df_no_duplicate_day.set_index('day').drop(columns = ['Blauwe bessen.1', 'Rundergehakt.1', 'Unox Gelderse rookworst.1', 'Biologisch rundergehakt.1', 'date_time', 'before or after delivery'])
products = sales_df.columns.tolist()

last_day = datetime.strptime('31-12-2018 21:00:00', '%d-%m-%Y %H:%M:%S')

diff_df = pd.read_csv('.\data\diff_between_restock_updated.csv')
diff_df = diff_df.set_index('day')

for product in products:
    product_waste_list = []
    product_diff = diff_df[product].tolist()
    transaction_date_time_series = transaction_df_clean[transaction_df_clean['description'] == product]['date_time']
    for idx, count in enumerate(inventory_count):
        if idx != len(inventory_count) - 1:
            sales_single_product = transaction_date_time_series.where((transaction_date_time_series > count) & (transaction_date_time_series <= inventory_count[idx + 1])).count()
            waste = product_diff[idx] - sales_single_product
            if waste < 0:
                sales_single_product = product_diff[idx]
        else:
            sales_single_product = transaction_date_time_series.where((transaction_date_time_series > count) & (transaction_date_time_series <= last_day)).count()
        product_waste_list.append(sales_single_product)
    sales_df[product] = product_waste_list

sales_df.to_csv('./derivative_data/sales_03pm.csv')

# def calculateSalesOfItem(inventory, transaction, inventory_column_date_time, transaction_column_date_time, productID):
#     date_time_series_inventory = inventory.df[inventory_column_date_time]
#     date_time_series_transactions = transaction.df[transaction.df['product_id'] == productID][transaction_column_date_time]

#     def calculateSales(x, date_time_series_transaction, date_time_series_inventory):
#         if x.name == 0 or x.name == inventory.df.index.max():
#             return 0
#         else:
#             transactions_sales = date_time_series_transaction[(date_time_series_transactions >= x[0]) & (date_time_series_transactions < date_time_series_inventory[x.name + 1])]
#             sales = transactions_sales.count()
#             return sales
    
#     date_time_series_inventory = inventory.df[inventory_column_date_time]
#     product_sale_column = inventory.df[[inventory_column_date_time]].apply(lambda x: calculateSales(x, date_time_series_transactions, date_time_series_inventory), axis = 1)
#     return product_sale_column

# sales_df = inventory_df.set_index('day').drop(columns = ['date_time', 'Blauwe bessen.1', 'Rundergehakt.1', 'Unox Gelderse rookworst.1', 'Biologisch rundergehakt.1'])
# for productName, contents in sales_df.items():
#     if productName != 'before or after delivery':
#         productID = convertNameToProductID(products, productName)
#         product_sale_column = calculateSalesOfItem(inventory, transactions, 'date_time', 'date_time', productID)
#         product_sale_column.index = sales_df.index
#         sales_df[productName] = product_sale_column

# sales_df = sales_df[sales_df['before or after delivery'] == 'after'].drop(columns = ['before or after delivery'])

# # sales_df.to_pickle('./df_inventory/inventory_sales_delivery_at_16.pkl')
# sales_df.to_pickle('./df_inventory/inventory_sales_delivery_at_12.pkl')

# # print(pd.read_pickle('./df_inventory/inventory_sales_delivery_at_16.pkl'))
# print(pd.read_pickle('./df_inventory/inventory_sales_delivery_at_23.pkl'))

