import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from preprocess.dataAttr import DataSet
from preprocess.parseData import convertStringToTimestamp, appendWeekColumn
from productFunctions.singletonProductFunctions import productYearlyThroughput, productWeeklyDiscountANDThroughput

products_df = pd.read_csv('.\data\products.csv')
promotions_df = pd.read_csv('.\data\promotions.csv')
transactions_df = pd.read_csv('.\data\\transactions.csv')

transactions_df = convertStringToTimestamp(transactions_df, 'day')
transactions_df = appendWeekColumn(transactions_df, 'day')

products = DataSet(products_df)
promotions = DataSet(promotions_df)
transactions = DataSet(transactions_df)

max_throughput_productid =  transactions.df['product_id'].value_counts().idxmax()
most_promotions_productID = promotions.df['product_id'].value_counts().idxmax()

[product_max_throughput, max_throughput] = productYearlyThroughput(products, transactions, most_promotions_productID)
product_discount__throughput = productWeeklyDiscountANDThroughput(promotions, transactions, most_promotions_productID)

# Weekly throughput is a function of weekly discounts
x = np.array(product_discount__throughput['weekly_discounts'])
y = np.array(product_discount__throughput['weekly_throughput'])

model = LinearRegression().fit(x.reshape(-1, 1), y)

plt.plot(x, y, 'o')

m, b = np.polyfit(x, y, 1)

plt.plot(x, m*x + b)

plt.show()
# r_sq = model.score(x, y)
# print('coefficient of determination:', r_sq)