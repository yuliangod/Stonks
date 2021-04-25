import pandas as pd
import matplotlib.pyplot as plt
import mpld3
from mpld3 import plugins
import numpy as np
from datetime import date
import math
import yfinance as yf
import re
from financials_scraper import financials
import openpyxl 
import traceback
from sgxscraper import sgx_scraper
from SGXtickers_list import sgx_market_cap

def tickers_to_csv(list_of_tickers, csv_name):
  ' '.join(list_of_tickers)
  data = yf.download(list_of_tickers, period = '2y')
  print(data)
  data1 = data['Close']
  data1.to_csv('%s.csv'%csv_name)
  #still missing dividend data


class Stonks:

    def __init__(self, csv, timeframe=56):
        self.csv = csv
        self.timeframe = timeframe
    
    def pricehistory(self, stock):
        timeframe = self.timeframe
        df = pd.read_csv(self.csv, thousands=',')
        stock = df[stock].dropna()
        stock = stock.iloc[-timeframe:]
        stock = stock.reset_index(drop=True)
        return(stock)

    def year_end_price(self, stock, year):
        data = yf.download(stock, start=f'{year}-11-01', end=f'{year}-12-31')
        return data['Close'][-1]
        
    def correlation(self, stock1, stock2):
        #pull out data for stock 1 & 2 and store it in a dataframe
        stock1_price = self.pricehistory(stock1)
        stock2_price = self.pricehistory(stock2)

        #create new dataframe with values needed for correlation calculation
        df3 = pd.DataFrame()
        df3[stock1] = stock1_price
        df3[stock2] = stock2_price
        df3 = df3.dropna()
        print(df3)

        stock1_mean = stock1_price.mean()
        stock2_mean = stock2_price.mean()
        df3['a'] = df3[stock1] - stock1_mean
        df3['b'] = df3[stock2] - stock2_mean
        df3['axb'] = df3['a'] * df3['b']
        df3['a_square'] = (df3['a'])**2
        df3['b_square'] = (df3['b'])**2

        #final calculation
        correlation = (df3['axb'].sum())/(math.sqrt(df3['a_square'].sum()*(df3['b_square'].sum())))

        print(correlation)
        return(correlation)
        #plt.plot(stock1_price,color='g')
        #plt.plot(stock2_price,color='b')
        #plt.show()

    def riskreturn(self, stock1):
        timeframe = self.timeframe
        stock = self.pricehistory(stock1)
        print(stock)
        series = pd.Series([], dtype='float64')
        if len(stock) == timeframe:
          for i in range(int(timeframe - 1)):
            n = int(i + 1)
            Cn1 = stock[n]
            Cn = stock[i]
            ln_returns = pd.Series([math.log(Cn1/Cn)])
            series = series.append(ln_returns)
          volatiliity1 = series.std()
          #calculate average returns

          starting_price1 = stock[0]
          average_returns1 = ((stock.mean()-starting_price1)/starting_price1)*100
          return stock1,average_returns1,volatiliity1
        else: 
          print(f'{stock1} has not enough price data for risk return data') 

    def riskreturn_graph(self, filename):
        df = pd.read_csv(self.csv, thousands=',')
        #create empty dataframe for stock name, volatility, and average returns(%)
        graph_df = pd.DataFrame(columns=['Name','Returns', 'Volatility'])

        #create loop to run risk return function for all stock symbols
        for column in df.columns[1:]:           #start index from 1 because 0 is date column
            print(column)
            stock1,average_returns1,volatility1 = self.riskreturn(column)
            new_row = {'Name':stock1,'Returns':average_returns1,'Volatility':volatility1}
            graph_df = graph_df.append(new_row,ignore_index = True)
            print(graph_df)

        #creating matplotlib graphs
        fig, ax = plt.subplots()
        ax.grid(True, alpha=0.3)

        #give stock name when hovering above it
        # Define some CSS to control our custom labels
        css = """
        table
        {
          border-collapse: collapse;
        }
        th
        {
          color: #ffffff;
          background-color: #000000;
        }
        td
        {
          background-color: #cccccc;
        }
        table, th, td
        {
          font-family:Arial, Helvetica, sans-serif;
          border: 1px solid black;
          text-align: right;
        }
        """
        labels = []
        for i in range(len(graph_df['Name'])):
            label = graph_df.iloc[[i], :].T
            label.columns = ['Row {0}'.format(i)]
            # .to_html() is unicode; so make leading 'u' go away with str()
            labels.append(str(label.to_html()))

        points = ax.plot(graph_df.Volatility,graph_df.Returns, 'o', color='b', mec='k', ms=1, mew=1, alpha=.6)

        tooltip = plugins.PointHTMLTooltip(points[0], labels,voffset=10, hoffset=10, css=css)
        plugins.connect(fig, tooltip)

        #save file as html to be able to interact with it in the future
        html_str = mpld3.fig_to_html(fig)
        Html_file= open("%s%s%s%s.html"%(self.timeframe, filename, 'fsm-riskreturn-',date.today()),"w")
        Html_file.write(html_str)
        Html_file.close()

