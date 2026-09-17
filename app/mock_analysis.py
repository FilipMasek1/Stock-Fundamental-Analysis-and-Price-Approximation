import os
import yfinance as yf
import pandas as pd
from pathlib import Path
os.chdir(Path(__file__).resolve().parent)
import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
import dataframe_image as dfi


def Mock_Analyza(tickers: list["str"], metrics: list["str"]) -> tuple[dict[str, tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, list[str]]], list[str]]:
    """
    In the first faze the function collects saved data from mock_data/akcie_metriky.csv and creates table with highlighted values of metrics based on set treshold.
    In the second faze the function collects data from mock_data/history/ and calculates a 3rd degree polynomial fit. 
    If there is a ticker for which there are no values saved, it raises exception.

    Arguments:
        tickers - list of stock tickers to analyze.
        metrics - list of financial metrics to evaluate.

    Result:
        Tuple containing a dictionary of fit data for plots and a list of available tickers.
    """

    """First faze"""
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


    if len(metrics)==0:
        raise Exception("No metrics")
    if len(tickers)==0:
        raise Exception("No tickers")

    OK=dict()
    tab=dict()
    availible_tickers=[]
    mock_data = pd.read_csv("mock_data/akcie_metriky.csv") 
    for ticker in tickers:
        for t in mock_data.values:
            if t[0] in tickers:
                if t[0] not in availible_tickers:
                    availible_tickers.append(t[0])
                    
    for ticker in availible_tickers:
        tickers.remove(ticker)
    tab["Stock"]=availible_tickers
    quant=[]
    OK_tickers=list()
    OK_metrics=list()

    if len(tickers) != 0:
        unav_tickers = ", ".join(tickers)
        raise Exception(f"Tickers '{unav_tickers}' are unavailible.")
    

    for metric in metrics:
        for i in range(len(availible_tickers)):
            value=float(mock_data[metric][i])
            quant.append(value)
        tab[metric]=quant
        quant=[]
    print(availible_tickers)
    for i in range(len(availible_tickers)):
        for metric in metrics:
            if tab[metric][i]==None:
                continue
            if (metric in ["returnOnEquity","grossMargins","operatingMargins","profitMargins","currentRatio","freeCashflow"]) and (tab[metric][i]>=OK_values[metric]):
                OK_metrics.append(metric)
            elif (metric in ["debtToEquity","trailingPE","forwardPE"]) and (tab[metric][i]<=OK_values[metric]):
                OK_metrics.append(metric)
        OK[availible_tickers[i]]=OK_metrics
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


    "Second faze"
    
    stocks=dict()
    stocks_date=dict()
    for ticker in availible_tickers:
        data = pd.read_csv(f"./mock_data/history/{ticker}.csv")
        dates = pd.to_datetime(data.index).strftime('%Y-%m-%d').tolist()
        ceny = data['Close'].dropna().tolist()
        ceny.remove(ceny[0]) 
        
        stocks[ticker] = np.array(ceny, dtype=float)
        stocks_date[ticker] = dates

    def fce(x: float, a: float, b: float, c: float, d:float) -> float:
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

    for ticker in availible_tickers:
        y_data = stocks[ticker]
        x_data = np.arange(1, len(y_data) + 1) 
        p0 = np.polyfit(x_data, y_data, deg=3)
        fit, _ = sp.optimize.curve_fit(fce, x_data, y_data, p0)
        a_fit, b_fit, c_fit, d_fit = fit
        x_fit = np.linspace(x_data.min(), x_data.max(), 100)
        y_fit = fce(x_fit, a_fit, b_fit, c_fit, d_fit)
        tick_fit[ticker]= (x_data, y_data, x_fit, y_fit, stocks_date[ticker])
    return tick_fit, availible_tickers
    
