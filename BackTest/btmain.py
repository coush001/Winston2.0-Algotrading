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

        self.orders = [None]*len(self.datas)
        self.names = [item._name for item in self.datas]

        self.hot_stock = None
        self.hot_index = None
        self.bar_executed = [None] * len(self.datas)

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            return
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log('BUY EXECUTED AT, %.2f' % order.executed.price)
            elif order.issell():
                self.log('SELL EXECUTED AT, %.2f' % order.executed.price)

            self.bar_executed[self.hot_index] = len(self)

        elif order.status in [order.Cancelled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')
        for count, i in enumerate(self.orders):
            self.orders[count] = None

    def next(self):
        # start day
        self.log('===')

        # whats hot
        todays_hot = swDataConverter.whats_hot(self.lines.datetime.date())
        print('- todays_hot:', todays_hot)
        self.hot_stock = todays_hot


        # order list
        for i in self.orders:
            if i:# if order pending
                return

        # Buy stock
        if todays_hot != 0:
            self.hot_index = self.names.index((todays_hot))
            self.orders[self.hot_index] = self.buy(data=self.datas[self.hot_index], size=100)
            # Todo : Assert buy same day
        print('BAR EXE', self.bar_executed)

        # close position
        for i in self.bar_executed:
            if i != None and len(self) >= (i+1):
                self.orders[self.hot_index] = self.sell(data=self.datas[self.hot_index])


if __name__ == '__main__':
    todaystr = datetime.datetime.now().date().__str__()
    print('=== Today is:', dir(todaystr))
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
        data = bt.feeds.PandasData(dataname=yf.download(i, '2022-08-19', todaystr), name=i)
        cerebro.adddata(data)

# running back test
    cerebro.broker.setcash(1000)
    print('\n=== Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())
    cerebro.run()
    print('\n=== Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
    cerebro.plot()
