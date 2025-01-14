from stock_fetch import StockFetch
from stock_prep import StockPrep, StockFilter
from stock_indicators import Indicator, StockScreener
from stock_notifier import TelegramNotifier
from config import CONSOLIDATED_OUTPUT_FILE, STOCK_POST_DIR

def main():
    # Print configuration paths for verification
    print(f"Consolidated Output File: {CONSOLIDATED_OUTPUT_FILE}")
    print(f"Processed Stock Data Directory: {STOCK_POST_DIR}")

    # Step 1: Fetch stock data
    fetcher = StockFetch()
    failed_symbols = fetcher.download_stock_data()

    # Check if any symbols failed
    if failed_symbols:
        print(f"Failed to download data for: {failed_symbols}")
    else:
        print("All stock data downloaded successfully.")

    # Step 2: Preprocess stock data
    prep = StockPrep()
    preprocessed_files = prep.preprocess_all()

    # Display preprocessed files
    if preprocessed_files:
        print("Preprocessed files:")
        for file in preprocessed_files:
            print(file)
    else:
        print("No files were preprocessed.")

    # Step 3: Screen for MACD signals
    screener = StockScreener(stock_dir=STOCK_POST_DIR)
    macd_signals = screener.screen_by_indicator(Indicator.calculate_macd)

    # Save signals to the consolidated output file
    screener.save_signals_to_file(macd_signals, output_file=CONSOLIDATED_OUTPUT_FILE)

    # Display saved signals
    print("MACD Signals saved to:", CONSOLIDATED_OUTPUT_FILE)

    # Step 4: Filter stock signals
    stock_filter = StockFilter(CONSOLIDATED_OUTPUT_FILE)
    stock_filter.filter_and_sort_data()

    # Load and display the filtered data
    filtered_data = stock_filter.filtered_data
    if filtered_data is not None and not filtered_data.empty:
        print("Filtered Signals:")
        print(filtered_data)  # Use print instead of `display` for non-Jupyter environments
    else:
        print("No signals found after filtering.")

    # Step 5: Send signals via Telegram
    if filtered_data is not None and not filtered_data.empty:
        notifier = TelegramNotifier()
        formatted_message = notifier.format_signals(filtered_data)

        # Display the message to be sent
        print("Message to be sent via Telegram:")
        print(formatted_message)

        # Send the message
        notifier.send_message(formatted_message)
    else:
        print("No stock signals to send via Telegram.")

if __name__ == "__main__":
    main()
