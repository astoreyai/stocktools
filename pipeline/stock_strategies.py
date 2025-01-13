import pandas as pd
import talib
import numpy as np
import os

class StockStrategies:
    
    @staticmethod
    def itg_scalper(df, len=14, FfastLength=12, FslowLength=26, FsignalLength=9):
        try:
            realC = df['Close']
            # Triple EMA
            ema1 = talib.EMA(realC, timeperiod=len)
            ema2 = talib.EMA(ema1, timeperiod=len)
            ema3 = talib.EMA(ema2, timeperiod=len)
            avg = 3 * (ema1 - ema2) + ema3
            # Filter formula
            FfastMA = talib.EMA(realC, timeperiod=FfastLength)
            FslowMA = talib.EMA(realC, timeperiod=FslowLength)
            Fmacd = FfastMA - FslowMA
            Fsignal = talib.SMA(Fmacd, timeperiod=FsignalLength)
            # Entry condition
            longSignal = (np.where((Fmacd > Fsignal) & (avg > avg.shift(1)), 1, 0)).astype(bool)
            return longSignal
        except Exception as e:
            print(f"Error in itg_scalper: {e}")
            return pd.Series([False] * len(df))
    
    @staticmethod
    def mcginley_dynamic(series, length):
        """McGinley Dynamic calculation."""
        mg = np.zeros(len(series))
        mg[0] = series[0]  # Initial value
        for i in range(1, len(series)):
            mg[i] = mg[i - 1] + (series[i] - mg[i - 1]) / (length * (series[i] / mg[i - 1]) ** 4)
        return mg

    @staticmethod
    def calculate_bollinger_bands(df, window=20, num_std=2.0):
        df['SMA'] = df['Close'].rolling(window).mean()
        df['STD'] = df['Close'].rolling(window).std()
        df['Upper Band'] = df['SMA'] + (df['STD'] * num_std)
        df['Lower Band'] = df['SMA'] - (df['STD'] * num_std)
        return df

    @staticmethod
    def calculate_rsi(df, period=16):
        delta = df['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / loss
        df['RSI'] = 100 - (100 / (1 + rs))
        return df

    @staticmethod
    def generate_bollinger_rsi_signals(df, rsi_period=16, rsi_value=45, bb_period=20, bb_std=2.0):
        df = StockStrategies.calculate_rsi(df, period=rsi_period)
        df = StockStrategies.calculate_bollinger_bands(df, window=bb_period, num_std=bb_std)
        
        RSIoverSold = rsi_value
        RSIoverBought = 100 - rsi_value
        
        df['Signal'] = 0
        df['Signal'] = np.where(
            (df['RSI'] < RSIoverSold) & (df['Close'] < df['Lower Band']), 1, df['Signal'])
        df['Signal'] = np.where(
            (df['RSI'] > RSIoverBought) & (df['Close'] > df['Upper Band']), -1, df['Signal'])
        df['Position'] = df['Signal'].shift()
        return df

    @staticmethod
    def scan_stock_for_signals(file_path):
        data = pd.read_csv(file_path)
        data = data.sort_values('Datetime')

        try:
            for col in ['Close', 'High', 'Low']:
                if col not in data.columns:
                    raise ValueError(f"Missing column: {col}")

            data['ITG'] = StockStrategies.itg_scalper(data)

            data['RSI'] = talib.RSI(data['Close'], timeperiod=14)
            data['MACD'], data['MACDSignal'], _ = talib.MACD(data['Close'], fastperiod=12, slowperiod=26, signalperiod=9)

            data['Jaw'] = StockStrategies.mcginley_dynamic((data['High'] + data['Low']) / 2, 13)
            data['Teeth'] = StockStrategies.mcginley_dynamic((data['High'] + data['Low']) / 2, 8)
            data['Lips'] = StockStrategies.mcginley_dynamic((data['High'] + data['Low']) / 2, 5)

            data['Jaw_ROC'] = talib.ROC(data['Jaw'], timeperiod=1)
            data['Teeth_ROC'] = talib.ROC(data['Teeth'], timeperiod=1)
            data['Lips_ROC'] = talib.ROC(data['Lips'], timeperiod=1)

            data = StockStrategies.generate_bollinger_rsi_signals(data)

            itg_signal = data['ITG'].iloc[-1]
            macd_signal = data['MACD'].iloc[-1] > data['MACDSignal'].iloc[-1]
            rsi_signal = data['RSI'].iloc[-1] < 30
            oar_signal = (data['Lips_ROC'].iloc[-1] > data['Teeth_ROC'].iloc[-1]) and \
                         (data['Teeth_ROC'].iloc[-1] > data['Jaw_ROC'].iloc[-1])

            strategies = []
            if itg_signal and macd_signal:
                strategies.append('Strategy 1')
            if data['Position'].iloc[-1] == 1:
                strategies.append('Strategy 2')
            if rsi_signal and oar_signal:
                strategies.append('Strategy 3')

            return strategies
        except Exception as e:
            print(f"Error processing {file_path}: {e}")
            return []

    @staticmethod
    def scan_folder_for_signals(folder_path):
        if not os.path.exists(folder_path):
            print(f"Directory {folder_path} does not exist.")
            return {}

        strategies_dict = {
            'ITG Scalper + MACD': [],
            'Bollinger Bands + RSI': [],
            'RSI + Alligator': []
        }

        for file_name in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file_name)
            if file_path.endswith('.csv'):
                strategies = StockStrategies.scan_stock_for_signals(file_path)
                stock_symbol = os.path.splitext(file_name)[0]
                for strategy in strategies:
                    if strategy == 'Strategy 1':
                        strategies_dict['ITG Scalper + MACD'].append(stock_symbol)
                    elif strategy == 'Strategy 2':
                        strategies_dict['Bollinger Bands + RSI'].append(stock_symbol)
                    elif strategy == 'Strategy 3':
                        strategies_dict['RSI + Alligator'].append(stock_symbol)
        return strategies_dict
