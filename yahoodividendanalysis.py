from Stonks import Stocks
from Stonks import tickers_to_csv
import traceback

#A big limitation of this script is that data is scraped from yahoo finance website, which can only be scraped half of the time

#set up Stocks class
csv = 'C:/Users/acer/Documents/Python_Scripts/Stonks/test.csv'
list1 = ['SPY', 'AAPL', 'MSFT', 'A17U.SI','CLN.SI', 'BVP.SI','U14.SI']      #always include SPY in list as it is used for Beta calculations
csv_name = 'test'
tickers_to_csv(list1,csv_name)
b = Stocks(csv, timeframe=250)

#script similar to SGX dividend analysis except data for financials scraped from yahoo finance which is very unstable
failed_tickers = []
for tickers in list1[1:]:
  try:
    b.dividend_analysis(tickers)
    print(tickers)
    print(list1.index(tickers))
  except Exception: 
    traceback.print_exc()
    failed_tickers.append(tickers)
    continue
print(failed_tickers)       #show which tickers the script did not manage to analyse
#file will be saved in a excel sheet called dividend analysis, which will have to be manually created beforehand
