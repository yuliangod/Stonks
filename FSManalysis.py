from Stonks import Funds

#set up arguments for Funds class
csv2 = 'C:/Users/acer/Documents/Python_Scripts/Stonks/fsm-pricehistory-2021-03-10.csv'
dividend_csv = 'C:/Users/acer/Documents/Python_Scripts/Stonks/fsmdividends.csv'
a = Funds(csv2, dividend_csv)

dividends = a.fund_dividends('Fullerton Asia Income Return A SGD')       #extract dividend yield of a fund from csv
print(f"Dividend yield is {dividends}%")

stock, returns, risk = a.riskreturn('Fullerton Asia Income Return A SGD', include_dividends=True)   #calculate risk and return values of a fund, can set whether dividends are included in calculation of returns
print(f'Risk of {stock} is {risk}, returns of {stock} is {returns}')

correlation = a.correlation('Wells Fargo US Large Cap Growth Fund Cl A Acc USD', 'Wells Fargo US Large Cap Growth Fund Cl A Acc USD')       #calculate correlation between 2 funds
print(f'Correlation between the two funds is {correlation}')



a.riskreturn_graph("22-5-21-FSM")     #generate risk return graph of all funds scraped from FSM website, argument is filename chart will be saved as
