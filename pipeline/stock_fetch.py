import os
import pandas as pd
import yfinance as yf
from tqdm import tqdm
import config  # Import only the config file, no other project modules

class StockFetch:
    def __init__(self):
        """Initialize StockFetch with configurations from the config file."""
        self.symbols_file = config.SYMBOLS_FILE
        self.output_dir = config.OUTPUT_DIR
        self.log_file = config.LOG_FILE
        self.interval = config.INTERVAL
        self.period = config.PERIOD

    @staticmethod
    def ensure_directory_exists(directory):
        """Ensure the directory exists, if not create it."""
        if not os.path.exists(directory):
            os.makedirs(directory)

    def log_to_file(self, message):
        """Log messages to a specified logfile."""
        with open(self.log_file, 'a') as f:
            f.write(message + '\n')

    def download_stock_data(self):
        """Download stock data from yfinance for symbols in the symbols file."""
        # Ensure the output directory exists
        self.ensure_directory_exists(self.output_dir)

        try:
            # Load symbols from the CSV file
            symbols_df = pd.read_csv(self.symbols_file)
            symbols = symbols_df['Symbol'].tolist()
            failed_symbols = []

            # Progress bar for all symbols
            with tqdm(total=len(symbols), desc="Downloading stock data", unit="symbol", leave=False) as pbar:
                for symbol in symbols:
                    try:
                        # Download stock data with the configured interval and period
                        data = yf.download(symbol, interval=self.interval, period=self.period, progress=False)
                        if not data.empty:
                            output_file = os.path.join(self.output_dir, f"{symbol}.csv")
                            data.to_csv(output_file)
                            self.log_to_file(f"Data for {symbol} saved to {output_file}")
                        else:
                            self.log_to_file(f"No data for {symbol}")
                            failed_symbols.append(symbol)
                    except Exception as e:
                        self.log_to_file(f"Failed to download data for {symbol}: {e}")
                        failed_symbols.append(symbol)
                    finally:
                        pbar.update(1)

            # Handle failed symbols
            if failed_symbols:
                self.log_to_file(f"Symbols that failed to download: {', '.join(failed_symbols)}")

                # Remove failed symbols from the CSV file
                symbols_df = symbols_df[~symbols_df['Symbol'].isin(failed_symbols)]
                symbols_df.to_csv(self.symbols_file, index=False)
                self.log_to_file("Failed symbols removed from the symbols CSV file.")

            return failed_symbols

        except Exception as e:
            self.log_to_file(f"Error: {e}")
            return []
