from tkinter import *
from PIL import ImageTk, Image
from Stonks import SGXstocks
import pandas as pd
from tkinter import messagebox
from tkinter import filedialog

root = Tk()
root.title('StonksApp')
spreadsheet_location = "Empty"


#################################################################################################### FIRST FRAME ###############################################################################
def search():   #search whether stock is in csv
    global ticker
    global dividend_analysis_df 
    global D0
    global wacc
    global Total_Equity
    global Total_Debt
    global Cost_of_Equity
    global Cost_of_Debt
    global corporatetax

    ticker = input_stockname.get()
    print(ticker)
    if spreadsheet_location == "Empty":
        messagebox.showerror("Error","Please select a spreadsheet file")
        return
    
    dividend_analysis_df = pd.read_excel(spreadsheet_location, index_col=[0,1])

    if ticker in dividend_analysis_df.index:
        #enable show search button
        showvalue_btn['state'] = 'normal'
        
    else:
        messagebox.showerror("Error","Sorry the ticker you entered was not found within this spreadsheet")
        return

    #set up  csv file to be analysed in frame 2(fair value)
    #D0 = float(dividend_analysis_df.loc[(ticker, 2020), "Dividend"])
    #D0_slider.delete(0, END)
    #D0_slider.insert(0, float(D0))

    #median_growthrate = dividend_analysis_df.loc[(ticker, 2020), "Median growth rate"]
    #median_growthrate_slider.delete(0, END)
    #median_growthrate_slider.insert(0, float(median_growthrate))
    
    wacc = dividend_analysis_df.loc[(ticker, 2020), "WACC"]
    wacc_slider.delete(0, END)
    wacc_slider.insert(0, float(wacc))
    fair_value_display.delete(0, END)

    #set up wacc frame variables
    market_value_of_equity = dividend_analysis_df.loc[(ticker, 2020), "Market cap"]
    market_value_of_equity_slider.delete(0, END)
    market_value_of_equity_slider.insert(0, float(market_value_of_equity))

    market_value_of_debt = dividend_analysis_df.loc[(ticker, 2020), "Market value of debt"]
    market_value_of_debt_slider.delete(0, END)
    market_value_of_debt_slider.insert(0, float(market_value_of_debt))

    Cost_of_Equity = dividend_analysis_df.loc[(ticker, 2020), "Cost of equity"]
    cost_of_equity_slider.delete(0, END)
    cost_of_equity_slider.insert(0, float(Cost_of_Equity))

    Cost_of_Debt = dividend_analysis_df.loc[(ticker, 2020), "Cost of debt"]
    cost_of_debt_slider.delete(0, END)
    cost_of_debt_slider.insert(0, float(Cost_of_Debt))

    corporatetax = dividend_analysis_df.loc[(ticker, 2020), "Corporate tax rate"]
    corporate_tax_slider.delete(0, END)
    corporate_tax_slider.insert(0, float(corporatetax))

    wacc_display.delete(0, END)

def show():     #show calculation when search button is pressed
    if clicked.get() == "Correlation":
        get_correlation()
    elif clicked.get() == "Volatility":
        get_volatility()
    elif clicked.get() == "Returns":
        get_returns()
    elif clicked.get() == "Beta":
        get_Beta()
    elif clicked.get() == "Expected Returns(CAPM)":
        get_expected_returns()

#def get_correlation():
#    a = SGXstocks('test.csv')
#    correlation = a.correlation('SPY', 'BKW.SI')
#    output.delete(0, END)
#    output.insert(0, str(correlation))
#    output.pack()

def get_volatility():
    a = SGXstocks('sgx_dividend_stocks.csv')
    volatility = a.riskreturn(ticker)[2]
    output.delete(0, END)
    output.insert(0, str(volatility))
    output.pack()

def get_returns():
    a = SGXstocks('sgx_dividend_stocks.csv')
    returns = a.riskreturn(ticker)[1]/100
    output.delete(0, END)
    output.insert(0, str(returns))
    output.pack()

def get_Beta():
    a = SGXstocks('sgx_dividend_stocks.csv')
    beta = a.Beta(ticker)
    output.delete(0, END)
    output.insert(0, str(beta))
    output.pack()

def get_expected_returns():
    a = SGXstocks('sgx_dividend_stocks.csv')
    expected_returns = a.expected_return(ticker)
    output.delete(0, END)
    output.insert(0, str(expected_returns))
    output.pack()

def select_spreadsheet():
    global spreadsheet_location
    root.filename = filedialog.askopenfilename(initialdir='C:/Users/acer/Documents/Python_Scripts/Stonks/Dividend_analysis', title="Select a File", filetype=(('excel files',"*.xlsx"),('csv files', '*.csv')))
    spreadsheet_location = root.filename

#Create frame    
frame = LabelFrame(root, text="Search for ticker", padx=50, pady=50)
frame.pack(padx=10, pady=10)