class Funds(Stonks):
  def __init__(self, csv, dividend_csv, timeframe=56):
    super().__init__(csv, timeframe)
    self.dividend_csv = dividend_csv

  def fund_dividends(self, stock):
      timeframe = self.timeframe
      dividend_csv = self.dividend_csv
      dividend_csv = pd.read_csv(dividend_csv)
      dividend_csv = dividend_csv.fillna('0%')
      dividend_csv['Fund Name'] = dividend_csv['Fund Name'].str.strip()
      dividend_csv = dividend_csv.set_index('Fund Name')
      annual_dividend = dividend_csv.loc[stock,'Indicated Gross <br\/> Dividend Yield* (%)']
      regex = re.compile(r'(.*)%')
      mo = regex.search(annual_dividend)
      annual_dividend = mo.group(1)
      dividend = timeframe/253 * float(annual_dividend)
      print(dividend)
      return(dividend)

  def riskreturn(self, stock1, include_dividends = True):
        timeframe = self.timeframe
        stock = self.pricehistory(stock1)
        print(stock)
        print(stock)
        series = pd.Series([], dtype='float64')
        if len(stock) == timeframe:
          for i in range(int(timeframe - 1)):
            n = int(i + 1)
            Cn1 = stock[n]
            Cn = stock[i]
            ln_returns = pd.Series([math.log(Cn1/Cn)])
            series = series.append(ln_returns)
          volatiliity1 = series.std()
          #calculate average returns

          starting_price1 = stock[0]
          average_returns1 = ((stock.mean()-starting_price1)/starting_price1)*100
          if include_dividends == True:
            dividend = self.fund_dividends(stock1)
            average_returns1 = average_returns1 + dividend
          return stock1,average_returns1,volatiliity1
        else:
          average_returns1, volatiliity1 = 0,0
          return stock1,average_returns1,volatiliity1

