import os
import pandas as pd
from datetime import datetime, timedelta
from stock_strategies import StockStrategies
from config import STOCK_DATA_DIR, OUTPUT_DIR, BACKLOOK_DAYS


class SignalProcessor:
    def __init__(self):
        self.stock_data_dir = STOCK_DATA_DIR
        self.output_dir = OUTPUT_DIR
        self.backlook_days = BACKLOOK_DAYS  # Backlook days from config

    @staticmethod
    def ensure_directory_exists(directory):
        """Ensure the specified directory exists."""
        if not os.path.exists(directory):
            os.makedirs(directory)

    @staticmethod
    def validate_timestamp(timestamp, format="%Y-%m-%d %H:%M:%S"):
        """Validate and convert timestamp to datetime object."""
        try:
            return datetime.strptime(timestamp, format)
        except ValueError:
            return None

    @staticmethod
    def scan_stock_for_signals(file_path):
        """
        Scan a single stock CSV file for TEMA, MACD, and RSI signals.
        Returns the detected strategies and the last timestamp.
        """
        try:
            # Read stock data
            data = pd.read_csv(file_path)
            data = data.sort_values('Datetime')

            # Ensure required columns exist
            required_columns = {'Close', 'High', 'Low', 'Datetime'}
            if not required_columns.issubset(data.columns):
                raise ValueError(f"Missing required columns in {file_path}")

            # Check for signals
            tema_signal = StockStrategies.tema_signal(data).iloc[-1]
            macd_signal = StockStrategies.macd_signal(data).iloc[-1]
            rsi_signal = StockStrategies.rsi_signal(data).iloc[-1]

            # Compile detected strategies
            strategies = []
            if tema_signal:
                strategies.append('TEMA Strategy')
            if macd_signal:
                strategies.append('MACD Strategy')
            if rsi_signal:
                strategies.append('RSI Strategy')

            last_timestamp = data['Datetime'].iloc[-1]
            return strategies, last_timestamp
        except Exception as e:
            print(f"Error processing {file_path}: {e}")
            return [], None

    def scan_folder_for_signals(self):
        """
        Scan all stock files in the folder for signals.
        Returns a dictionary with strategies and their associated stocks and timestamps.
        """
        if not os.path.exists(self.stock_data_dir):
            print(f"Stock data directory {self.stock_data_dir} does not exist.")
            return {}

        strategies_dict = {
            'TEMA Strategy': [],
            'MACD Strategy': [],
            'RSI Strategy': []
        }

        for file_name in os.listdir(self.stock_data_dir):
            if file_name.endswith('.csv'):
                file_path = os.path.join(self.stock_data_dir, file_name)
                strategies, last_timestamp = self.scan_stock_for_signals(file_path)
                stock_symbol = os.path.splitext(file_name)[0]
                for strategy in strategies:
                    strategies_dict[strategy].append((stock_symbol, last_timestamp))

        return strategies_dict

    def filter_signals_by_backlook(self, strategies_dict):
        """
        Filter stock signals to include only those within the backlook period.
        """
        recent_signals = {}
        now = datetime.now()
        backlook_time = now - timedelta(days=self.backlook_days)

        for strategy, stocks in strategies_dict.items():
            recent_stocks = [
                (stock, timestamp)
                for stock, timestamp in stocks
                if self.validate_timestamp(timestamp) >= backlook_time
            ]
            if recent_stocks:
                recent_signals[strategy] = recent_stocks

        return recent_signals

    def save_signals_to_file(self, strategies_dict):
        """
        Save signals to a file in the output directory.
        """
        if not strategies_dict:
            print("No signals to save.")
            return

        self.ensure_directory_exists(self.output_dir)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file_path = os.path.join(self.output_dir, f'signals_{timestamp}.txt')

        try:
            with open(output_file_path, 'w') as f:
                f.write(f"Stock Signals Report - {timestamp}\n\n")
                for strategy, stocks in strategies_dict.items():
                    f.write(f"{strategy}:\n")
                    for stock, stock_time in stocks:
                        f.write(f"  {stock} (Last Signal: {stock_time})\n")
                    f.write("\n")
            print(f"Signals saved to {output_file_path}")
        except Exception as e:
            print(f"Error saving signals to file: {e}")

    def scan_and_report_signals(self):
        """
        Scan stock data, filter signals by the backlook period, and save results if any signals are found.
        """
        try:
            # Step 1: Scan for signals
            strategies_dict = self.scan_folder_for_signals()

            # Step 2: Filter signals by backlook period
            filtered_signals = self.filter_signals_by_backlook(strategies_dict)

            # Step 3: Save and report signals
            if filtered_signals:
                print("Signals detected within the backlook period.")
                self.save_signals_to_file(filtered_signals)
            else:
                print(f"No signals found within the past {self.backlook_days} days.")

        except Exception as e:
            print(f"Error in scanning and reporting signals: {e}")
