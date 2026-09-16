import os
from pathlib import Path
os.chdir(Path(__file__).resolve().parent)

import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from matplotlib.pylab import size
import matplotlib.pyplot as plt
import live_analysis
import mock_analysis
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.ticker as ticker_locator
import mock_analysis
import sys

class RAWindow():
    """ Main window for online analysis (RA = Real Analysis). """
    
    def __init__(self) -> None:
        """Initializes Tkinter widgets for ticker, period, interval, and metric selection."""
        
        self.screen = tk.Tk()
        self.screen.title("Nastavení analýzy")
        self.screen_width=800
        self.screen.geometry(f"{self.screen_width}x600+550+150")
        self.tickers = tk.Entry(self.screen, width=50)
        self.Metrics = ["returnOnEquity","grossMargins","operatingMargins","profitMargins","debtToEquity","currentRatio","freeCashflow","trailingPE","forwardPE"]
        self.select_period = tk.StringVar()
        self.select_interval = tk.StringVar()
        self.download_data = tk.BooleanVar(value=False)


    def metrics_selection(self, m: str) -> bool:
        """
        Adds or removes a selected metric from the active metrics list.
        Argumetns:
            m - metric that has been selected
        """
        
        if m in self.Metrics:
            self.Metrics.remove(m)
        else:
            self.Metrics.append(m)
        return True


    def MainWindow(self) -> None:
        """Builds and displays the main configuration GUI elements."""
        
        tickers_label = tk.Label(self.screen, text="Input Tickers:")
        tickers_label.place(relx=0.1, rely=0.1, anchor="w")
        self.tickers.place(relx=0.5, rely=0.1, anchor="center")

        period_label = tk.Label(self.screen, text="Select Period:")
        interval_label = tk.Label(self.screen, text="Select Interval:")
        period_label.place(relx=0.1, rely=0.2, anchor="w")
        interval_label.place(relx=0.1, rely=0.25, anchor="w")

        periods = ("1d", "2d", "5d", "1mo", "3mo", "6mo", "1y", "2y", "5y", "10y", "max")
        
        self.intervals_dict = {
            "1d": ["1m", "2m", "5m", "15m", "30m", "60m", "90m"],
            "2d": ["1m", "2m", "5m", "15m", "30m", "60m", "90m"],
            "5d": ["1m", "2m", "5m", "15m", "30m", "60m", "90m", "1d"],
            "1mo": ["2m", "5m", "15m", "30m", "60m", "90m", "1d", "5d", "1wk"],
            "3mo": ["60m", "1d", "5d", "1wk", "1mo"],
            "6mo": ["60m", "1d", "5d", "1wk", "1mo"],
            "1y": ["60m", "1d", "5d", "1wk", "1mo"],
            "2y": ["60m", "1d", "5d", "1wk", "1mo"],
            "5y": ["1d", "5d", "1wk", "1mo", "3mo"],
            "10y": ["1d", "5d", "1wk", "1mo", "3mo"],
            "max": ["1d", "5d", "1wk", "1mo", "3mo"],
        }

        self.interval_frame = tk.Frame(self.screen)
        self.interval_frame.place(relx=0.21, rely=0.27, width = self.screen_width, height=50, anchor="w")

        x = 1
        for period in periods:
            r = ttk.Radiobutton(self.screen, text=period, value=period, variable=self.select_period,command=self.update_intervals_ui)
            r.place(relx=(0.15+x*0.06), rely=0.2, anchor="w")
            x += 1

        self.update_intervals_ui()

        Metrics_label = tk.Label(self.screen, text="Select Metrics:")
        Metrics_label.place(relx=0.1, rely=0.4, anchor="w")
        metrics = ["returnOnEquity", "grossMargins", "operatingMargins", "profitMargins", "debtToEquity", "currentRatio", "freeCashflow", "trailingPE", "forwardPE"]
        vars_list = []
        x = 0
        y = 0

        for i in range(len(metrics)):
            if x < len(metrics) / 3:
                x = x + 1
            else:
                x = 1
                y += 1

            var = tk.BooleanVar(value=True)
            vars_list.append(var)
            ttk.Checkbutton(self.screen, variable=var, text=metrics[i], command=lambda m=metrics[i]: self.metrics_selection(m)).place(relx=0.06 + 0.2 * x, rely=0.4 + y * 0.05, anchor="w")

        ttk.Checkbutton(self.screen, variable=self.download_data, text="Do you want to download data for selected tickers?").place(relx=0.5, rely=0.7, anchor="center")
        
        if sys.platform == "darwin":
            analyze_button = tk.Label(self.screen, text="Analyze", bg="green", fg="white", width=20, height=2)
            analyze_button.bind("<Button-1>", lambda event: self.Analyze())
        else:
            analyze_button = tk.Button(self.screen, text="Analyze",command=self.Analyze, width=20, height=2, bg="green", fg="white")

        analyze_button.place(relx=0.5, rely=0.8, anchor="center")

        self.screen.mainloop()

    def update_intervals_ui(self) -> None:
        """Updates available interval radio buttons according to selected period."""
        
        if self.select_period.get() in self.intervals_dict:
            for widget in self.interval_frame.winfo_children():
                widget.destroy()

            current_period = self.select_period.get()
            available_intervals = self.intervals_dict[current_period]
            for i in range(len(available_intervals)):
                r = ttk.Radiobutton(self.interval_frame, text=available_intervals[i], value=available_intervals[i], variable=self.select_interval)
                r.place(relx=(i*0.06), rely=0.25, anchor="w")
            self.select_interval.set("")

    def Analyze(self) -> None:
        """Collects inputs and opens the analysis results window."""
        
        tickers1 = self.tickers.get()
        tickers1 = tickers1.split(",")
        tickers=[]
        for t in tickers1:
            tickers.append(t.strip())
        if "" in tickers:
            tickers.remove("")

        interval = self.select_interval.get()
        period = self.select_period.get()
        metrics = self.Metrics
        if len(tickers) > 6:
            ErrorWindow(self.screen, "You entered too many tickers. The maximum ammount of tickers is 6.")
            return
        if len(metrics)==0:
            ErrorWindow(self.screen, "No metrics selected.")
            return
        if len(tickers)==0:
            ErrorWindow(self.screen, "No tickers entered.")
            return
        if not period:
            ErrorWindow(self.screen, "No period selected.")
            return
        if not interval:
            ErrorWindow(self.screen, "No interval selected.")
            return

        print("Tickers:", tickers)
        print("Interval:", interval)
        print("Period:", period)
        print("Metrics:", metrics)
        AnalysisWindow(tickers, interval, period, metrics, self.screen, self.download_data.get())
        return None






