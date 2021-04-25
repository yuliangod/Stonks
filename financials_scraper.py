import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import time

class financials:
    def __init__(self, stock):
        self.stock = stock

    def extract_table(self,url):
        r = requests.get(url)
        soup = bs(r.content, 'lxml')

        ls = []

        for l in soup.find_all('div'):
            ls.append(l.string)

        new_ls = list(filter(None, ls))
        new_ls = new_ls[11:-7]
        new_ls[0] = 'Annual'

        num_of_columns = soup.select('.D\(tbhg\) div')
        num_of_columns = len(num_of_columns) - 2

        bs_data = list(zip(*[iter(new_ls)]*num_of_columns))

        balance_sheet = pd.DataFrame(bs_data[0:])

        balance_sheet.columns = balance_sheet.iloc[0]   #make columns first row
        balance_sheet = balance_sheet.iloc[1:,]
        balance_sheet = balance_sheet.T
        balance_sheet.columns = balance_sheet.iloc[0]
        balance_sheet.drop(balance_sheet.index[0],inplace=True)
        balance_sheet.index.name = ''
        return(balance_sheet)

    def get_balance_sheet(self):
        stock = self.stock
        url = 'https://sg.finance.yahoo.com/quote/' + stock +'/balance-sheet'

        for i in range(3):
            try: 
                table = self.extract_table(url)
            except:
                print('retrying %s' %i)
            else:
                break
                
        print(table)
        return(table)

    def get_income_statement(self):
        stock = self.stock
        url = 'https://sg.finance.yahoo.com/quote/' + stock +'/financials'
        for i in range(3):
            try: 
                table = self.extract_table(url)
            except:
                print('retrying %s' %i)
            else:
                break
        print(table)
        return(table)

    def get_cash_flow(self):
        stock = self.stock
        url = 'https://sg.finance.yahoo.com/quote/' + stock +'/cash-flow'
        for i in range(3):
            try: 
                table = self.extract_table(url)
            except:
                print('retrying %s' %i)
            else:
                break
        print(table)
        return(table)
 
if __name__ == '__main__':
    a = financials('A26.SI')
    a.get_income_statement()


