import pandas as pd

SmallCapCDS_df = pd.read_csv('SmallCapCDS.csv')

stock_ICR = 7.4

ICR_list = list(SmallCapCDS_df[">"])
ICR_list.append(stock_ICR)
ICR_list.sort(reverse=True)
spread_idx = ICR_list.index(stock_ICR)
CDS = float(SmallCapCDS_df['Spread is'][spread_idx].replace("%",""))/100

print(CDS)