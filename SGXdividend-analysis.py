from Stonks import SGXstocks
from Stonks import tickers_to_csv
import traceback
from SGXtickers_list import sgx_dividend_tickers
import pandas as pd

csv = 'C:/Users/acer/Documents/Python_Scripts/Stonks/test.csv'
csv2 = 'C:/Users/acer/Documents/Python_Scripts/Stonks/fsm-pricehistory-2021-03-10.csv'
list2 = ['SPY', '575.SI', 'BKY.SI', 'BKW.SI', '5PF.SI', 'M12.SI', 'M11.SI', 'AWZ.SI', 'S71.SI', '558.SI']          #always include SPY in list as it is used to calculate beta

dividend_stocks_list = sgx_dividend_tickers(1000)
csv_name = 'sgx_dividend_stocks'
#tickers_to_csv(dividend_stocks_list,csv_name)
sgx_dividend_stocks_csv = f'C:/Users/acer/Documents/Python_Scripts/Stonks/{csv_name}.csv'

c = SGXstocks(sgx_dividend_stocks_csv, timeframe=250)

failed_tickers = []
successful_tickers = []

df = pd.DataFrame()
for tickers in dividend_stocks_list[1:]:   
  try:
    df2 = c.dividend_analysis(tickers)
    df = pd.concat([df,df2])
    print(tickers)
    print(dividend_stocks_list.index(tickers))
    successful_tickers.append(tickers)    
  except Exception: 
    traceback.print_exc()
    failed_tickers.append(tickers)
    print(f"The program could not analyse these tickers: {failed_tickers}")
    continue

df = df.groupby(['Price to fair value', 'Symbol', 'Year']).mean()
print(df)
df.to_excel('./Dividend_analysis/sgx_dividend_analysis.xlsx')
print(f"The program could not analyse these tickers: {failed_tickers}")

#add image of price history to excel
print(successful_tickers)
for tickers in successful_tickers:
  c.plot_price_graph(tickers)

