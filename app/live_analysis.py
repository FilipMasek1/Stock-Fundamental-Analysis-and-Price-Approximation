import os
from pathlib import Path
os.chdir(Path(__file__).resolve().parent)

import yfinance as yf
import pandas as pd
import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
import dataframe_image as dfi



def Real_Analyza(tickers: list[str], interval1: str, period1: str, metrics: list[str]) -> dict[str, tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, list[str]]]:
    """
    In the first faze the function downloads data using yfinance and creates table with highlighted values of metrics based on set tresholds.
    In the second faze the function the data to calculate a 3rd degree polynomial fit. 
    If there is a problem with analysis, the function raises according error.

    Arguments:
        List of stock tickers to analyze.
        Interval - between downloaded dates.
        Period - historical
        List of financial metrics to evaluate.

    Result:
        Tuple containing a dictionary of fitted data for plots.
    """
    #Vygenerováno AI
    OK_values = dict(
        returnOnEquity=0.15,      # ROE > 15 %
        grossMargins=0.40,        # Hrubá marže > 40 %
        operatingMargins=0.15,    # Provozní marže > 15 %
        profitMargins=0.10,       # Čistá marže > 10 %
        debtToEquity=1.5,         # Zadlužení / Vlastní kapitál < 1.5 (nebo < 150 %)
        currentRatio=1.5,         # Běžná liquidita > 1.5
        freeCashflow=0.00001,           # Pozitivní FCF (> 0)
        trailingPE=25,            # P/E (minulé) < 25
        forwardPE=20              # Forward P/E < 20
    )


    OK=dict()
    tab=dict()
    tab["Stock"]=tickers
    quant=[]
    OK_metrics=list()
    invalid_tickers=[]
    for metric in metrics:
        for ticker in tickers:
            try:
                value=yf.Ticker(ticker).info.get(metric)
            except Exception:
                raise Exception("Analysis is not possible due to an error in the yfinance library. Please check your internet connection and try again. \n You can also relaunch the app for offline analysis.")
            if value==None:
                if ticker not in invalid_tickers:
                    invalid_tickers.append(ticker)
            else:
                quant.append(value)
        tab[metric]=quant
        quant=[]
    if len(invalid_tickers)!=0:
        invalid_str=", ".join(invalid_tickers)
        raise Exception(f"Ticker/s {invalid_str} do not exist")
    

    for i in range(len(tickers)):
        for metric in metrics:
            if tab[metric][i]==None:
                continue
            if (metric in ["returnOnEquity","grossMargins","operatingMargins","profitMargins","currentRatio","freeCashflow"]) and (tab[metric][i]>=OK_values[metric]):
                OK_metrics.append(metric)
            elif (metric in ["debtToEquity","trailingPE","forwardPE"]) and (tab[metric][i]<=OK_values[metric]):
                OK_metrics.append(metric)
        OK[tickers[i]]=OK_metrics
        OK_metrics=[]


    def style_rate(row: pd.Series) -> list[str]:
        """Applies green or red styling to table cells based on metric threshold evaluation."""
        color=[None]
        for metric in metrics:
            if metric in OK[row["Stock"]]: 
                color.append("color: green;")
            else:
                color.append("color: red;")
        return color


    df = pd.DataFrame(tab)
    df_styled=df.style.apply(style_rate,1)
    dfi.export(df_styled, "tabulka.png")

    #Aproximace cen akcií křivkou
    stocks=dict()
    stocks_date=dict()
    try:
        data = yf.download(tickers, period=period1, interval=interval1, progress=False)
    except Exception:
        raise Exception(f"An unexpected error occurred for ticker {ticker}. \n Try selecting a different value for the period or remove the ticker.")
    for ticker in tickers:
        dates = data.index.strftime('%Y-%m-%d').tolist()
        try:
            ceny = data['Close'][ticker].dropna().values.flatten().tolist() 
        except Exception: 
            ceny = data['Close'].dropna().values.flatten().tolist()
        stocks[ticker] = ceny
        stocks_date[ticker] = dates

    def fce(x: float, a: float, b: float, c: float, d: float) -> float:
        """
        3rd degree polynomial function definition
     
        Arguments:
            x - float
            a, b, c, d - calculated values (floats)
        Returns:
            calculated value (float)
        """
        return a*x**3+b*x**2+c*x+d

    tick_fit=dict()
    for ticker in tickers:
        y_data = stocks[ticker]
        x_data = np.arange(1, len(y_data) + 1)
        try: 
            p0 = np.polyfit(x_data, y_data, deg=3)
        except Exception:
            raise Exception(f"An unexpected error occurred for ticker {ticker}. \n Try selecting a different value for the period or remove the ticker.")
        fit, _ = sp.optimize.curve_fit(fce, x_data, y_data, p0)
        a_fit, b_fit, c_fit, d_fit = fit
        x_fit = np.linspace(x_data.min(), x_data.max(), 100)
        y_fit = fce(x_fit, a_fit, b_fit, c_fit, d_fit)
        tick_fit[ticker]= (x_data, y_data, x_fit, y_fit, stocks_date[ticker])
    return tick_fit 



def Download_data(tickers: list[str]) -> None:
    """
    Downloads historical price data and metrics for tickers, saving them locally for offline use.

    Arguments:
        List of tickers to save
    """

    
    metrics = ["returnOnEquity","grossMargins","operatingMargins","profitMargins","debtToEquity","currentRatio","freeCashflow","trailingPE","forwardPE"]
    for ticker in tickers:
        exists = False
        new_file = str(ticker)+".csv"
        for file in Path("./mock_data/history/").iterdir():
            if file.name == new_file:
                exists = True
        if exists == False:           
            data = yf.download(ticker, period="1y", interval="1d")
            data.to_csv(f"./mock_data/history/{new_file}")
            metrics_text = str(ticker)
            for metric in metrics:
                metrics_text += "," + str(yf.Ticker(ticker).info.get(metric))
            with open("./mock_data/akcie_metriky.csv", "a") as slozka:
                slozka.write(metrics_text + "\n")
