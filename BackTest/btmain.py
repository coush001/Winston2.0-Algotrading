import backtrader as bt
import datetime  # For datetime objects
import swDataConverter
import yfinance as yf
import pandas as pd


# Create a Strategy
class Strategy(bt.Strategy):

    def log(self, txt, dt=None):
        ''' Logging function fot this strategy'''
        dt = dt or self.lines.datetime.date()
        print('LOG:  %s, %s' % (dt, txt))

    def __init__(self):
        # Keep a reference to the "close" line in the data[0] dataseries
        self.dataclose = self.datas[2].close
        print('\n=== Init Strategy',
              '\n-Total datas: ', len(self.datas),
              '\n-Datas are: ',
        )
        for i in self.datas:
            print(i._name)
        print('\n')

    def next(self):
        self.log('===')
        print(self.lines.datetime.date())
        # TODO: handle case where date not in hot_stocks
        # TODO: Place order on hot stock
        # TODO: close order after 1 day
        # TODO: manage order status
        print(swDataConverter.whats_hot(self.lines.datetime.date()))




if __name__ == '__main__':

    # Getting strategy data
    uniqTick, hot_tick = swDataConverter.get_signal_and_stocks()  # 1. get uniq stocks and all hot picks
    print("\n=== Hot tick is\n", hot_tick)
    print('\n===Unique tics are:\n', uniqTick)

    # creating engine and strategy
    cerebro = bt.Cerebro()
    cerebro.addstrategy(Strategy)

# adding stock data - all unique datas
    for i in uniqTick:
        print(i)
        data = bt.feeds.PandasData(dataname=yf.download(i, '2022-08-23', '2022-08-27'), name=i)
        cerebro.adddata(data)


# running back test
    cerebro.broker.setcash(1996)
    print('\n=== Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())
    cerebro.run()
    print('\n=== Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
    # cerebro.plot()