class Stocks(Stonks):
  def __init__(self, csv, timeframe=56):
    super().__init__(csv, timeframe)

  def plot_price_graph(self, stock):
        stock_graph = self.pricehistory(stock)
        fig, ax = plt.subplots()
        ax.set(title = stock, xlabel = 'Date', ylabel = 'Price')

        plt.plot(stock_graph)
        graph_name = stock.replace('.','_')
        graph = f'Dividend_analysis/{graph_name}.png'
        plt.savefig(graph)
        path = r'Dividend_analysis/sgx_dividend_analysis.xlsx'

        #read excel sheet to know where to attach image
        df = pd.read_excel(path)
        idx = df[df["Symbol"]==stock].index[0] + 2

        #add image to sheet
        wb = openpyxl.load_workbook(path)
        ws = wb.active

        img = openpyxl.drawing.image.Image(graph)
        img.height = 200
        img.width = 300
        img.anchor = f'T{idx}'

        ws.add_image(img)
        wb.save(path)
        plt.close('all')

  def Beta(self, stock, index='SPY'):
    correlation = self.correlation(stock, index)
    volatility = (self.riskreturn(stock))[-1]
    index_volatility = (self.riskreturn(index))[-1]
    beta = correlation * (volatility/index_volatility)
    print(beta)
    return beta

  def expected_return(self, stock, Rf = 0.017, Rm = 0.025):
      beta = self.Beta(stock)
      Er = Rf + beta*(Rm - Rf)
      print(Er)
      return(Er)

  def income_sheet_stats(self, stock):
    IS = financials(stock)
    IS = IS.get_income_statement()
    IE = IS['Interest expense'][0]
    IE = float(IE.replace(',',''))    # remove commas
    ITE = IS['Income tax expense'][0]
    ITE = float(ITE.replace(',',''))
    IBT = IS['Income before tax'][0]
    IBT = float(IBT.replace(',',''))
    print(IE, ITE, IBT)
    return(IE, ITE, IBT)

  def balance_sheet_stats(self, stock):
    BS = financials(stock)
    BS = BS.get_balance_sheet()
    current_debt = BS['Current debt'][0]
    current_debt = float(current_debt.replace(',',''))  #remove commas
    longterm_debt = BS['Long-term debt'][0]
    longterm_debt = float(longterm_debt.replace(',',''))  #remove commas
    print(current_debt)
    print(longterm_debt)
    return(current_debt,longterm_debt)

  def dividend_analysis(self, stock):
    #extract dividends
    stock1 = yf.Ticker(stock)
    stock1 = stock1.dividends
    print(stock1)
    #stock = stock.index().dt.year
    dividend_df = pd.DataFrame()    #create empty dataframe to store info
    for row_idx in range(len(stock1)):
      year = stock1.index[row_idx].year
      dividend = stock1[row_idx]
      new_row = {'Year':year,'Dividend':dividend}
      dividend_df = dividend_df.append(new_row,ignore_index = True)
    print(dividend_df)
    dividend_df = dividend_df.groupby('Year')['Dividend'].sum().reset_index()
    dividend_growthrate = [None,]    #create empty list to add as column later
    
    #calculate growth rates
    for i in range(len(dividend_df['Year'])-1):
      dividend_growthrate.append((dividend_df['Dividend'][i+1] - dividend_df['Dividend'][i])/dividend_df['Dividend'][i])
    dividend_df['Dividend Growth Rate'] = dividend_growthrate

    #calculate dividend yield 
    pricehistory = self.pricehistory(stock)
    dividend_df['Dividend yield'] = dividend_df['Dividend']/pricehistory.iloc[-1]
    
    #median dividend growth rate
    median_growthrate = dividend_df['Dividend Growth Rate'].median()
    dividend_df['Median growth rate'] = median_growthrate

    #get total debt
    current_debt, longterm_debt = self.balance_sheet_stats(stock)
    total_debt = current_debt + longterm_debt
    dividend_df['Total debt'] = total_debt

    #calculate rate debt
    IE, ITE, IBT = self.income_sheet_stats(stock)
    dividend_df['Interest expense'] = IE
    rate_debt = IE/total_debt
    dividend_df['Rate debt'] = rate_debt

    #get market cap
    info = yf.Ticker(stock)
    cap = info.info['marketCap']
    dividend_df['Market cap'] = cap

    #calculate weight of debt
    weight_of_debt = total_debt/(total_debt+cap)
    dividend_df['Weight of debt'] = weight_of_debt

    #calculate weight of equity
    weight_of_equity = 1 - weight_of_debt
    dividend_df['Weight of equity'] = weight_of_equity

    #calculate Ra
    Ra = self.expected_return(stock)
    dividend_df['Ra'] = Ra

    #get interest tax expense
    dividend_df['Income tax expense'] = ITE

    #get incoem before tax
    dividend_df['Income before tax'] = IBT

    #calculate effective tax rate
    effective_tax_rate = ITE/IBT
    dividend_df['Effective tax rate'] = effective_tax_rate

    #calculate WACC
    wacc = weight_of_debt * rate_debt * (1-effective_tax_rate) + (weight_of_equity * Ra)
    dividend_df['WACC'] = wacc

    if wacc > 0.085:
      #calculate fair value
      D0 = dividend_df.loc[dividend_df['Year'] == 2020.0,'Dividend']
      D0 = float(D0.values[0])
      fair_value = (D0*(1 + median_growthrate))/(wacc - median_growthrate)
      dividend_df['Fair value'] = fair_value
    else:
      #calculate fair value but set wacc at 9%
      D0 = dividend_df.loc[dividend_df['Year'] == 2020.0,'Dividend']
      D0 = float(D0.values[0])
      fair_value = (D0*(1 + median_growthrate))/(0.09 - median_growthrate)
      dividend_df['Fair value'] = fair_value

    #calculate dividend payout ratio
    eps = info.info['trailingEps']
    dividend_payout_ratio = D0/eps
    dividend_df['Dividend payout ratio'] = dividend_payout_ratio

    #save to excel sheet
    path = r'C:/Users/acer/Documents/Python_Scripts/Stonks/Dividend_analysis/dividendanalysis.xlsx' 
    book = openpyxl.load_workbook(path)
    writer = pd.ExcelWriter(path, engine = 'openpyxl')
    writer.book = book

    dividend_df.to_excel(writer, sheet_name = stock)
    writer.save()
    writer.close()  

    self.plot_price_graph(stock)

