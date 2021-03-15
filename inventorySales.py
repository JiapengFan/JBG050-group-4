import pandas as pd
import numpy as np
from preprocess.dataAttr import DataSet
from preprocess.parseData import convertStringToTimestamp, appendWeekColumn, convertDayToTimestamp, appendDateTime
from productFunctions.singletonProductFunctions import productYearlyThroughput, productWeeklyDiscountANDThroughput, convertProductIDToName, convertNameToProductID 
from datetime import datetime 

inventory_df = pd.read_csv('.\data\inventory.csv')
# products_df = pd.read_csv('.\data\products.csv')
# promotions_df = pd.read_csv('.\data\promotions.csv')
transactions_df = pd.read_csv('.\data\\transactions.csv')

# Preprocessing data sets before storing it as an object
transactions_df = appendDateTime(transactions_df, 'day', 'time')
# inventory_df = convertDayToTimestamp(inventory_df, 'day', 'before or after delivery', '12:00:00', '12:00:00')

inventory = DataSet(inventory_df)
# products = DataSet(products_df)
# promotions = DataSet(promotions_df)
transactions = DataSet(transactions_df)

def convertDayToDate(days: list, year: str):
    '''
    Converts list of day numbers given the year to list of dates.

    Arguments:
    days <class: list>: The day numbers to be converted.
    year  <class: str>: The year the day numbers are in.

    Returns:
    dates <class: list>: The dates associated with input list day.
    '''

    dates = []

    for day in days:
        actual_day = day + 1
        datetime_instance = datetime.strftime(datetime.strptime(year + '-' + str(actual_day), '%Y-%j'), '%d-%m-%Y')
        dates.append(datetime_instance)

    return dates

def wasteFirstWholeHourDelivery(transaction, diff: list, products: list, start_datetime, end_date):
    '''
    returns the first whole hour for the given end date for which the waste per product is positive.

    Arguments:
    transaction <class: pd.DataFrame>: Transaction history of products.
    diff <class: list>: Difference of product quantity between restocks, each index matches up with the product list.
    products <class: list>: The product names of which their waste needss to be obtained.
    start_time <class: str> [day-month-year hours:minutes:seconds]: Start date and time for sales to be considered.
    end_time <class: str> [day-mounth-year]: End date for sales to be considered.

    Returns:
    option 1:
        [waste_list, positive_times]

        waste_list <class: list>: Positive waste for each product, 
        where the index of the element corresponds to the index of the given products list and an extra element that represents the corresponding end time.
        positive_times <class: list>: Whole hours for which the waste per product is positive.
    option 2:
        [[], []]
        
        : if there is no whole hours for which the waste of every product is positive.

    Remarks:
    A transaction can only take place between 9 am and 9 pm.
    '''

    start_datetime = datetime.strptime(start_datetime, '%d-%m-%Y %H:%M:%S')

    positive_times_all_products = []
    positive_waste_all_products = []

    for idx, inventory_diff in enumerate(diff):
        transaction_single_product_datetime = transaction[transaction['description'] == products[idx]]['date_time']

        positive_times = []
        positive_waste = []

        wholeHour = 9
        while wholeHour < 22:
            formatted_whole_hour = ' {}:00:00'.format(wholeHour)
            end_datetime = datetime.strptime(end_date + formatted_whole_hour, '%d-%m-%Y %H:%M:%S')
            sales = transaction_single_product_datetime.where((start_datetime <= transaction_single_product_datetime) & (transaction_single_product_datetime < end_datetime)).count()
            waste = inventory_diff - sales

            if waste >= 0:
                positive_times.append(formatted_whole_hour)
                positive_waste.append(waste)
            wholeHour += 1
        
        positive_times_all_products.append(positive_times)
        positive_waste_all_products.append(positive_waste)

    final_positive_times = positive_times_all_products[0]
    for product_positive_times in positive_times_all_products:
        final_positive_times = [i for i in final_positive_times if i in product_positive_times]

    if not final_positive_times:
        return [[], []]
    
    final_positive_waste = []

    for final_time in final_positive_times:
        final_positive_waste_item = []
        for i_times, times in enumerate(positive_times_all_products):
            for i_time, time in enumerate(times):
                if final_time == time:
                    final_positive_waste_item.append(f'{positive_waste_all_products[i_times][i_time]}')
        final_positive_waste.append(final_positive_waste_item)

    return [final_positive_waste, final_positive_times]