#Select spreadsheet button
select_spreadsheet_btn = Button(frame, text="Select spreadsheet", command=select_spreadsheet)
select_spreadsheet_btn.pack()

# Label to ask for stock ticker
ticker_label = Label(frame, text="Please input stock ticker below:")
ticker_label.pack()

#input to get stock name
input_stockname = Entry(frame)
input_stockname.pack(pady=10)

# Button to search for ticker
search_btn = Button(frame, text="Search", command=search)  
search_btn.pack()

# Label to give instructions to user to select from dropdown menu
instructions_label = Label(frame, text="Select statistic from dropdown list below")
instructions_label.pack()

#dropdown menu to select function to be calculated
options = [ 
    "Volatility",
    "Returns", 
    "Beta",
    "Expected Returns(CAPM)",
    #"Correlation",
]

clicked = StringVar()
clicked.set(options[0])

drop = OptionMenu(frame, clicked, *options)     
drop.pack()

#button to show value
showvalue_btn = Button(frame, text="Show Value", command=show, state=DISABLED)  
showvalue_btn.pack(side=RIGHT)

# box to show value of function selected
output = Entry(frame)
output.pack(pady=10)

############################################################################################ END OF FIRST FRAME ################################################################################

############################################################################################ WACC frame ########################################################################################

def calculate_wacc():
    market_value_of_equity = float(market_value_of_equity_slider.get())
    market_value_of_debt = float(market_value_of_debt_slider.get())
    Cost_of_Equity = float(cost_of_equity_slider.get())
    Cost_of_Debt = float(cost_of_debt_slider.get())
    corporatetax = float(corporate_tax_slider.get())

    wacc = ((market_value_of_equity/(market_value_of_equity + market_value_of_debt))*Cost_of_Equity) + ((market_value_of_debt/(market_value_of_equity + market_value_of_debt))*Cost_of_Debt*(1-corporatetax))
    print(wacc)
    wacc_display.delete(0, END)
    wacc_display.insert(0, wacc)

wacc_frame = LabelFrame(root, text="WACC adjustor", padx=50, pady=50)
wacc_frame.pack(padx=10, pady=10, side=RIGHT)

market_value_of_equity_label = Label(wacc_frame, text='Market value of equity')
market_value_of_equity_label.pack()
market_value_of_equity_slider = Entry(wacc_frame)
market_value_of_equity_slider.pack()

market_value_of_debt_label = Label(wacc_frame, text='Market value of debt')
market_value_of_debt_label.pack()
market_value_of_debt_slider = Entry(wacc_frame)
market_value_of_debt_slider.pack()

Cost_of_Equity_label = Label(wacc_frame, text='Cost of Equity')
Cost_of_Equity_label.pack()
cost_of_equity_slider = Entry(wacc_frame)
cost_of_equity_slider.pack()

Cost_of_Debt_label = Label(wacc_frame, text='Cost of Debt')
Cost_of_Debt_label.pack()
cost_of_debt_slider = Entry(wacc_frame)
cost_of_debt_slider.pack()

corporatetax_label = Label(wacc_frame, text='Coporate tax rate')
corporatetax_label.pack()
corporate_tax_slider = Entry(wacc_frame)
corporate_tax_slider.pack()

calculate_wacc_btn = Button(wacc_frame, text="Calculate WACC", command=calculate_wacc)
calculate_wacc_btn.pack()

wacc_display = Entry(wacc_frame, text="WACC")
wacc_display.pack(pady=10)

############################################################################################ END of WACC FRAME #################################################################################

############################################################################################ Frame two #########################################################################################

def calculate():
    D0 = float(D0_slider.get())
    median_growthrate = float(median_growthrate_slider.get())
    wacc = float(wacc_slider.get())
    fair_value = (D0*(1 + median_growthrate))/(wacc - median_growthrate)
    print(fair_value)
    fair_value_display.delete(0, END)
    fair_value_display.insert(0, fair_value)

frame2 = LabelFrame(root, text="Fair value adjustor", padx=50, pady=50)
frame2.pack(padx=10, pady=10)

D0_label = Label(frame2, text='D0')
D0_label.pack()
D0_slider = Entry(frame2)
D0_slider.pack()

median_label = Label(frame2, text='Median Growth Rate')
median_label.pack()
median_growthrate_slider = Entry(frame2)
median_growthrate_slider.pack()

wacc_label = Label(frame2, text='WACC')
wacc_label.pack()
wacc_slider = Entry(frame2)
wacc_slider.pack()

calculate_fair_value_btn = Button(frame2, text="Calculate fair value", command=calculate)
calculate_fair_value_btn.pack()

fair_value_display = Entry(frame2, text="Fair value")
fair_value_display.pack(pady=10)

############################################################################################ END OF SECOND FRAME ###############################################################################


#button_exit = Button(root, text='EXIT PROGRAM', command=root.quit)
#button_exit.pack()

root.mainloop()