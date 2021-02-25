def product_difference(before, after):
    after1 = after.set_index('day')
    before1 = before.set_index('day')
    
    df = after1.copy()
    
    for product in after1:#.loc[:,'Komkommer':]:
        for day in range(len(after1)-1):
            day_after = after1.index[day]
            day_before = after1.index[day + 1]
            difference = ((after1[product][day_after]) - (before1[product][day_before]))
            df[product][day_after] = difference
            
            
    return df
