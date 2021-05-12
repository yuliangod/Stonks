from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import pandas as pd
from PIL import ImageTk, Image
import re
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

fcff_df = pd.read_excel('Dividend_analysis/sgx_FCFF_analysis.xlsx', index_col=[0,2])
sgx_df = pd.read_csv('myData.csv', index_col=[1])

class swipestonks:
    def __init__(self, master):
        self.master = master
        master.title("SwipeStonks")
        self.window_frame = Frame(master)
        self.window_frame.pack()
        
        #get last stock before app was closed
        with open('swipestonkscache.txt', 'r') as f1:
            lines = f1.read()
        self.idx = int(lines)
        self.stock = fcff_df.index.get_level_values("Ticker").drop_duplicates()[self.idx]

        #print image of stock price history on screen
        #img_regex = re.compile(r'(.*)\.SI')
        #mo = img_regex.search(self.stock)
        #self.img_name = mo.group(1) + "_SI"
        #self.img = ImageTk.PhotoImage(Image.open(f'Dividend_analysis/{self.img_name}.png'))
        #self.stock_img = Label(window_frame, image = self.img)
        #self.stock_img.grid(row=0, column=0, columnspan=2)

        #embed 1st matplotlib graph into tkinter
        self.figure = plt.Figure(figsize=(6,5), dpi=70)
        self.ax = self.figure.add_subplot(111)
        self.line_graph = FigureCanvasTkAgg(self.figure, self.window_frame)
        self.line_graph.get_tk_widget().grid(row=0, column=0)

        self.fcff_df = fcff_df.loc[self.stock,'Revenue']     #plot graph for Revenue
        self.fcff_df.plot(kind='line', legend=True, ax=self.ax)

        self.fcff_df = fcff_df.loc[self.stock,'Net Income']     #plot graph for net income
        self.fcff_df.plot(kind='line', legend=True, ax=self.ax)

        self.fcff_df = fcff_df.loc[self.stock,'FCFF']     #plot graph for FCFF
        self.fcff_df.plot(kind='line', legend=True, ax=self.ax)
        
        self.ax.set_title(self.stock)
        
        #embed 2nd matplotlib graph into tkinter
        self.figure2 = plt.Figure(figsize=(6,5), dpi=70)
        self.ax2 = self.figure2.add_subplot(111)
        self.line_graph2 = FigureCanvasTkAgg(self.figure2, self.window_frame)
        self.line_graph2.get_tk_widget().grid(row=0, column=1)

        self.fcff_df = fcff_df.loc[self.stock,'Expected Growth Rate']     #plot graph for expected growth rate
        self.fcff_df.plot(kind='line', legend=True, ax=self.ax2)

        self.fcff_df = fcff_df.loc[self.stock,'Revenue Growth Rate']     #plot graph for historical revenue growth rate
        self.fcff_df.plot(kind='line', legend=True, ax=self.ax2)

        self.fcff_df = fcff_df.loc[self.stock,'Net Income Growth Rate']     #plot graph for historical net income growth rate
        self.fcff_df.plot(kind='line', legend=True, ax=self.ax2)
        
        self.ax2.set_title(self.stock)

        self.stats_frame(self.stock, self.window_frame)

        #self.dividend_button = Button(window_frame, text="Show dividend trend", command=self.div_graph)   #plot graph of historical dividend growth
        #self.dividend_button.grid(row=3, column=0, sticky="E")

        #self.dividend = fcff_df.loc[self.stock, "Dividend"].to_string()     #extract historical dividends of stock
        #self.dividend_label = Label(text= f"Historical dividends: \n{self.dividend}", font='Helvetica 10')
        #self.dividend_label.grid(row=2, column=0, sticky="E")

        #self.dividend_growth_rate = fcff_df.loc[self.stock, "Dividend Growth Rate"].to_string()     #extract dividend growth rate of stock
        #self.dividend_growth_rate_label = Label(text= f"Dividend Growth Rate: \n{self.dividend_growth_rate}", font='Helvetica 10')
        #self.dividend_growth_rate_label.grid(row=2, column=1, sticky="W")

        #button to edit WACC
        self.edit_wacc_button = Button(self.window_frame, text="Edit WACC", command= lambda: self.editWACC(self.stock))
        self.edit_wacc_button.grid(row=2, column=0)

        #button to edit fair value
        self.edit_wacc_button = Button(self.window_frame, text="Edit fair value", command=lambda: self.editFairValue(self.stock))
        self.edit_wacc_button.grid(row=2, column=1)

        #button to get to next page
        self.next_button = Button(self.window_frame, text="Next", command=lambda: self.greet(self.idx + 1))    
        self.next_button.grid(row=4, column=1, pady=10, sticky="W")
        if (self.idx + 1) == len(fcff_df.index.get_level_values("Ticker").drop_duplicates()):
            self.next_button["state"] = DISABLED
            

        #button to get back to previous page
        self.back_button = Button(self.window_frame, text="Back", command=lambda: self.greet(self.idx - 1))    
        self.back_button.grid(row=4, column=0, pady=10, sticky="E")
        if (self.idx) == 0:
            self.back_button["state"] = DISABLED

        #button to like stock
        self.like_button = Button(self.window_frame, text="Like", command= self.like, relief="raised")
        self.like_button.grid(row=5, column=0, sticky="E")
        with open("watchlistcache.txt", "r") as f:
            lines = f.readlines()
        for line in lines:
            if self.stock in line.strip("\n"):
                self.like_button.config(relief="sunken")

        #button to view watchlist
        self.watchlist_button = Button(self.window_frame, text="Watchlist", command=self.see_watchlist)
        self.watchlist_button.grid(row=5, column=1, sticky="W")  

        #button to close program
        self.close_button = Button(self.window_frame, text="Close", command=master.quit)      
        self.close_button.grid(row=6, column=0, columnspan=2)

    #function to set up frame that displays relevant stats relating to stock
    def stats_frame(self,stock,frame,forget=False):
        self.statsframe = Frame(frame)
        self.statsframe.grid(row=1, column=0, columnspan=2)

        trading_code = stock.replace(".SI", "")
        self.trading_name = sgx_df.loc[trading_code, "Trading Name"]    #display name of stock
        self.trading_name_label = Label(self.statsframe, text= f"Name: \n{self.trading_name}", font='Helvetica 10')
        self.trading_name_label.grid(row=0, column=0)

        self.sector = sgx_df.loc[trading_code, "Sector"]    #display sector of stock
        self.sector_label = Label(self.statsframe, text= f"Sector: \n{self.sector}", font='Helvetica 10')
        self.sector_label.grid(row=0, column=1)

        self.wacc = fcff_df.loc[(stock, 2020), "WACC"]      #extract wacc of stock
        self.wacc_label = Label(self.statsframe, text= f"WACC: \n{self.wacc}", font='Helvetica 10')
        self.wacc_label.grid(row=1, column=0)

        self.fair_value = fcff_df.loc[(stock, 2020), "Fair value"]      #extract fair value of stock
        self.fair_value_label = Label(self.statsframe, text= f"Fair value: \n{self.fair_value}", font='Helvetica 10')
        self.fair_value_label.grid(row=1, column=1)

        self.percentage_undervalued = round(fcff_df.loc[(stock, 2020), "Percentage undervalued"],2)      #extract fair value of stock
        self.percentage_undervalued_label = Label(self.statsframe, text= f"Percentage undervalued: \n{self.percentage_undervalued}%", font='Helvetica 10')
        self.percentage_undervalued_label.grid(row=2, column=0)

    #function that refreshes app when next or back button is pressed
    def greet(self, idx):
        #reset window_frame frame
        self.window_frame.forget()
        self.window_frame = Frame(self.master)
        self.window_frame.pack()

        #get ticker of next stock in the list
        self.stock = fcff_df.index.get_level_values("Ticker").drop_duplicates()[idx]

        #toggle like button depending on whether current stock is in watchlist
        self.like_button = Button(self.window_frame, text="Like", command= self.like, relief="raised")
        self.like_button.grid(row=5, column=0, sticky="E")
        with open("watchlistcache.txt", "r") as watchlist:
            lines = watchlist.readlines()
        if str(self.stock + '\n') in lines:
            self.like_button.config(relief="sunken")
        else:
            self.like_button.config(relief="raised")

        #button to edit WACC
        self.edit_wacc_button = Button(self.window_frame, text="Edit WACC", command= lambda: self.editWACC(self.stock))
        self.edit_wacc_button.grid(row=2, column=0)

        #button to edit fair value
        self.edit_wacc_button = Button(self.window_frame, text="Edit fair value", command=lambda: self.editFairValue(self.stock))
        self.edit_wacc_button.grid(row=2, column=1)

        #button to view watchlist
        self.watchlist_button = Button(self.window_frame, text="Watchlist", command=self.see_watchlist)
        self.watchlist_button.grid(row=5, column=1, sticky="W")  

        #button to close program
        self.close_button = Button(self.window_frame, text="Close", command=self.master.quit)      
        self.close_button.grid(row=6, column=0, columnspan=2)

        #update next button
        self.next_button = Button(self.window_frame, text="Next", command=lambda: self.greet(idx + 1))
        self.next_button.grid(row=4, column=1, sticky="W")

        #disable next stock button at the last stock 
        if (idx + 1) == len(fcff_df.index.get_level_values("Ticker").drop_duplicates()):
            self.next_button["state"] = DISABLED

        #update back button
        self.back_button = Button(self.window_frame, text="Back", command=lambda: self.greet(idx - 1), state=NORMAL)    
        self.back_button.grid(row=4, column=0, sticky="E")
        if (idx) == 0:
            self.back_button["state"] = DISABLED

        #display next image
        #self.stock_img.grid_forget()
        #img_regex = re.compile(r'(.*)\.SI')
        #mo = img_regex.search(self.stock)
        #self.img_name = mo.group(1) + "_SI"
        #self.img = ImageTk.PhotoImage(Image.open(f'Dividend_analysis/{self.img_name}.png'))
        #self.stock_img = Label(self.window_frame, image = self.img)
        #self.stock_img.grid(row=0, column=0, columnspan=2)

        #plot next 1st graph
        self.figure = plt.Figure(figsize=(6,5), dpi=70)
        self.ax = self.figure.add_subplot(111)
        self.line_graph = FigureCanvasTkAgg(self.figure, self.window_frame)
        self.line_graph.get_tk_widget().grid(row=0, column=0)

        self.fcff_df = fcff_df.loc[self.stock,'Revenue']     #plot graph for Revenue
        self.fcff_df.plot(kind='line', legend=True, ax=self.ax)

        self.fcff_df = fcff_df.loc[self.stock,'Net Income']     #plot graph for Net income
        self.fcff_df.plot(kind='line', legend=True, ax=self.ax)

        self.fcff_df = fcff_df.loc[self.stock,'FCFF']     #plot graph for Net income
        self.fcff_df.plot(kind='line', legend=True, ax=self.ax)
        
        self.ax.set_title(self.stock)

        #embed 2nd matplotlib graph into tkinter
        self.figure2 = plt.Figure(figsize=(6,5), dpi=70)
        self.ax2 = self.figure2.add_subplot(111)
        self.line_graph2 = FigureCanvasTkAgg(self.figure2, self.window_frame)
        self.line_graph2.get_tk_widget().grid(row=0, column=1)

        self.fcff_df = fcff_df.loc[self.stock,'Expected Growth Rate']     #plot graph for expected growth rate
        self.fcff_df.plot(kind='line', legend=True, ax=self.ax2)

        self.fcff_df = fcff_df.loc[self.stock,'Revenue Growth Rate']     #plot graph for historical growth rate of revenue
        self.fcff_df.plot(kind='line', legend=True, ax=self.ax2)
        
        self.fcff_df = fcff_df.loc[self.stock,'Net Income Growth Rate']     #plot graph for historical growth rate of net income
        self.fcff_df.plot(kind='line', legend=True, ax=self.ax2)
        

        self.ax2.set_title(self.stock)

        #display next stats
        self.stats_frame(self.stock, self.window_frame, forget=True)

        #self.dividend_label.grid_forget()
        #self.dividend = fcff_df.loc[self.stock, "Dividend"].to_string()     #extract historical dividends of stock
        #self.dividend_label = Label(text= f"Historical dividends: \n{self.dividend}", font='Helvetica 10')
        #self.dividend_label.grid(row=2, column=0, sticky="E")
        #
        #self.dividend_growth_rate_label.grid_forget()
        #self.dividend_growth_rate = fcff_df.loc[self.stock, "Dividend Growth Rate"].to_string()     #extract dividend growth rate of stock
        #self.dividend_growth_rate_label = Label(text= f"Dividend Growth Rate: \n{self.dividend_growth_rate}", font='Helvetica 10')
        #self.dividend_growth_rate_label.grid(row=2, column=1, sticky="W")

        #store current index in txt file so that app will restart from current stock
        with open("swipestonkscache.txt", "w") as myfile:
            myfile.write(str(idx))

    #function for like button
    def like(self):     
        if self.like_button.config('relief')[-1] == 'sunken':
            self.like_button.config(relief="raised")
            print('Unlike')
            with open("watchlistcache.txt", "r") as f:
                lines = f.readlines()
            with open("watchlistcache.txt", "w") as f:
                for line in lines:
                    if line.strip("\n") != self.stock:
                        f.write(line)
        else:
            with open("watchlistcache.txt", "a") as myfile:
                myfile.write(f"{self.stock}\n")
            self.like_button.config(relief="sunken")

    # functions for edit wacc window
    def editWACC(self, stock):
        def calculate_wacc():
            market_value_of_equity = float(market_value_of_equity_slider.get())
            market_value_of_debt = float(market_value_of_debt_slider.get())
            Cost_of_Equity = float(cost_of_equity_slider.get())
            Cost_of_Debt = float(cost_of_debt_slider.get())
            corporatetax = float(corporate_tax_slider.get())

            wacc = ((market_value_of_equity/(market_value_of_equity + market_value_of_debt))*Cost_of_Equity) + ((market_value_of_debt/(market_value_of_equity + market_value_of_debt))  *Cost_of_Debt*    (1-corporatetax))
            wacc_display.delete(0, END)
            wacc_display.insert(0, wacc)

        editWACC_window = Toplevel(self.window_frame)
        editWACC_window.title("Edit WACC")
        editWACC_window.geometry("200x300")

        # set up labels for variables in wacc calculations
        market_value_of_equity_label = Label(editWACC_window, text='Market value of equity')
        market_value_of_equity_label.pack()
        market_value_of_equity_slider = Entry(editWACC_window)
        market_value_of_equity_slider.pack()

        market_value_of_debt_label = Label(editWACC_window, text='Market value of debt')
        market_value_of_debt_label.pack()
        market_value_of_debt_slider = Entry(editWACC_window)
        market_value_of_debt_slider.pack()

        Cost_of_Equity_label = Label(editWACC_window, text='Cost of Equity')
        Cost_of_Equity_label.pack()
        cost_of_equity_slider = Entry(editWACC_window)
        cost_of_equity_slider.pack()

        Cost_of_Debt_label = Label(editWACC_window, text='Cost of Debt')
        Cost_of_Debt_label.pack()
        cost_of_debt_slider = Entry(editWACC_window)
        cost_of_debt_slider.pack()

        corporatetax_label = Label(editWACC_window, text='Coporate tax rate')
        corporatetax_label.pack()
        corporate_tax_slider = Entry(editWACC_window)
        corporate_tax_slider.pack()

        calculate_wacc_btn = Button(editWACC_window, text="Calculate WACC", command=calculate_wacc)
        calculate_wacc_btn.pack()

        wacc_display = Entry(editWACC_window, text="WACC")
        wacc_display.pack(pady=10)

        # pull computed calculations from spreadsheet
        market_value_of_equity = fcff_df.loc[(self.stock, 2020), "Market cap"]
        market_value_of_equity_slider.delete(0, END)
        market_value_of_equity_slider.insert(0, float(market_value_of_equity))

        market_value_of_debt = fcff_df.loc[(self.stock, 2020), "Market value of debt"]
        market_value_of_debt_slider.delete(0, END)
        market_value_of_debt_slider.insert(0, float(market_value_of_debt))

        Cost_of_Equity = fcff_df.loc[(self.stock, 2020), "Cost of equity"]
        cost_of_equity_slider.delete(0, END)
        cost_of_equity_slider.insert(0, float(Cost_of_Equity))

        Cost_of_Debt = fcff_df.loc[(self.stock, 2020), "Cost of debt"]
        cost_of_debt_slider.delete(0, END)
        cost_of_debt_slider.insert(0, float(Cost_of_Debt))

        corporatetax = fcff_df.loc[(self.stock, 2020), "Corporate tax rate"]
        corporate_tax_slider.delete(0, END)
        corporate_tax_slider.insert(0, float(corporatetax))

        wacc = fcff_df.loc[(self.stock, 2020), "WACC"]
        wacc_display.delete(0, END)
        wacc_display.insert(0, wacc)

    # functions for edit fair value window
    def editFairValue(self, stock):
        def calculate_fairValue():
            
            FCFF = float(FCFF_slider.get())
            expected_growth_rate = float(expected_growth_rate_slider.get())
            WACC = float(WACC_slider.get())
            terminal_value = float(terminal_value_slider.get())
            shares_out = float(shares_out_slider.get())


            projected_FCFF = terminal_value
            for i in range(1,5):
              FCFF_t = (FCFF*(1 + expected_growth_rate)**i)/((1+WACC)**i)
              projected_FCFF += FCFF_t

            fair_value = projected_FCFF/shares_out

            fairValue_display.delete(0, END)
            fairValue_display.insert(0, fair_value)

        editFairValue_window = Toplevel(self.window_frame)
        editFairValue_window.title("Edit fair value")
        editFairValue_window.geometry("200x300")

        # set up labels for variables in wacc calculations
        FCFF_label = Label(editFairValue_window, text='FCFF')
        FCFF_label.pack()
        FCFF_slider = Entry(editFairValue_window)
        FCFF_slider.pack()

        expected_growth_rate_label = Label(editFairValue_window, text='Expected Growth Rate')
        expected_growth_rate_label.pack()
        expected_growth_rate_slider = Entry(editFairValue_window)
        expected_growth_rate_slider.pack()

        WACC_label = Label(editFairValue_window, text='WACC')
        WACC_label.pack()
        WACC_slider = Entry(editFairValue_window)
        WACC_slider.pack()

        terminal_value_label = Label(editFairValue_window, text='Terminal value')
        terminal_value_label.pack()
        terminal_value_slider = Entry(editFairValue_window)
        terminal_value_slider.pack()

        shares_out_label = Label(editFairValue_window, text='Shares outstanding')
        shares_out_label.pack()
        shares_out_slider = Entry(editFairValue_window)
        shares_out_slider.pack()

        calculate_fairValue_btn = Button(editFairValue_window, text="Calculate fair value", command=calculate_fairValue)
        calculate_fairValue_btn.pack()

        fairValue_display = Entry(editFairValue_window, text="Fair value")
        fairValue_display.pack(pady=10)
        
        # pull computed calculations from spreadsheet
        FCFF = fcff_df.loc[(stock, 2020), "FCFF"]
        FCFF_slider.delete(0, END)
        FCFF_slider.insert(0, float(FCFF))

        expected_growth_rate = fcff_df.loc[(stock, 2020), "Expected Growth Rate"]
        expected_growth_rate_slider.delete(0, END)
        expected_growth_rate_slider.insert(0, float(expected_growth_rate))

        WACC = fcff_df.loc[(stock, 2020), "WACC"]
        WACC_slider.delete(0, END)
        WACC_slider.insert(0, float(WACC))

        terminal_value = fcff_df.loc[(stock, 2020), "Terminal value"]
        terminal_value_slider.delete(0, END)
        terminal_value_slider.insert(0, float(terminal_value))

        shares_out = fcff_df.loc[(stock, 2020), "Shares outstanding"]
        shares_out_slider.delete(0, END)
        shares_out_slider.insert(0, float(shares_out))

        fairValue = fcff_df.loc[(stock, 2020), "Fair value"]
        fairValue_display.delete(0, END)
        fairValue_display.insert(0, fairValue)
    
    # function to see stocks in watchlist
    def see_watchlist(self):
        #function to open new window to view stock in watchlist
        def view_watchlist_stock(stock):
            print(stock)
            watchlist_stock_window = Toplevel(see_watchlist_window)
            watchlist_stock_window.title("Watchlist stock")

            #plot next 1st graph
            self.figure = plt.Figure(figsize=(6,5), dpi=70)
            self.ax = self.figure.add_subplot(111)
            self.line_graph = FigureCanvasTkAgg(self.figure, watchlist_stock_window)
            self.line_graph.get_tk_widget().grid(row=0, column=0)

            self.fcff_df = fcff_df.loc[stock,'Revenue']     #plot graph for Revenue
            self.fcff_df.plot(kind='line', legend=True, ax=self.ax)

            self.fcff_df = fcff_df.loc[stock,'Net Income']     #plot graph for Net income
            self.fcff_df.plot(kind='line', legend=True, ax=self.ax)

            self.fcff_df = fcff_df.loc[stock,'FCFF']     #plot graph for FCFF
            self.fcff_df.plot(kind='line', legend=True, ax=self.ax)

            self.ax.set_title(stock)

            #embed 2nd matplotlib graph into tkinter
            self.figure2 = plt.Figure(figsize=(6,5), dpi=70)
            self.ax2 = self.figure2.add_subplot(111)
            self.line_graph2 = FigureCanvasTkAgg(self.figure2, watchlist_stock_window)
            self.line_graph2.get_tk_widget().grid(row=0, column=1)

            self.fcff_df = fcff_df.loc[stock,'Expected Growth Rate']     #plot graph for expected growth rate
            self.fcff_df.plot(kind='line', legend=True, ax=self.ax2)

            self.fcff_df = fcff_df.loc[stock,'Revenue Growth Rate']     #plot graph for historical growth rate of revenue
            self.fcff_df.plot(kind='line', legend=True, ax=self.ax2)

            self.fcff_df = fcff_df.loc[stock,'Net Income Growth Rate']     #plot graph for historical growth rate of net income
            self.fcff_df.plot(kind='line', legend=True, ax=self.ax2)


            self.ax2.set_title(stock)

            #display next stats
            self.stats_frame(stock, watchlist_stock_window)

            #button to edit WACC
            edit_wacc_button = Button(watchlist_stock_window, text="Edit WACC", command=lambda: self.editWACC(stock))
            edit_wacc_button.grid(row=2, column=0)

            #button to edit fair value
            edit_wacc_button = Button(watchlist_stock_window, text="Edit fair value", command=lambda: self.editFairValue(stock))
            edit_wacc_button.grid(row=2, column=1)

            #button to like stock
            self.watchlist_like_button = Button(watchlist_stock_window, text="Like", command= lambda:watchlist_like(stock), relief="raised")
            self.watchlist_like_button.grid(row=2, column=0, sticky="E")

            #toggle like button depending on whether current stock is in watchlist
            with open("watchlistcache.txt", "r") as watchlist:
                lines = watchlist.readlines()
            if str(stock + '\n') in lines:
                self.watchlist_like_button.config(relief="sunken")
            else:
                self.watchlist_like_button.config(relief="raised")

        # function to delete unwanted stocks in watchlist
        def delete_watchlist_stock(stock):
            print(f'Removing {stock} from watchlist')
            with open("watchlistcache.txt", "r") as f:
                lines = f.readlines()
            with open("watchlistcache.txt", "w") as f:
                for line in lines:
                    if line.strip("\n") != stock:
                        f.write(line)
            
            idx = Lines.index(stock+'\n')
            labels[idx].destroy()
            view_buttons[idx].destroy()
            delete_buttons[idx].destroy()

            if len(lines) == 1:
                Label(second_frame, text='Watchlist is currently empty', font='Helvetica 10').grid(column=0)

        def search():
            search_ticker = search_entry.get()
            if search_ticker in fcff_df.index:
                view_watchlist_stock(search_ticker)
        
            else:
                messagebox.showerror("Error","Sorry the ticker you entered was not found within this spreadsheet")
                return

        def watchlist_like(stock):
            if self.watchlist_like_button.config('relief')[-1] == 'sunken':
                self.watchlist_like_button.config(relief="raised")
                print('Unlike')
                with open("watchlistcache.txt", "r") as f:
                    lines = f.readlines()
                with open("watchlistcache.txt", "w") as f:
                    for line in lines:
                        if line.strip("\n") != self.stock:
                            f.write(line)
                # restart watchlist window with stock now removed
                see_watchlist_window.destroy()
                self.see_watchlist()
            else:
                with open("watchlistcache.txt", "a") as myfile:
                    myfile.write(f"{stock}\n")
                self.watchlist_like_button.config(relief="sunken")
                # restart watchlist window with stock now added to watchlist
                see_watchlist_window.destroy()
                self.see_watchlist()

        see_watchlist_window = Toplevel(self.window_frame)
        see_watchlist_window.title("Watchlist")
        see_watchlist_window.geometry("400x500")

        #create search bar
        search_frame = Frame(see_watchlist_window)
        search_frame.pack()
        search_entry = Entry(search_frame)
        search_entry.pack(side=LEFT)
        search_button = Button(search_frame, text='Search', command=search)
        search_button.pack(side=LEFT)

        #### scroll button ###
        # Create A Main Frame

        main_frame = Frame(see_watchlist_window)
        main_frame.pack(fill=BOTH, expand=1)

        # Create A Canvas
        my_canvas = Canvas(main_frame)
        my_canvas.pack(side=LEFT, fill=BOTH, expand=1)

        # Add A Scrollbar To The Canvas
        my_scrollbar = ttk.Scrollbar(main_frame, orient=VERTICAL, command=my_canvas.yview)
        my_scrollbar.pack(side=RIGHT, fill=Y)

        # Configure The Canvas
        my_canvas.configure(yscrollcommand=my_scrollbar.set)
        my_canvas.bind('<Configure>', lambda e: my_canvas.configure(scrollregion=my_canvas.bbox("all")))

        def _on_mouse_wheel(event):
            my_canvas.yview_scroll(-1 * int((event.delta / 120)), "units")

        my_canvas.bind_all("<MouseWheel>", _on_mouse_wheel)

        # Create ANOTHER Frame INSIDE the Canvas
        second_frame = Frame(my_canvas)

        # Add that New frame To a Window In The Canvas
        my_canvas.create_window((0,0), window=second_frame, anchor="nw")

        ### end of scroll bar ###

        #get list of stocks in watchlist
        file1 = open('watchlistcache.txt', 'r')
        Lines = file1.readlines()

        if len(Lines) == 0:
            Label(second_frame, text='Watchlist is currently empty', font='Helvetica 10').grid(column=0)

        labels = []     #create empty lists to reference which ones to delete later on
        view_buttons = []
        delete_buttons = []
        for i in range(len(Lines)):
            watchlist_stock_label = Label(second_frame, text=Lines[i], font='Helvetica 10')
            watchlist_stock_label.grid(row=i, column=0)
            watchlist_stock_button = Button(second_frame, text='View', command=lambda i=i: view_watchlist_stock(Lines[i].strip()))
            watchlist_stock_button.grid(row=i, column=1)
            delete_watchlist_stock_button = Button(second_frame, text='Remove', command=lambda i=i:delete_watchlist_stock(Lines[i].strip()))
            delete_watchlist_stock_button.grid(row=i, column=2)

            labels.append(watchlist_stock_label)
            view_buttons.append(watchlist_stock_button)
            delete_buttons.append(delete_watchlist_stock_button)           

    #def div_graph(self):      #button to show dividend trend
    #    plt.plot(fcff_df.loc[self.stock].index, fcff_df.loc[self.stock, "Dividend"])
    #    #plt.xticks(fcff_df.loc[self.stock].index)
    #    plt.xlabel("Year")
    #    plt.ylabel("Dividend payout")
    #    plt.title("Dividends")
    #    plt.show()

root = Tk()
my_gui = swipestonks(root)
root.mainloop()