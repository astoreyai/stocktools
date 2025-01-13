import talib
import numpy as np
import pandas as pd
import warnings

# ITG Scalper Strategy
def itg_scalper(df, len=14, FfastLength=12, FslowLength=26, FsignalLength=9):
    try:
        realC = df['Close']
        ema1 = talib.EMA(realC, timeperiod=len)
        ema2 = talib.EMA(ema1, timeperiod=len)
        ema3 = talib.EMA(ema2, timeperiod=len)
        avg = 3 * (ema1 - ema2) + ema3
        FfastMA = talib.EMA(realC, timeperiod=FfastLength)
        FslowMA = talib.EMA(realC, timeperiod=FslowLength)
        Fmacd = FfastMA - FslowMA
        Fsignal = talib.SMA(Fmacd, timeperiod=FsignalLength)
        longSignal = (np.where((Fmacd > Fsignal) & (avg > avg.shift(1)), 1, 0)).astype(bool)
        return longSignal
    except Exception as e:
        print(f"Error in itg_scalper: {e}")
        return pd.Series([False] * len(df))

# McGinley Dynamic Calculation
def mcginley_dynamic(series, length):
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        mg = np.zeros(len(series))
        mg[0] = series[0]  # Initial value
        for i in range(1, len(series)):
            mg[i] = mg[i-1] + (series[i] - mg[i-1]) / (length * (series[i] / mg[i-1])**4)
        return mg

# Bollinger Bands + RSI Strategy
def calculate_bollinger_bands(df, window=20, num_std=2.0):
    df['SMA'] = df['Close'].rolling(window).mean()
    df['STD'] = df['Close'].rolling(window).std()
    df['Upper Band'] = df['SMA'] + (df['STD'] * num_std)
    df['Lower Band'] = df['SMA'] - (df['STD'] * num_std)
    return df

def calculate_rsi(df, period=16):
    delta = df['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    df['RSI'] = 100 - (100 / (1 + rs))
    return df