# retrieveValidWasteDF(...) returns(waste_df: pd.DataFrame)
def retrieveValidWasteDF(transactions, diffs: list, products: list, dates: list, uneliminated_possible_start_times: list, uneliminated_possible_waste: list, positive_waste_so_far: list):
    '''
    Returns waste data frame with only positive values, with an extra column filled with the corresponding end datetime.

    Arguments:
    transactions <class: pd.DataFrame>: Transaction history of products.
    diff <class: list>: Difference of product quantity between restocks, each index matches up with the product list.
    products <class: list>: The product names of which their waste needs to be obtained.
    dates <class: list>: The dates of restocks in order of the date.
    uneliminated_possible_times <class: list>: Enables backtracking when a time trace gives negative waste, this list contains all possible start times
    , the element positioned at i indicates the possible start times for the i + 1th row of the diff data frame.
    uneliminated_possible_waste <class: list>: Similar to uneliminated_possible_times, 
    but contains all possible waste associated with the start times of uneliminated_possible_times by index.
    possible_waste_so_far <class: list>: Positive waste obtained so far by going down the current time trace, where i of row i corresponds to the index of input 'dates'.

    Returns:
    option 1:
        final_positive_waste_df <class pd.DataFrame>: only positive values, with an extra column filled with the corresponding end datetime.
    option 2:
        False: Not possible.
    '''

    retrieveValidWasteDF.counter += 1

    # initialization
    if not uneliminated_possible_start_times:
        end_date =  dates[1]
        start_date = '01-01-2018 09:00:00'

        [first_restock_waste, first_restock_times] = wasteFirstWholeHourDelivery(transactions, diffs[0], products, start_date, end_date)

        if first_restock_times:
            uneliminated_possible_start_times.append(first_restock_times)
            uneliminated_possible_waste.append(first_restock_waste)

            if uneliminated_possible_start_times:
                retrieveValidWasteDF(transactions, diffs, products, dates, uneliminated_possible_start_times, uneliminated_possible_waste, positive_waste_so_far)

        else:
            print(retrieveValidWasteDF.counter)
            print('Im in initialization')
            return False
    
    else:
        # loop
            # invariant: 0 <= i <= |diff_df| not true
            # invariant: forall j | 0 <= j <= i :: forall m | 0 <= m <= |diff_products| :: total_waste[j][m] > 0 not true

        i = len(uneliminated_possible_start_times)
        uneliminated_possible_start_times_intact = uneliminated_possible_start_times[-1].copy()
        max_index = len(uneliminated_possible_start_times_intact)

        for uneliminated_possible_start_time_index, uneliminated_possible_start_time in enumerate(uneliminated_possible_start_times_intact):
            print(uneliminated_possible_start_time)
            # invariance
            if i < len(diffs) - 1:
                start_date_time = dates[i] + uneliminated_possible_start_time
                end_date = dates[i + 1]

                del uneliminated_possible_start_times[-1][0]
                del uneliminated_possible_waste[-1][0]

                print(start_date_time)
                [test_waste, test_times] = wasteFirstWholeHourDelivery(transactions, diffs[i], products, start_date_time, end_date)
                print(test_times)

                if test_times:
                    uneliminated_possible_start_times.append(test_times)
                    uneliminated_possible_waste.append(test_waste)

                    end_date_time = start_date_time

                    positive_waste_so_far_item = test_waste[0]
                    positive_waste_so_far_item.append(end_date_time)
                    positive_waste_so_far.append(positive_waste_so_far_item)

                    retrieveValidWasteDF(transactions, diffs, products, dates, uneliminated_possible_start_times, uneliminated_possible_waste, positive_waste_so_far)

                else:
                    if uneliminated_possible_start_time_index < max_index - 1: 
                        continue
                    else:
                        if len(uneliminated_possible_start_times) != 1:
                            del uneliminated_possible_start_times[-1]
                            del uneliminated_possible_waste[-1]
                            del positive_waste_so_far[len(uneliminated_possible_start_times) - 1]

                            retrieveValidWasteDF(transactions, diffs, products, dates, uneliminated_possible_start_times, uneliminated_possible_waste, positive_waste_so_far)
                        else:
                            print(retrieveValidWasteDF.counter)
                            print('Im in invariance')
                            return False

            # finalization
            else:
                waste_last_restock = []

                end_date_time = '31-12-2018 21:00:00'

                start_datetime = datetime.strptime(positive_waste_so_far[-1][-1], '%d-%m-%Y %H:%M:%S')
                end_datetime = datetime.strptime(end_date_time, '%d-%m-%Y %H:%M:%S')

                for idx, inventory_diff in enumerate(diffs[-1]):
                    transaction_single_product_datetime = transactions[transactions['description'] == products[idx]]['date_time']

                    sales = transaction_single_product_datetime.where((start_datetime <= transaction_single_product_datetime) & (transaction_single_product_datetime < end_datetime)).count()  
                    waste = inventory_diff - sales

                    if waste >= 0:
                        if idx != len(diffs[-1]) - 1:
                            waste_last_restock.append(waste)
                        else:
                            waste_last_restock.extend((waste, end_date_time))

                    else:
                        if uneliminated_possible_start_time_index < max_index - 1: 
                            continue

                        else:
                            del positive_waste_so_far[len(uneliminated_possible_start_times) - 1]

                            retrieveValidWasteDF(transactions, diffs, products, dates, uneliminated_possible_start_times, uneliminated_possible_waste, positive_waste_so_far)

                positive_waste_so_far.append(waste_last_restock)
                final_positive_waste = positive_waste_so_far
                break

        final_positive_waste_df = pd.DataFrame(final_positive_waste, index = dates, columns = products)

        return final_positive_waste_df

