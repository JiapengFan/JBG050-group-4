import pandas as pd

inventory_df = pd.read_csv('.\data\inventory.csv')
products_df = pd.read_csv('.\data\products.csv')
promotions_df = pd.read_csv('.\data\promotions.csv')
transactions_df = pd.read_csv('.\data\\transactions.csv')

class DataSet():
    """ Class for storing data and its attributes/properties
    """

    def __init__(self, df, shape, columns):
        self.df = df
        self.shape = shape
        self.columns = columns
        # add more useful attributes/properties

inventory = DataSet(inventory_df, inventory_df.shape, inventory_df.columns)
products = DataSet(products_df, products_df.shape, products_df.columns)
promotions = DataSet(promotions_df, promotions_df.shape, promotions_df.columns)
transactions = DataSet(transactions_df, transactions_df.shape, transactions_df.columns)

# Inspect data sets
print(inventory.df)
print(products.df)
print(promotions.df)
print(transactions.df)