class MAWindow():
    """Window for offline analysis using downloaded datasets (MA = Mock Analysis)."""
    def __init__(self) -> None:
            """Initialize GUI widgets for offline data configuration."""
            self.screen = tk.Tk()
            self.screen.title("Analysis configuration")
            self.screen_width=800
            self.screen.geometry(f"{self.screen_width}x600+550+150")
            self.tickers = tk.Entry(self.screen, width=50)
            self.Metrics = ["returnOnEquity","grossMargins","operatingMargins","profitMargins","debtToEquity","currentRatio","freeCashflow","trailingPE","forwardPE"]
            self.select_period = tk.StringVar()
            self.select_interval = tk.StringVar()

    def metrics_selection(self, m: str) -> bool:
        """
        Adds or removes a selected metric from the active metrics list.
        Argumetns:
            m - metric that has been selected
        """
        
        if m in self.Metrics:
            self.Metrics.remove(m)
        else:
            self.Metrics.append(m)
        return True
    
    def MainWindow(self) -> None:
        """Builds and displays the main configuration GUI elements."""
        
        mock_label = tk.Label(self.screen, text = "Analysis is not possible due to an error in the yfinance library. You can analyze old downloaded data.")
        mock_label.place(relx=0.5, rely = 0.05, anchor = "center")
        tickers_label = tk.Label(self.screen, text="Input Tickers:")
        tickers_label.place(relx=0.1, rely=0.1, anchor="w")
        self.tickers.place(relx=0.5, rely=0.1, anchor="center")
        av_data_label = tk.Label(self.screen, text = "Downloaded tickers:")
        av_data_label.place(relx=0.1, rely=0.15, anchor="w")


        av_mock_data = str()
        for file in Path("./mock_data/history/").iterdir():
            av_mock_data += str(file.name) + ","
        av_data = tk.Label(self.screen, text = av_mock_data)
        av_data.place(relx=0.30, rely = 0.15, anchor = "w")


        Metrics_label = tk.Label(self.screen, text="Select Metrics:")
        Metrics_label.place(relx=0.1, rely=0.4, anchor="w")
        metrics = ["returnOnEquity", "grossMargins", "operatingMargins", "profitMargins", "debtToEquity", "currentRatio", "freeCashflow", "trailingPE", "forwardPE"]
        vars_list = []
        x = 0
        y = 0

        for i in range(len(metrics)):
            if x < len(metrics) / 3:
                x = x + 1
            else:
                x = 1
                y += 1
            var = tk.BooleanVar(value=True)
            vars_list.append(var)
            ttk.Checkbutton(self.screen, variable=var, text=metrics[i], command=lambda m=metrics[i]: self.metrics_selection(m)).place(relx=0.06 + 0.2 * x, rely=0.4 + y * 0.05, anchor="w")

        if sys.platform == "darwin":
            analyze_button = tk.Label(self.screen, text="Analyze", bg="green", fg="white", width=20, height=2)
            analyze_button.bind("<Button-1>", lambda event: self.Analyze())
        else:
            analyze_button = tk.Button(self.screen, text="Analyze",command=self.Analyze, width=20, height=2, bg="green", fg="white")

        analyze_button.place(relx=0.5, rely=0.8, anchor="center")

        self.screen.mainloop()

    def Analyze(self) -> None:
        """Trigger offline analysis on requested tickers."""
        
        tickers1 = self.tickers.get()
        tickers1 = tickers1.split(",")
        tickers=[]
        for t in tickers1:
            tickers.append(t.strip())
        if "" in tickers:
            tickers.remove("")

        metrics = self.Metrics
        if len(tickers) > 6:
            ErrorWindow(self.screen, "You entered too many tickers. The maximum ammount of tickers is 6.")
            return
        if len(metrics)==0:
            ErrorWindow(self.screen, "No metrics selected")
            return
        if len(tickers)==0:
            ErrorWindow(self.screen, "No tickers entered.")
            return
        print("Tickers:", tickers)
        print("Metrics:", metrics)
        AnalysisWindow(tickers, interval="1d", period="1y", metrics=metrics, parent=self.screen, dwn_data=False)
        return None

    

