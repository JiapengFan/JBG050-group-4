import pandas as pd
import numpy as np
from preprocess.dataAttr import DataSet
from preprocess.parseData import convertStringToTimestamp, appendWeekColumn, convertDayToTimestamp, appendDateTime
from productFunctions.singletonProductFunctions import productYearlyThroughput, productWeeklyDiscountANDThroughput, convertProductIDToName, convertNameToProductID 
from datetime import datetime 

inventory_df = pd.read_csv('.\data\inventory.csv')
products_df = pd.read_csv('.\data\products.csv')
promotions_df = pd.read_csv('.\data\promotions.csv')
transactions_df = pd.read_csv('.\data\\transactions.csv')

# Preprocessing data sets before storing it as an object
transactions_df = appendDateTime(transactions_df, 'day', 'time')
inventory_df = convertDayToTimestamp(inventory_df, 'day', 'before or after delivery', '12:00:00', '12:00:00')


inventory = DataSet(inventory_df)
products = DataSet(products_df)
promotions = DataSet(promotions_df)
transactions = DataSet(transactions_df)

def calculateSalesOfItem(inventory, transaction, inventory_column_date_time, transaction_column_date_time, productID):
    date_time_series_inventory = inventory.df[inventory_column_date_time]
    date_time_series_transactions = transaction.df[transaction.df['product_id'] == productID][transaction_column_date_time]

    def calculateSales(x, date_time_series_transaction, date_time_series_inventory):
        if x.name == 0 or x.name == inventory.df.index.max():
            return 0
        else:
            transactions_sales = date_time_series_transaction[(date_time_series_transactions >= x[0]) & (date_time_series_transactions < date_time_series_inventory[x.name + 1])]
            sales = transactions_sales.count()
            return sales
    
    date_time_series_inventory = inventory.df[inventory_column_date_time]
    product_sale_column = inventory.df[[inventory_column_date_time]].apply(lambda x: calculateSales(x, date_time_series_transactions, date_time_series_inventory), axis = 1)
    return product_sale_column

sales_df = inventory_df.set_index('day').drop(columns = ['date_time', 'Blauwe bessen.1', 'Rundergehakt.1', 'Unox Gelderse rookworst.1', 'Biologisch rundergehakt.1'])
for productName, contents in sales_df.items():
    if productName != 'before or after delivery':
        productID = convertNameToProductID(products, productName)
        product_sale_column = calculateSalesOfItem(inventory, transactions, 'date_time', 'date_time', productID)
        product_sale_column.index = sales_df.index
        sales_df[productName] = product_sale_column

sales_df = sales_df[sales_df['before or after delivery'] == 'after'].drop(columns = ['before or after delivery'])

# sales_df.to_pickle('./df_inventory/inventory_sales_delivery_at_16.pkl')
sales_df.to_pickle('./df_inventory/inventory_sales_delivery_at_12.pkl')

# print(pd.read_pickle('./df_inventory/inventory_sales_delivery_at_16.pkl'))
print(pd.read_pickle('./df_inventory/inventory_sales_delivery_at_23.pkl'))

