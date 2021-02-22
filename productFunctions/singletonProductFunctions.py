def productYearlyThroughput(products, transactions, productID):
    '''
    Retrieves given product's yearly transactional throughput and its name.
    Argument:
        products <type 'object'>: self defined object, see dataAttr.py.
        transactions <type 'object'>: self defined object, see dataAttr.py.
        productID <type 'str'>: Product ID.
    Returns: 
        <type 'list'> [product name, yearly transactional throughput of the product]
    '''

    products_throughput_count = transactions.df['product_id'].value_counts()
    transactional_throughput = products_throughput_count[productID]

    product = products.df[products.df['product_id'] == productID]['description'].values[0]

    return [product, transactional_throughput]

def productWeeklyDiscountANDThroughput(promotions, transactions, productID):
    '''
    Retrieves given product's weekly discount in list with nested dictionaries and throughput.
    Argument:
        promotions <type 'object'>: self defined object, see dataAttr.py.
        transactions <type 'object'>: self defined object, see dataAttr.py.
        productID <type 'str'>: Product ID.
    Returns: 
        <type 'dictionary'> 
        {
            'weekly_discounts' <type 'list'>: Position of the elements + 1 represent the week number,
            'weekly_throughput' <type 'list'>: Position of the elements + 1 represent the week number
        }
    '''

    weekly_discounts_series = promotions.df[promotions.df['product_id'] == productID].set_index('week')['discount']
    weekly_discounts_list = [0] * transactions.df['week'].max()     # initialize list of zeros with its length as number of weeks available in the transaction data set - 1
    
    for idx, value in weekly_discounts_series.items():
        weekly_discounts_list[idx-1] = value

    weekly_throughput_series = transactions.df[transactions.df['product_id'] == productID].groupby('week').count()[transactions.columns[0]]

    return {'weekly_discounts': weekly_discounts_list, 'weekly_throughput': weekly_throughput_series.tolist()}