class ErrorWindow():
    """Pop-up window displaying error message."""
    
    def __init__(self, parent: tk.Tk, message: str) -> None:
        """
        Shows a window with an error message.

        Argumetns:
            Parent - Parent Tkinter window.
            Message - Error text to display.
        """
        
        self.errorscreen = tk.Toplevel(parent)
        self.errorscreen.title("Error")
        self.errorscreen.geometry("400x300+750+250")
        msg=tk.Label(self.errorscreen, text=message)
        msg.place(relx=0.5, rely=0.5, anchor="center")
        return None





class AnalysisWindow():
    """Display window presenting metric summary table and stock price plots."""

    def __init__(self, tickers: list[str], interval: str, period: str, metrics: list[str], parent: tk.Tk, dwn_data: bool) -> None:
        """
        Runs analysis and construct results view window.

        tickers - ticker symbols list.
        interval - data interval string.
        period - data period string.
        metrics - requested metrics.
        parent - parent Tk widget.
        dwn_data - boolean value indicating whether to download data locally.
        """
        
        self.tickers = tickers
        self.interval = interval
        self.period = period
        self.metrics = metrics

        try:
            self.data = live_analysis.Real_Analyza(self.tickers, self.interval, self.period, self.metrics)
        except Exception as e:
            if "Analysis is not possible due to an error in the yfinance library. Please check your internet connection and try again." in str(e):
                try:
                    self.data, tickers = mock_analysis.Mock_Analyza(self.tickers, self.metrics)

                except Exception as e2:
                    ErrorWindow(parent, str(e2))
                    return
            else:
                ErrorWindow(parent, str(e))
                return

        if dwn_data == True:
            live_analysis.Download_data(tickers)
        
        self.newscreen = tk.Toplevel(parent)
        self.newscreen.title("Analysis results")
        self.newscreen.geometry("800x600+600+200")
        self.screen_width = 800
        self.current_canvas = None

        img = Image.open("tabulka.png")
        new_size = (int(img.width/1.3), int(img.height/1.3))
        img_resized = img.resize(new_size)
        self.tabulka_img = ImageTk.PhotoImage(img_resized)
        tabulka = tk.Label(self.newscreen, image=self.tabulka_img)
        tabulka.place(relx=0.01, rely=0.01, anchor="nw")

        opt = tk.StringVar(value=tickers[0])
        option_menu = tk.OptionMenu(self.newscreen, opt, *tickers)
        option_menu.place(relx=0.05, rely=0.33, anchor="center")
        zobrazit = tk.Button(self.newscreen, text="Show graph", command=lambda: self.graph(opt.get()))
        zobrazit.place(relx=0.15, rely=0.33, anchor="center")

        self.graph(tickers[0])

    def graph(self, ticker: str) -> None:
        """
        Plots stock prices alongside fitted polynomial approximation curves inside Tkinter window.

        Argumetns:
        ticker - selected ticker to plot.
        """
        
        if self.current_canvas is not None:
            self.current_canvas.get_tk_widget().destroy()
            self.current_canvas = None

        if ticker not in self.data:
            return

        x_data = self.data[ticker][0]
        y_data = self.data[ticker][1]
        x_fit = self.data[ticker][2]
        y_fit = self.data[ticker][3]
        dates = self.data[ticker][4]


        fig, ax = plt.subplots(figsize=(7, 4), dpi=90)
        ax.scatter(x_data, y_data, color='red', s=15, label="Actual Price")
        ax.plot(x_fit, y_fit, color='blue', linewidth=2, label="Polynomial Fit")
        ticks_loc = list(range(len(dates)))
        ax.set_xticks(ticks_loc)
        ax.set_xticklabels(dates)
        ax.xaxis.set_major_locator(ticker_locator.MaxNLocator(nbins=7))
        plt.setp(ax.get_xticklabels(), rotation=30, ha='right')
        ax.set_title(f"Price Approximation for Ticker: {ticker}")
        ax.set_xlabel("Date")
        ax.set_ylabel("Price")
        ax.legend()
        ax.grid(True, linestyle='--', alpha=0.6)
        fig.tight_layout()

        self.current_canvas = FigureCanvasTkAgg(fig, self.newscreen)
        self.current_canvas.draw()
        self.current_canvas.get_tk_widget().place(relx=0.5, rely=0.38, anchor="n")

        plt.close(fig)






