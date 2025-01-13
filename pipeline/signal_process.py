import os
import pandas as pd
from datetime import datetime
from stock_strategies import StockStrategies

print("StockStrategies imported successfully.")  # Debugging line to ensure import is working

class SignalProcessor:
    def __init__(self, stock_data_dir, output_dir):
        self.stock_data_dir = stock_data_dir
        self.output_dir = output_dir

    def ensure_directory_exists(self, directory):
        """Ensure the directory exists, create if not."""
        if not os.path.exists(directory):
            os.makedirs(directory)

    def process_signals(self):
        """Process the stock data to generate trading signals."""
        try:
            strategies_dict = StockStrategies.scan_folder_for_signals(self.stock_data_dir)
            if strategies_dict:
                print("Signals generated successfully.")
            else:
                print("No signals generated.")
            return strategies_dict
        except Exception as e:
            print(f"Error processing signals: {e}")
            return {}

    def consolidate_signals(self, output_file):
        """Consolidate all signal files into one CSV."""
        self.ensure_directory_exists(self.output_dir)
        dataframes = self.read_signal_files(self.stock_data_dir)
        if not dataframes:
            print("No signal dataframes to consolidate.")
            return

        consolidated_df = pd.concat(dataframes, ignore_index=True)
        consolidated_df.to_csv(output_file, index=False)
        print(f"Consolidated signals saved to {output_file}")

    def read_signal_files(self, signal_dir):
        """Read all CSV signal files in the given directory."""
        dataframes = []
        for signal_file in os.listdir(signal_dir):
            file_path = os.path.join(signal_dir, signal_file)
            if os.path.isfile(file_path) and signal_file.endswith('.csv'):
                try:
                    df = pd.read_csv(file_path)
                    if not df.empty:
                        dataframes.append(df)
                    else:
                        print(f"File {file_path} is empty.")
                except Exception as e:
                    print(f"Error reading {file_path}: {e}")
        return dataframes

    def save_signals_to_file(self, strategies_dict):
        """Save the generated signals to a text file."""
        self.ensure_directory_exists(self.output_dir)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file_path = os.path.join(self.output_dir, f'signals_{timestamp}.txt')
        
        with open(output_file_path, 'w') as f:
            f.write(f"Stock Scanning Results - {timestamp}\n\n")
            for strategy, stocks in strategies_dict.items():
                f.write(f"{strategy}:\n")
                for stock in stocks:
                    f.write(f"  {stock}\n")
                f.write("\n")

        print(f"\nResults saved to: {output_file_path}")
