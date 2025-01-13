import os
from stock_fetch import StockFetch
from signal_process import SignalProcessor
from telegram_notifier import TelegramNotifier
from config import SYMBOLS_FILE, STOCK_DATA_DIR, OUTPUT_DIR, CONSOLIDATED_OUTPUT_FILE, LOG_FILE, TOKEN, CHAT_ID

def main():
    # Step 1: Download stock data
    stock_fetcher = StockFetch(SYMBOLS_FILE, STOCK_DATA_DIR, LOG_FILE)
    failed_symbols = stock_fetcher.download_stock_data()

    if failed_symbols:
        print(f"Failed to download data for: {', '.join(failed_symbols)}")

    # Step 2: Process the stock data for signals
    processor = SignalProcessor(STOCK_DATA_DIR, OUTPUT_DIR)
    strategies_dict = processor.process_signals()

    if strategies_dict:
        print(f"Strategies generated: {strategies_dict}")
    else:
        print("No valid strategies were generated.")

    # Step 3: Consolidate the signals
    processor.consolidate_signals(CONSOLIDATED_OUTPUT_FILE)

    # Step 4: Send results via Telegram
    notifier = TelegramNotifier(token=TOKEN, chat_id=CHAT_ID)
    if strategies_dict:
        formatted_message = notifier.format_signals(strategies_dict)
        notifier.send_message(formatted_message)
    else:
        notifier.send_message("No valid signals were generated.")

    print("Pipeline complete. Consolidated signals saved.")

if __name__ == "__main__":
    main()