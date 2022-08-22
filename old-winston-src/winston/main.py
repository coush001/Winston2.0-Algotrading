from broker import Broker
from modelmachine import *
from datamachine import *


def run():

    broker = Broker()
    broker.login()
    broker.oauth_login()

    # Data and model run code:
    BOOHOO_algo = MomentumModel("GBPUSD")
    BOOHOO_algo.get_data()
    signal = BOOHOO_algo.model_output() # [buy/sell, symbol, size

    if signal[0] == 1:
        print(signal,  'means buy')
        broker.buy(signal[1], signal[2])

    elif signal[0] == -1:
        print(signal, 'means sell')
        broker.sell(signal[1], signal[2])
    else: pass

    broker.logout()


if __name__ == "__main__":

    run()