diff_df = pd.read_csv('.\data\diff_between_restock.csv')
diff_df = diff_df.drop(columns = ['Blauwe bessen.1', 'Rundergehakt.1', 'Unox Gelderse rookworst.1', 'Biologisch rundergehakt.1', 'before or after delivery']).set_index('day')

diff_list = diff_df.values.tolist()
diff_products =  diff_df.columns.tolist()
    
Inventory_without_duplicate_day  = inventory.df[inventory.df['before or after delivery'] == 'after']
days = Inventory_without_duplicate_day['day'].tolist()
date_list = convertDayToDate(days, '2018')

retrieveValidWasteDF.counter = 0
valid_waste_df = retrieveValidWasteDF(transactions.df, diff_list, diff_products, date_list, [], [], [])

print(valid_waste_df)

# def calculateSalesOfItem(inventory, transaction, inventory_column_date_time, transaction_column_date_time, productName):
#     date_time_series_inventory = inventory.df[inventory_column_date_time]
#     date_time_series_transactions = transaction.df[transaction.df['description'] == productName][transaction_column_date_time]

#     def calculateSales(x, date_time_series_transaction, date_time_series_inventory):
#         if x.name == inventory.df.index.max():
#             transactions_sales = date_time_series_transaction[(date_time_series_transactions >= x[0]) & (date_time_series_transactions < date_time_series_inventory[x.name + 1])]
#             sales = transactions_sales.count()
#             return sales
#         else:
#             transactions_sales = date_time_series_transaction[(date_time_series_transactions >= x[0]) & (date_time_series_transactions < date_time_series_inventory[x.name + 1])]
#             sales = transactions_sales.count()
#             return sales
    
#     product_sale_column = inventory.df[[inventory_column_date_time]].apply(lambda x: calculateSales(x, date_time_series_transactions, date_time_series_inventory), axis = 1)
#     return product_sale_column

# sales_df = inventory_df.drop(columns = ['date_time', 'Blauwe bessen.1', 'Rundergehakt.1', 'Unox Gelderse rookworst.1', 'Biologisch rundergehakt.1'])

# for productName, contents in sales_df.items():
#     if productName != 'before or after delivery' and productName != 'day':
#         # productID = convertNameToProductID(products, productName)
#         product_sale_column = calculateSalesOfItem(inventory, transactions, 'date_time', 'date_time', productName)
#         sales_df[productName] = product_sale_column

# sales_df = sales_df[sales_df['before or after delivery'] == 'after'].drop(columns = ['before or after delivery'])

# # # sales_df.to_pickle('./df_inventory/inventory_sales_delivery_at_16.pkl')
# # # sales_df.to_pickle('./df_inventory/inventory_sales_delivery_at_12.pkl')

# # # # print(pd.read_pickle('./df_inventory/inventory_sales_delivery_at_16.pkl'))
# # # print(pd.read_pickle('./df_inventory/inventory_sales_delivery_at_12.pkl'))

# sales_df.to_csv('./data/sales/inventory_sales_delivery_at_12.csv')
