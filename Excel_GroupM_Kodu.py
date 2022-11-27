import pandas as pd
import time

def main():
    aggregate_variables = []
    prefix = 'M'

    beginning = time.time()
    start = time.time()
    print('\n\n================================================================================')
    print('Loading data... If your data contains around 1m rows and 10-15 columns, '
          'this process may take up to 2-3 minutes.')
    df_offline_copy, bds_offline_copy = load_data()
    end = time.time()
    time_elapsed = round(((end - start) / 60), 2)
    print(f'\nIt took {time_elapsed} minutes to load the data.')

    if time_elapsed >= 2:
        print('\nIt seems like it took too much time to load the data. '
              'Try to delete unnecessary columns to shorten the waiting time.')

    ## ne olur ne olmaz
    df_offline = df_offline_copy.copy()
    bds_offline = bds_offline_copy.copy()
    global aggs
    aggs = []
    global dfs
    dfs = []
    global prefixes
    prefixes=[]
    global bds
    bds = []
    if len(aggregate_variables) == 1:

        aggs = [aggregate_variables[0]]
        prefixes = [prefix]
        bds = [bds_offline]
        dfs = [df_offline]
    elif len(aggregate_variables) == 2:
        aggs = [aggregate_variables[0], aggregate_variables[1]]
        prefixes = [prefix, prefix]
        bds = [bds_offline, bds_offline]
        dfs = [df_offline, df_offline]
    else:
        print('1 veya 2 dependent variable girilmesi gerekiyor.')

    frames = []
    for i in range(len(aggs)):
        print(f'\nAggregate variable: {aggs[i]}')
        start = time.time()
        df_app = set_index2(variable_generator2(dfs[i], aggs[i], prefixes[i], bds[i]))
        frames.append(df_app)

        end = time.time()
        time_elapsed = round((end - start), 2)
        print(f'For the aggregate variable {aggs[i]} it took {time_elapsed} seconds.\n')

    result = pd.concat(frames, axis=1)
    result = result.sort_index()
    result.fillna(0, inplace=True)
    

    # dropping columns with a sum of 0.
    cols_not_to_be_dropped = [col for col in result.columns if result[col].sum() != 0]

    # number of columns that have a sum of 0.
    num_of_zeroes = len(result.columns) - len(cols_not_to_be_dropped)

    result = result[cols_not_to_be_dropped]

    # result = result.rename(index={'Date': 'date'})  # or vice-versa
    result.to_excel('OUTPUT.xlsx')

    ending = time.time()
    time_elapsed_all = round(((ending - beginning) / 60), 2)
    print(f'\n\nWhole process took {time_elapsed_all} minutes.')
    print(f'In total; {len(cols_not_to_be_dropped) + num_of_zeroes} variables have been generated. ')
    print(f'{num_of_zeroes} had a sum of 0, {len(cols_not_to_be_dropped)} variables remained.')
    print(f'You can find the generated variables in the "OUTPUT.xlsx" excel file.')

def load_data():
    """
    A basic function to load the data.
    """
    ## for offline data
    offline_breakdowns = pd.read_excel(r'breakdowns.xlsx')
    list_of_breakdowns_offline = [offline_breakdowns.iloc[row].tolist() for row in range(len(offline_breakdowns))]
    bds_offline = []
    for bd in list_of_breakdowns_offline:
        bd = [i for i in bd if pd.isnull(i) is False]
        bds_offline.append(bd)
    df_ = pd.read_excel(r'data.xlsx')
    # df_copy = df_.copy()
    # df_copy.dropna(subset=['Tarih'], axis=0, inplace=True)
    if 'Tarih' in df_.columns.tolist():
        df_.dropna(subset=['Tarih'], axis=0, inplace=True)
    df_offline = df_.copy()
    df_offline.replace('-', 0, inplace=True)

    # 2022-01-04 / added so that object and datetime confusion gets eliminated.
    df_offline['date'] = pd.to_datetime(df_offline['date'])

    return df_offline, bds_offline