class SGXstocks(Stocks):
    def __init__(self,csv,timeframe=250):
      super().__init__(csv, timeframe)

    def dividend_analysis(self,stock,year='2020'):
      for i in range(3):
        try:
          tables = sgx_scraper(stock)
          IS = tables[0]
          BS = tables[1]
          E = float(BS.loc['Total Equity', year])   #try to find total equity in balance sheet to ensure tables were scraped properly
          CF = tables[2]
          break
        except:
          continue

      #extract dividends payed out per year
      stock1 = yf.Ticker(stock)
      stock1 = stock1.dividends
      print(stock1)
      #stock = stock.index().dt.year
      dividend_df = pd.DataFrame()    #create empty dataframe to store info
      for row_idx in range(len(stock1)):
        dividend_year = stock1.index[row_idx].year
        dividend = stock1[row_idx]
        new_row = {'Year':dividend_year,'Dividend':dividend}
        dividend_df = dividend_df.append(new_row,ignore_index = True)
      print(dividend_df)
      dividend_df = dividend_df.groupby('Year')['Dividend'].sum().reset_index()
      dividend_growthrate = [None,]    #create empty list to add as column later

      #calculate growth rates
      for i in range(len(dividend_df['Year'])-1):
        dividend_growthrate.append((dividend_df['Dividend'][i+1] - dividend_df['Dividend'][i])/dividend_df['Dividend'][i])
      dividend_df['Dividend Growth Rate'] = dividend_growthrate

      #calculate standard diviation of growth rates to rank tickers for easier screening
      growth_rate_std = dividend_df['Dividend Growth Rate'].std
      dividend_df['SD of div growth rate'] = growth_rate_std(skipna=True)

      #calculate dividend yield based on EOY price
      todays_date = date.today() 
      current_year = float(f'{todays_date.year}.0')     #get current year to avoid error in loop
      dividend_yield = []
      eoyprice = []
      latest_price = list(self.pricehistory(stock))[-1]
      for i in range(len(dividend_df['Year'])):
        print(i)
        
        if dividend_df['Year'][i] == current_year:        #as this is the current year, eoy price is not released yet so get current price to calculate yield instead
          latest_dividend = dividend_df['Dividend'].iloc[-1]
          dividend_yield.append(latest_dividend/latest_price)
          eoyprice.append(latest_price)
        else:
          divyear = int(dividend_df['Year'][i]//1)
          eoy_price = self.year_end_price(stock, divyear)
          eoyprice.append(eoy_price)
          divamount = dividend_df['Dividend'][i]
          dividend_yield.append(divamount/eoy_price)
          
      dividend_df['EOY Price'] = eoyprice
      dividend_df['Dividend Yield'] = dividend_yield

      #median dividend growth rate
      median_growthrate = dividend_df['Dividend Growth Rate'].median()
      dividend_df['Median growth rate'] = median_growthrate      

      #calculate dividend payout ratio
      info = yf.Ticker(stock)
      eps = info.info['trailingEps']
      D0 = dividend_df.loc[dividend_df['Year'] == float(f'{year}.0'),'Dividend']
      D0 = float(D0.values[0])
      dividend_payout_ratio = D0/eps
      dividend_df['Dividend payout ratio'] = dividend_payout_ratio

      #get total equity
      total_equity = float(BS.loc['Total Equity', year])
      dividend_df['Total Equity'] = total_equity

      #get total debt
      total_debt = float(BS.loc['Total Debt', year])
      dividend_df['Total debt'] = total_debt

      #Cost of equity
      BL = self.Beta(stock)*(1+(1-0.17)*(total_debt/total_equity))
      dividend_df['Leveled Beta'] = BL
      cost_of_equity = 0.01559 + BL*(0.0456) + 0.0472
      dividend_df['Cost of equity'] = cost_of_equity

      #Prepare data to calculate cost of debt
      IE = float(IS.loc['Interest Inc.(Exp.),Net-Non-Op., Total', year]) * -1
      if IE == 0:
        IE = 0.000000000000000001
      EBIT = float(IS.loc['Operating Income', year])
      stock_ICR = EBIT/IE     #interest coverage ratio
      info = yf.Ticker(stock)
      cap = (info.info['marketCap'])/1000000    #get market cap

      LargeCapCDS_df = pd.read_csv('LargeCapCDS.csv')
      SmallCapCDS_df = pd.read_csv('SmallCapCDS.csv')

      #get CDS based on market cap
      if cap <= 5000:
        ICR_list = list(SmallCapCDS_df[">"])
        ICR_list.append(stock_ICR)
        ICR_list.sort(reverse=True)
        spread_idx = ICR_list.index(stock_ICR)
        CDS = float(SmallCapCDS_df['Spread is'][spread_idx].replace("%",""))/100
      else:
        ICR_list = list(LargeCapCDS_df[">"])
        ICR_list.append(stock_ICR)
        ICR_list.sort(reverse=True)
        spread_idx = ICR_list.index(stock_ICR)
        CDS = float(LargeCapCDS_df['Spread is'][spread_idx].replace("%",""))/100     
      dividend_df['Company Default Spread'] = CDS

      #cost of debt
      cost_of_debt = 0.01559 + CDS
      dividend_df['Cost of debt'] = cost_of_debt 

      #market value of equity
      dividend_df['Market cap'] = cap
      
      #market value of debt
      market_value_of_debt = total_debt + IE
      dividend_df['Market value of debt'] = market_value_of_debt

      #Corporate tax rate
      Tc = float(IS.loc['Provision for Income Taxes', year])/float(IS.loc['Net Income Before Taxes', year])
      dividend_df['Corporate tax rate'] = Tc

      #calculate WACC
      wacc = ((cap/(cap + market_value_of_debt))*cost_of_equity) + ((market_value_of_debt/(cap + market_value_of_debt))*cost_of_debt*(1-Tc))
      dividend_df['WACC'] = wacc

      #calculate FCFF
      CapEx = float(CF.loc['Capital Expenditures', year])
      Depreciation = float(CF.loc['Depreciation/Depletion', year])
      non_cashItems = float(CF.loc['Non-Cash Items', year])
      workingCapital = float(CF.loc['Changes in Working Capital', year])
      FCFF = EBIT*(1-Tc) + CapEx + Depreciation + non_cashItems + workingCapital
      dividend_df['FCFF'] = FCFF  

      #calculate reinvestment rate with data from previous year
      CapEx_prev = float(CF.loc['Capital Expenditures', str(int(year) - 1)])
      Depreciation_prev = float(CF.loc['Depreciation/Depletion', str(int(year) - 1)])
      non_cashItems_prev = float(CF.loc['Non-Cash Items', str(int(year) - 1)])
      
      NetCapEx_prev = - CapEx_prev - Depreciation_prev - non_cashItems_prev
      workingCapital_prev = float(CF.loc['Changes in Working Capital', str(int(year) - 1)])
      EBIT_prev = float(IS.loc['Operating Income', str(int(year) - 1)])
      Tc_prev = float(IS.loc['Provision for Income Taxes', str(int(year) - 1)])/float(IS.loc['Net Income Before Taxes', str(int(year) - 1)])

      reinvestment_rate = (NetCapEx_prev - workingCapital_prev)/(EBIT_prev*(1-Tc_prev))
      dividend_df['Reinvestment rate'] = reinvestment_rate

      #calculate return on capital
      cash = float(BS.loc['Cash', year])
      ROC = (EBIT*(1 - Tc))/(total_equity + total_debt - cash)
      dividend_df['Return on capital'] = ROC

      #calculate expected growth rate
      expected_growth_rate = reinvestment_rate * ROC

      #project EBIT
      EBIT_t5 = EBIT*(1 + expected_growth_rate)**5

      #caculate terminal value
      v0 = (EBIT_t5*(1-Tc)*(1-(0.01559/ROC)))/(wacc - 0.01559)
      dividend_df['Terminal value'] = v0

      #project FCFF
      projected_FCFF = v0
      for i in range(1,5):
        FCFF_t = (FCFF*(1 + expected_growth_rate)**i)/((1+wacc)**i)
        projected_FCFF += FCFF_t
      dividend_df['Present value of FCFF'] = projected_FCFF 

      #calculate fair value
      shares_outstanding = float(BS.loc['Total Common Shares Outstanding', year])
      fair_value = projected_FCFF/shares_outstanding
      dividend_df['Fair value'] = fair_value

      #calculate % undervalued
      price_to_fairvalue = latest_price/fair_value
      dividend_df['Price to fair value'] = price_to_fairvalue

      dividend_df['Symbol'] = stock

      return dividend_df

      #self.plot_price_graph(stock)

    def FCFF_analysis(self, stock):
      # scrape financial statements from sgx
      for i in range(3):
        try:
          tables = sgx_scraper(stock)
          IS = tables[0]
          BS = tables[1]
          E = BS.loc['Total Equity']   #try to find total equity in balance sheet to ensure tables were scraped properly
          CF = tables[2]
          break
        except:
          continue

      #create index of dataframe 
      fcff_df = pd.DataFrame()
      fcff_df['Year'] = list(IS.columns)
      fcff_df['Ticker'] = stock
      fcff_df = fcff_df.set_index(['Ticker', 'Year'])
      print(fcff_df)

      #loop wacc and fair value calculations through all years 
      for year in list(IS.columns):
        #get revenue
        revenue = float(IS.loc['Revenue', year])
        fcff_df.loc[(stock,year),'Revenue'] = revenue

        #get net income
        net_income = float(IS.loc['Net Income', year])
        fcff_df.loc[(stock,year),'Net Income'] = net_income

        #get total equity
        total_equity = float(BS.loc['Total Equity', year])
        fcff_df.loc[(stock,year),'Total Equity'] = total_equity

        #get total debt
        total_debt = float(BS.loc['Total Debt', year])
        fcff_df.loc[(stock,year),'Total debt'] = total_debt

        #Cost of equity
        BL = self.Beta(stock)*(1+(1-0.17)*(total_debt/total_equity))
        fcff_df.loc[(stock,year),'Leveled Beta'] = BL
        cost_of_equity = 0.01559 + BL*(0.0456) + 0.0472
        fcff_df.loc[(stock,year),'Cost of equity'] = cost_of_equity

        #Prepare data to calculate cost of debt
        IE = float(IS.loc['Interest Inc.(Exp.),Net-Non-Op., Total', year]) * -1
        if IE == 0:
          IE = 0.000000000000000001
        EBIT = float(IS.loc['Operating Income', year])
        stock_ICR = EBIT/IE     #interest coverage ratio
        cap = sgx_market_cap(stock)    #get market cap

        LargeCapCDS_df = pd.read_csv('LargeCapCDS.csv')
        SmallCapCDS_df = pd.read_csv('SmallCapCDS.csv')

        #get CDS based on market cap
        if cap <= 5000:
          ICR_list = list(SmallCapCDS_df[">"])
          ICR_list.append(stock_ICR)
          ICR_list.sort(reverse=True)
          spread_idx = ICR_list.index(stock_ICR)
          CDS = float(SmallCapCDS_df['Spread is'][spread_idx].replace("%",""))/100
        else:
          ICR_list = list(LargeCapCDS_df[">"])
          ICR_list.append(stock_ICR)
          ICR_list.sort(reverse=True)
          spread_idx = ICR_list.index(stock_ICR)
          CDS = float(LargeCapCDS_df['Spread is'][spread_idx].replace("%",""))/100     
        fcff_df.loc[(stock,year),'Company Default Spread'] = CDS

        #cost of debt
        cost_of_debt = 0.01559 + CDS
        fcff_df.loc[(stock,year),'Cost of debt'] = cost_of_debt 

        #market value of equity
        fcff_df.loc[(stock,year),'Market cap'] = cap

        #market value of debt
        market_value_of_debt = total_debt + IE
        fcff_df.loc[(stock,year),'Market value of debt'] = market_value_of_debt

        #Corporate tax rate
        Tc = abs(float(IS.loc['Provision for Income Taxes', year])/float(IS.loc['Net Income Before Taxes', year]))
        fcff_df.loc[(stock,year),'Corporate tax rate'] = Tc

        #calculate WACC
        wacc = ((cap/(cap + market_value_of_debt))*cost_of_equity) + ((market_value_of_debt/(cap + market_value_of_debt))*cost_of_debt*(1-Tc))
        fcff_df.loc[(stock,year),'WACC'] = wacc
        
        #calculate FCFF
        CapEx = float(CF.loc['Capital Expenditures', year])
        Depreciation = float(CF.loc['Depreciation/Depletion', year])
        non_cashItems = float(CF.loc['Non-Cash Items', year])
        workingCapital = float(CF.loc['Changes in Working Capital', year])
        FCFF = EBIT*(1-Tc) + CapEx + Depreciation + non_cashItems + workingCapital
        fcff_df.loc[(stock,year),'FCFF'] = FCFF

      # calculate fair values
      for year in list(IS.columns)[1:]:  

        #calculate reinvestment rate with data from previous year
        CapEx_prev = float(CF.loc['Capital Expenditures', str(round(float(year)) - 1)])
        Depreciation_prev = float(CF.loc['Depreciation/Depletion', str(round(float(year)) - 1)])
        non_cashItems_prev = float(CF.loc['Non-Cash Items', str(round(float(year)) - 1)])

        NetCapEx_prev = - CapEx_prev - Depreciation_prev - non_cashItems_prev
        workingCapital_prev = float(CF.loc['Changes in Working Capital', str(round(float(year)) - 1)])
        EBIT_prev = float(IS.loc['Operating Income', str(round(float(year)) - 1)])
        Tc_prev = float(IS.loc['Provision for Income Taxes', str(round(float(year)) - 1)])/float(IS.loc['Net Income Before Taxes', str(round(float(year)) - 1)])

        reinvestment_rate = (NetCapEx_prev - workingCapital_prev)/(EBIT_prev*(1-Tc_prev))
        fcff_df.loc[(stock,year),'Reinvestment rate'] = reinvestment_rate

        #calculate return on capital
        cash = float(BS.loc['Cash', year])
        ROC = (EBIT*(1 - Tc))/(total_equity + total_debt - cash)
        fcff_df.loc[(stock,year),'Return on capital'] = ROC

        #calculate expected growth rate
        expected_growth_rate = reinvestment_rate * ROC
        fcff_df.loc[(stock,year),'Expected Growth Rate'] = expected_growth_rate

        #calculate historical growth rate of revenue(to compare with expected growth rate in program)
        revenue_growth_rate = (float(IS.loc['Revenue', year]) - float(IS.loc['Revenue', str(round(float(year)) - 1)]))/float(IS.loc['Revenue', str(round(float(year)) - 1)])
        fcff_df.loc[(stock,year),'Revenue Growth Rate'] = revenue_growth_rate

        #calculate historical growth rate of net income(to compare with expected growth rate in program)
        revenue_growth_rate = (float(IS.loc['Net Income', year]) - float(IS.loc['Net Income', str(round(float(year)) - 1)]))/float(IS.loc['Net Income', str(round(float(year)) - 1)])
        fcff_df.loc[(stock,year),'Net Income Growth Rate'] = revenue_growth_rate

        #project EBIT
        EBIT_t5 = EBIT*(1 + expected_growth_rate)**5

        #caculate terminal value
        v0 = (EBIT_t5*(1-Tc)*(1-(0.01559/ROC)))/(wacc - 0.01559)
        fcff_df.loc[(stock,year),'Terminal value'] = v0

        #project FCFF
        projected_FCFF = v0
        for i in range(1,5):
          FCFF_t = (FCFF*(1 + expected_growth_rate)**i)/((1+wacc)**i)
          projected_FCFF += FCFF_t
        fcff_df.loc[(stock,year),'Present value of FCFF'] = projected_FCFF 

        #calculate fair value
        shares_outstanding = float(BS.loc['Total Common Shares Outstanding', year])
        fcff_df.loc[(stock,year),'Shares outstanding'] = shares_outstanding
        fair_value = projected_FCFF/shares_outstanding
        fcff_df.loc[(stock,year),'Fair value'] = fair_value

      #calculate percentage undervalued
      latest_price = list(self.pricehistory(stock))[-1]
      percentage_undervalued = (1 - (latest_price/fair_value))*100

      #create index again to include percentage undervalued as an index
      fcff_df.loc[stock,'Percentage undervalued'] = percentage_undervalued
      fcff_df['Year'] = list(IS.columns)
      fcff_df['Ticker'] = stock
      fcff_df = fcff_df.set_index(['Ticker', 'Percentage undervalued', 'Year'])

      return fcff_df

if __name__ ==  "__main__": 

    #testing fcff function
    csv_name = 'sgx_dividend_stocks'
    sgx_dividend_stocks_csv = f'C:/Users/acer/Documents/Python_Scripts/Stonks/{csv_name}.csv'

    c = SGXstocks(sgx_dividend_stocks_csv, timeframe=250)
    fcff_df = c.FCFF_analysis('AWX.SI')
    print(fcff_df)