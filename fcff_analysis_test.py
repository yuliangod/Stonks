from Stonks import SGXstocks

sgx_dividend_stocks_csv = f'C:/Users/acer/Documents/Python_Scripts/Stonks/sgx_dividend_stocks.csv'

c = SGXstocks(sgx_dividend_stocks_csv, timeframe=250)

# check company default spread function
CDS = c.CDS(300, 7.4)
if CDS == 0.0118:
    print('CDS function for small cap is working')
CDS = c.CDS(7000, 7.4)
if CDS == 0.0085:
    print('CDS function for large cap is working')

