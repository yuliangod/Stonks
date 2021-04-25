import pandas as pd
import numpy as np

def sgx_dividend_tickers(minCap=0):
    csv = "myData.csv"
    sgx_df = pd.read_csv(csv)
    dividend_tickers = ["SPY",]
    for index, rows in sgx_df.iterrows():
        if sgx_df.loc[index, 'Mkt Cap ($M)'] > minCap:
            if not np.isnan(rows["Yield (%)"]):
                dividend_tickers.append(f"{rows['Trading Code']}.SI")
    return dividend_tickers

def sgx_market_cap(stock):
    stock = stock.replace('.SI', '')
    csv = "myData.csv"
    sgx_df = pd.read_csv(csv)
    sgx_df = sgx_df.set_index("Trading Code")
    cap = sgx_df.loc[stock, 'Mkt Cap ($M)']
    return cap

if __name__ == '__main__':
    print(sgx_market_cap('A17U.SI'))
    #print(sgx_dividend_tickers(1000))
