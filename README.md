#  ---_Winston2.0_---

## What?
This is an independent project to build the end to end infrastructure and strategy for an algorithmic trading platform.


## Current features:

  - Webscrape script to pull data from stock-wits.com and pulls the list of most watched stocks last 24hr 
  - Historical dataset creation via scheduled cron job / manual run to build data in .csv file
  - Data handler converts CSV to useful format, returns unique tickers and given datetime date returns 'hot stock' for that date
  - Backtesting - can run back test on strategies involving 'hot stock' placing buy orders on ticker (90% complete)

## Current development:

- Completion of back testing for basic 'hot stock' strategy


## Next

- Connection to broker for out of sample testing
- Live trading?
- Review of other potential algo trading strategies?
