import csv
import pandas as pd
from datetime import datetime


def get_signal_and_stocks(datapath='../DataMining/data/stockwitswatched.csv'):
    d = {'date':[],'tick':[],'move':[]}
    # print(d)
    with open(datapath, newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',')
        for count, row in enumerate(spamreader):
            if count == 0:
                continue
            dt = datetime.strptime(row[0], '%d/%m/%Y %H:%M:%S')
            d['date'].append(dt.date())
            d['tick'].append(row[1])
            d['move'].append(float(row[-1]))

    # The dataframe for all stockwits scraped data:
    df = pd.DataFrame(d)


    hot_pick = {'date':[],'tick':[]}
    for i in df.date.unique(): # return the hotest stock each day.
        # print('=====', type(i))
        days_data = df.where(df.date==i).dropna()
        # print(i)
        # print(df.loc[days_data['move'].idxmax()][-2])
        hot_pick['date'].append(i)
        # hot_pick['tick'].append(55)
        hot_pick['tick'].append(df.loc[days_data['move'].idxmax()][-2])

    # The dataframe for unique hot picks pulled from stockwits
    hs = pd.DataFrame(hot_pick)
    uniq_tick = hs.tick.unique()

    print('\n=== Stockwits data created:\n- unique ticks and hot_pick for:', datapath)
    print('- Total data collections made: ', int(len(df)/10),
          '\n- Unique days data: ', len(hs))

    # print(hs)
    return uniq_tick, hs



def whats_hot(dt):
    uniqTick, hot_tick = get_signal_and_stocks()
    # print(uniqTick, hot_tick)
    hot = hot_tick.where(hot_tick['date']==dt).dropna()
    print('=====', dir(hot.tick))
    return hot.tick.values[0]


# # get_signal_and_stocks()
# today = datetime.now().date()
#
# ticker = whats_hot(today)
# print('\n==== Today is: ', today, '\nthis is hot: ', ticker)