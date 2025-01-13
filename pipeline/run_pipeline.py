import logging
from stock_fetch import StockFetch
from stock_processor import SignalProcessor
from config import CONSOLIDATED_OUTPUT_FILE, LOG_FILE, TOKEN, CHAT_ID

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename=LOG_FILE,
    filemode='a'  # Append to the log file
)

def download_stock_data():
    """Step 1: Download stock data."""
    try:
        stock_fetcher = StockFetch()  # Initialize StockFetch using config.py
        failed_symbols = stock_fetcher.download_stock_data()
        
        if failed_symbols:
            logging.warning(f"Failed to download data for: {', '.join(failed_symbols)}")
        
        return failed_symbols
    except Exception as e:
        logging.error(f"Error in downloading stock data: {e}")
        return []


def process_signals():
    """Step 2: Process the stock data for signals."""
    try:
        processor = SignalProcessor()
        strategies_dict = processor.scan_and_filter_signals()
        
        if strategies_dict:
            logging.info(f"Strategies generated: {strategies_dict}")
        else:
            logging.info("No valid strategies were generated.")
        
        return strategies_dict
    except Exception as e:
        logging.error(f"Error in processing signals: {e}")
        return {}


def consolidate_signals(strategies_dict):
    """Step 3: Consolidate the signals."""
    if strategies_dict:
        try:
            processor = SignalProcessor()
            processor.save_signals_to_file(strategies_dict)
            logging.info(f"Consolidated signals saved to {CONSOLIDATED_OUTPUT_FILE}")
        except Exception as e:
            logging.error(f"Error in consolidating signals: {e}")
    else:
        logging.info("No valid strategies generated. Skipping consolidation.")


def send_notifications(strategies_dict):
    """Step 4: Send results via Telegram."""
    if TOKEN and CHAT_ID:
        try:
            from stock_notifier import TelegramNotifier  # Import only if needed
            notifier = TelegramNotifier(token=TOKEN, chat_id=CHAT_ID)
            
            if strategies_dict:
                formatted_message = notifier.format_signals(strategies_dict)
                notifier.send_message(formatted_message)
            else:
                notifier.send_message("No valid signals were generated.")
        except Exception as e:
            logging.error(f"Error in sending Telegram notifications: {e}")
    else:
        logging.warning("Telegram notification skipped: Missing TOKEN or CHAT_ID.")


def main():
    logging.info("Pipeline started.")

    # Step 1: Download stock data
    download_stock_data()

    # Step 2: Process the stock data for signals
    strategies_dict = process_signals()

    # Step 3: Consolidate the signals
    consolidate_signals(strategies_dict)

    # Step 4: Send results via Telegram
    send_notifications(strategies_dict)

    logging.info("Pipeline complete. Consolidated signals saved.")


if __name__ == "__main__":
    main()
