import os
import pandas as pd
import talib
from config import STOCK_POST_DIR, CONSOLIDATED_OUTPUT_FILE


class Indicator:
    """
    A class to encapsulate technical indicator calculations.
    """
    @staticmethod
    def calculate_macd(data, fast_length=12, slow_length=26, signal_length=9):
        """
        Calculate MACD and Signal Line from stock data, and return the last cross-up signal.

        Parameters:
            data (pd.DataFrame): DataFrame containing stock data with 'Close' column.
            fast_length (int): Fast length for MACD.
            slow_length (int): Slow length for MACD.
            signal_length (int): Signal length for Signal Line.

        Returns:
            pd.DataFrame: DataFrame with MACD, Signal Line, Histogram, and crossovers.
            pd.Timestamp: Last Long Position Date (MACD Cross Up).
        """
        if 'Close' not in data.columns:
            raise ValueError("The input data must contain a 'Close' column.")

        # Calculate Fast and Slow Moving Averages (Oscillator)
        fast_ma = talib.EMA(data['Close'], timeperiod=fast_length)
        slow_ma = talib.EMA(data['Close'], timeperiod=slow_length)

        # Calculate MACD and Signal Line
        macd = fast_ma - slow_ma
        signal = talib.EMA(macd, timeperiod=signal_length)

        # Calculate Histogram (MACD - Signal)
        hist = macd - signal

        # Detect Crossovers (MACD crossing above Signal Line)
        cross_up = (macd.shift(1) <= signal.shift(1)) & (macd > signal)

        # Add calculated columns to the DataFrame
        data['MACD'] = macd
        data['Signal Line'] = signal
        data['Histogram'] = hist
        data['Cross Up'] = cross_up

        # Find the last "cross-up" position
        last_cross_up = data.loc[data['Cross Up'], 'Datetime'].max() if not data.loc[data['Cross Up']].empty else None

        return data, last_cross_up


class StockScreener:
    """
    A class to handle stock screening based on technical indicators.
    """
    def __init__(self, stock_dir):
        if not os.path.exists(stock_dir):
            raise FileNotFoundError(f"The directory {stock_dir} does not exist.")
        self.stock_dir = stock_dir

    def screen_by_indicator(self, indicator_func):
        """
        Process all stock data and find signals based on the given indicator function.

        Parameters:
            indicator_func (function): A function that calculates the indicator and returns the last signal date.

        Returns:
            list: A list of tuples containing stock symbols and their last signal dates.
        """
        signals = []

        # Iterate over all CSV files in the processed stock data directory
        for file_name in os.listdir(self.stock_dir):
            if file_name.endswith(".csv"):
                stock_symbol = os.path.splitext(file_name)[0]
                file_path = os.path.join(self.stock_dir, file_name)

                # Load stock data
                data = pd.read_csv(file_path)
                if 'Datetime' not in data.columns:
                    raise ValueError(f"The file {file_name} must contain a 'Datetime' column.")
                data['Datetime'] = pd.to_datetime(data['Datetime'])

                # Calculate the indicator and find the last signal
                _, last_signal = indicator_func(data)

                if last_signal:
                    signals.append((stock_symbol, last_signal))

        return signals

    @staticmethod
    def save_signals_to_file(signals, output_file):
        """
        Save the list of detected signals to a file.

        Parameters:
            signals (list): List of tuples containing stock symbols and their last signal dates.
            output_file (str): Path to the output file for saving signals.
        """
        if not signals:
            print("No signals found.")
            return

        # Save the results to a CSV file
        signals_df = pd.DataFrame(signals, columns=["Stock Symbol", "Last Signal Date"])
        os.makedirs(os.path.dirname(output_file), exist_ok=True)  # Ensure output directory exists
        signals_df.to_csv(output_file, index=False)
        print(f"Signals saved to {output_file}")


# Main Execution
if __name__ == "__main__":
    try:
        screener = StockScreener(stock_dir=STOCK_POST_DIR)

        # Screen stocks using the MACD indicator
        macd_signals = screener.screen_by_indicator(Indicator.calculate_macd)

        # Save the signals to the consolidated output file
        screener.save_signals_to_file(macd_signals, output_file=CONSOLIDATED_OUTPUT_FILE)

    except Exception as e:
        print(f"Error: {e}")
