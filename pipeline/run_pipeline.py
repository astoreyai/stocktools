import pandas as pd
import logging
import os

# Import your custom modules
from stock_fetch import StockFetch
from stock_prep import StockPrep, StockFilter
from stock_indicators import StockIndicators, StockScreener
from stock_notifier import TelegramNotifier
from config import CONSOLIDATED_OUTPUT_FILE, STOCK_POST_DIR
from stock_utils import DataUtils  # Assuming DataUtils is saved in data_utils.py



def main():

    # Initialize DataUtils
    data_utils = DataUtils()

    # Reset the signal generator at the start of execution
    print("Resetting signal generator...")
    data_utils.reset_signal_generator()
    
    # Step 1: Fetch stock data
    print("Fetching stock data...")
    fetcher = StockFetch()
    failed_symbols = fetcher.download_stock_data()

    # Check if any symbols failed
    if failed_symbols:
        print(f"Failed to download data for: {failed_symbols}")
    else:
        print("All stock data downloaded successfully.")

    # Step 2: Preprocess stock data
    print("Preprocessing stock data...")
    prep = StockPrep()
    preprocessed_files = prep.preprocess_all()

    # Display preprocessed files
    if preprocessed_files:
        print("Preprocessed files:")
        for file in preprocessed_files:
            print(file)
    else:
        print("No files were preprocessed.")

    # Step 3: Process all indicators
    print("Processing stock indicators...")
    screener = StockScreener(stock_dir=STOCK_POST_DIR)

    # Define the list of indicators
    indicators = [StockIndicators.calculate_macd, StockIndicators.calculate_rsi]

    # Call screen_by_indicators with the list of indicators and the output file
    screener.screen_by_indicators(indicators=indicators, output_file=CONSOLIDATED_OUTPUT_FILE)

    # Load and display consolidated signals (optional)
    consolidated_signals = pd.read_csv(CONSOLIDATED_OUTPUT_FILE)
    print("Consolidated signals saved to:", CONSOLIDATED_OUTPUT_FILE)

    # Display the first few rows of the saved signals
    consolidated_signals.head()

    print("Filtering and aggregating stock signals...")

    # Initialize StockFilter and tally signals
    stock_filter = StockFilter(CONSOLIDATED_OUTPUT_FILE)
    stock_filter.tally_signals()  # Tally signals within the lookback period

    # Check if there is filtered data
    if stock_filter.filtered_data is not None and not stock_filter.filtered_data.empty:
        # Sort data by symbol and datetime (alphabetize)
        filtered_data = stock_filter.filtered_data.sort_values(by=['symbol', 'datetime'], ascending=[True, False])
        stock_filter.filtered_data = filtered_data.copy()  # Use `.copy()` to avoid SettingWithCopyWarning

        # Save filtered and aggregated signals to a file
        filtered_output_file = CONSOLIDATED_OUTPUT_FILE.replace(".csv", "_filtered.csv")
        stock_filter.save_filtered_data(filtered_output_file)

        # Display filtered and aggregated data
        print("Filtered and aggregated signals:")
        print(stock_filter.filtered_data.head())
    else:
        print("No signals found after filtering and aggregation.")

    # Step 5: Send notifications via Telegram
    print("Sending notifications via Telegram...")

    # Check if filtered data exists and is not empty
    if stock_filter.filtered_data is not None and not stock_filter.filtered_data.empty:
        try:
            # Initialize TelegramNotifier
            notifier = TelegramNotifier()

            # Format the filtered signals for the message
            formatted_message = notifier.format_signals(stock_filter.filtered_data)

            # Display the formatted message for verification
            print("Message to be sent via Telegram:")
            print(formatted_message)

            # Send the message via Telegram
            notifier.send_message(formatted_message)
            print("✅ Notification sent successfully.")

        except Exception as e:
            # Handle any exceptions during the notification process
            print(f"❌ Error while sending Telegram notification: {e}")
            logging.error(f"Error while sending Telegram notification: {e}")

    else:
        # Handle the case where there are no signals to send
        print("🚨 No stock signals to send via Telegram.")

if __name__ == "__main__":
    main()
