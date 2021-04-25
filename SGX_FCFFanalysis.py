from Stonks import SGXstocks
from Stonks import tickers_to_csv
import traceback
from SGXtickers_list import sgx_dividend_tickers
import pandas as pd

dividend_stocks_list = sgx_dividend_tickers(1000)
csv_name = 'sgx_dividend_stocks'
tickers_to_csv(dividend_stocks_list,csv_name)
sgx_dividend_stocks_csv = f'C:/Users/acer/Documents/Python_Scripts/Stonks/{csv_name}.csv'

c = SGXstocks(sgx_dividend_stocks_csv, timeframe=250)

failed_tickers = []
successful_tickers = []

df = pd.DataFrame()
for tickers in dividend_stocks_list[1:]:   
  try:
    df2 = c.FCFF_analysis(tickers)
    df = pd.concat([df,df2])
    print(tickers)
    print(dividend_stocks_list.index(tickers))
    successful_tickers.append(tickers)    
  except Exception: 
    traceback.print_exc()
    failed_tickers.append(tickers)
    print(f"The program could not analyse these tickers: {failed_tickers}")
    continue
df = df.sort_index(level='Percentage undervalued', ascending=False)
df.to_excel('./Dividend_analysis/sgx_FCFF_analysis.xlsx')
print(f"The program could not analyse these tickers: {failed_tickers}")
