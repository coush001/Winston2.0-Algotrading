import csv
import pandas as pd


def get_signal_and_stocks(datapath='../DataMining/data/stockwitswatched.csv'):
    d = {'date':[],'tick':[],'move':[]}
    print(d)
    with open(datapath, newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',')
        for count, row in enumerate(spamreader):
            if count == 0:
                continue
            d['date'].append(row[0])
            d['tick'].append(row[1])
            d['move'].append(float(row[-1]))
    print(d)
    df = pd.DataFrame(d)
    print('DF:  ', df)

    hot_pick = {'date':[],'tick':[]}
    for i in df.date.unique(): # return the hotest stock each day.
        print('=====', type(i))
        days_data = df.where(df.date==i).dropna()
        print(i)
        print(df.loc[days_data['move'].idxmax()][-2])
        hot_pick['date'].append(i)
        hot_pick['tick'].append(df.loc[days_data['move'].idxmax()][-2])
    print(hot_pick)

    return df.tick.unique(), hot_pick
