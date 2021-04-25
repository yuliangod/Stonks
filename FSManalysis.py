from Stonks import Funds

#set up arguments for Funds class
csv2 = 'C:/Users/acer/Documents/Python_Scripts/Stonks/fsm-pricehistory-2021-03-10.csv'
dividend_csv = 'C:/Users/acer/Documents/Python_Scripts/Stonks/fsmdividends.csv'
a = Funds(csv2, dividend_csv)

a.fund_dividends('Wells Fargo US Large Cap Growth Fund Cl A Acc USD')       #extract dividend yield of a fund from csv
a.riskreturn('Wells Fargo US Large Cap Growth Fund Cl A Acc USD', include_dividends = True)     #calculate risk and return values of a fund, can set whether dividends are included in calculatiosn of returns
a.correlation('Wells Fargo US Large Cap Growth Fund Cl A Acc USD', 'Wells Fargo US All Cap Growth Fund Cl A Acc USD')       #calculate correlation between 2 funds



#a.riskreturn_graph('Wells Fargo US Large Cap Growth Fund Cl A Acc USD')     #generate risk return graph of all funds scraped from FSM website, argument is filename of graph