import pandas as pd
import talib
from config import TEMA_CONFIG, MACD_CONFIG, RSI_CONFIG


class StockStrategies:
    @staticmethod
    def tema_signal(df):
        """
        Calculates TEMA and identifies long signals.
        """
        try:
            realC = df['Close']
            length = TEMA_CONFIG['length']

            # Triple EMA Calculation
            ema1 = talib.EMA(realC, timeperiod=length)
            ema2 = talib.EMA(ema1, timeperiod=length)
            ema3 = talib.EMA(ema2, timeperiod=length)
            avg = 3 * (ema1 - ema2) + ema3

            # Long signal condition
            long_signal = avg > avg.shift(1)
            return long_signal.astype(bool)
        except Exception as e:
            print(f"Error in TEMA calculation: {e}")
            return pd.Series([False] * len(df), index=df.index)

    @staticmethod
    def macd_signal(df):
        """
        Calculates MACD and identifies long signals.
        """
        try:
            fast_length = MACD_CONFIG['fast_length']
            slow_length = MACD_CONFIG['slow_length']
            signal_length = MACD_CONFIG['signal_length']

            macd, macd_signal, _ = talib.MACD(
                df['Close'], fastperiod=fast_length, slowperiod=slow_length, signalperiod=signal_length
            )

            # Long signal condition
            long_signal = macd > macd_signal
            return long_signal.astype(bool)
        except Exception as e:
            print(f"Error in MACD calculation: {e}")
            return pd.Series([False] * len(df), index=df.index)

    @staticmethod
    def rsi_signal(df):
        """
        Calculates RSI and identifies long signals when RSI is below the cutoff.
        """
        try:
            period = RSI_CONFIG['period']
            rsi_cutoff = RSI_CONFIG['rsi_cutoff']

            rsi = talib.RSI(df['Close'], timeperiod=period)

            # Long signal condition
            long_signal = rsi < rsi_cutoff
            df['RSI'] = rsi  # Store RSI for analysis
            return long_signal.astype(bool)
        except Exception as e:
            print(f"Error in RSI calculation: {e}")
            return pd.Series([False] * len(df), index=df.index)