def breakdown_generator(dff, list_of_breakdowns, agg, n1=0, n2=0, n3=0, n4=0):
    """
    Main aim is to create a list of sub category breakdowns from given column names using a threshold value to block certain breakdowns to be generated.
    This threshold represents the weight of the selected sub category breakdown wrt total spend in that general breakdown.
    """
    all_breakdowns = []
    for bd in list_of_breakdowns:
        if len(bd) == 1:
            threshold = n1
        elif len(bd) == 2:
            threshold = n2
        elif len(bd) == 3:
            threshold = n3
        else:
            threshold = n4
        dff_ = dff.groupby(bd).agg({agg: 'sum'})
        dff_['% of grand total'] = dff_[agg] / dff_[agg].sum()
        dff_ = dff_[dff_['% of grand total'] >= threshold]
        dff_ = dff_.reset_index()

        ## bd'leri ekle listelere
        dff_bd = dff_[bd]
        breakdowns = [bd + dff_bd.loc[row].tolist() for row in range(len(dff_bd))]

        all_breakdowns.extend(breakdowns)

    return all_breakdowns

def create_empty_date_df2(dff):
    """
    just creates an empty dataframe.
    """
    df_dates = dff[['date']]

    df_dates = df_dates.drop_duplicates()
    return df_dates


def variable_generator2(dff, agg, prefix, list_of_bds):
    """
    combines all of the functions above and creates the variables.
    """
    df_merged = create_empty_date_df2(dff)
    df_bridge = pd.DataFrame()
    df_bridge['date'] = ''

    for breakdown in breakdown_generator(dff, list_of_bds, agg):
        length = len(breakdown)
        if length == 8:
            df_aggregated = dff[(dff[breakdown[0]] == breakdown[4]) & (dff[breakdown[1]] == breakdown[5]) &
                                (dff[breakdown[2]] == breakdown[6]) & (dff[breakdown[3]] == breakdown[7])] \
                .groupby('date').agg({agg: 'sum'}).reset_index()
            df_aggregated.columns = ['date',
                                     prefix + '_' + breakdown[4] + '_' + breakdown[5] + '_' + breakdown[6] + '_' +
                                     breakdown[7] + '_' + agg]

        if length == 6:
            df_aggregated = dff[(dff[breakdown[0]] == breakdown[3]) & (dff[breakdown[1]] == breakdown[4]) &
                                (dff[breakdown[2]] == breakdown[5])] \
                .groupby('date').agg({agg: 'sum'}).reset_index()
            df_aggregated.columns = ['date',
                                     prefix + '_' + breakdown[3] + '_' + breakdown[4] + '_' + breakdown[5] + '_' + agg]

        if length == 4:
            df_aggregated = dff[(dff[breakdown[0]] == breakdown[2]) & (dff[breakdown[1]] == breakdown[3])] \
                .groupby('date').agg({agg: 'sum'}).reset_index()
            df_aggregated.columns = ['date',
                                     prefix + '_' + breakdown[2] + '_' + breakdown[3] + '_' + agg]

        if length == 2:
            df_aggregated = dff[(dff[breakdown[0]] == breakdown[1])] \
                .groupby('date').agg({agg: 'sum'}).reset_index()
            df_aggregated.columns = ['date',
                                     prefix + '_' + breakdown[1] + '_' + agg]

        df_bridge = df_bridge.merge(df_aggregated, on='date', how='outer')

    df_bridge = df_bridge.merge(df_merged, on='date', how='outer')

    df_bridge.fillna(0, inplace=True)
    df_bridge.drop_duplicates(inplace=True)
    # if agg == 'Net Tutar':
    #     new_cols = [col + '_tl' if (col != 'date') else col for col in df_bridge.columns.tolist()]
    # else:
    #     new_cols = [col + '_grp' if (col != 'date') else col for col in df_bridge.columns.tolist()]
    # df_bridge.columns = new_cols

    return df_bridge

def set_index2(dff, weekly=True):
    """
    sets the index of the generated variable to its dates.
    """
    dates = dff['date'].tolist()
    new_dates = []
    for row in range(len(dates)):
        dt = dates[row]
        dt = dt.strftime("%Y-%m-%d")
        new_dates.append(dt)
    dff['date'] = new_dates
    dff_out = dff.set_index('date', drop=True)
    # dff_out = dff.drop('date', axis=1)

    return dff_out


if __name__ == "__main__":
    main()