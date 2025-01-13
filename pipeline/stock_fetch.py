import os
import pandas as pd
import yfinance as yf
from tqdm import tqdm

class StockFetch:
    def __init__(self, symbols_file, output_dir, log_file):
        """Initialize StockFetch with paths for symbols file, output directory, and log file."""
        self.symbols_file = symbols_file
        self.output_dir = output_dir
        self.log_file = log_file

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
        """Download 1-hour stock data from yfinance for symbols in the symbols_file."""
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
                        # Suppress the yfinance output using progress=False
                        data = yf.download(symbol, interval='1h', period='1mo', progress=False)
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

# Example usage:
# Initialize the class with file paths
# stock_fetcher = StockFetch(
#     symbols_file='path_to_symbols.csv',
#     output_dir='path_to_output_directory',
#     log_file='path_to_log_file.txt'
# )

# Fetch stock data
# failed_symbols = stock_fetcher.download_stock_data()
