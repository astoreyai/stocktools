import os
from datetime import datetime
from pipeline.ta_functions import fetch_and_save_data
from scan_signals3 import scan_and_save_signals
from pipeline.telegram_notifier import send_signals

# Define paths
input_file = 'data/symbols/tv_tickers.csv'
output_folder = 'data/stock_data/1hour_data'
output_signals_file = 'data/txt_files/signals_1h.txt'

# Main function to fetch data, scan signals, and send notifications
def main():
    print(f"Running Stock Monitoring and Signal Aggregation at {datetime.now()}")

    # Step 1: Fetch stock data
    symbols = load_tickers(input_file)
    for symbol in symbols:
        fetch_and_save_data(symbol, output_folder)

    # Step 2: Scan for signals
    scan_and_save_signals(output_folder, output_signals_file)

    # Step 3: Send signals to Telegram
    send_signals(output_signals_file)

if __name__ == "__main__":
    main()
