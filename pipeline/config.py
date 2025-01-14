import os
from datetime import datetime
from dotenv import load_dotenv  # Import dotenv for environment variable handling

# Load environment variables from a .env file
load_dotenv()

# Telegram Configuration
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')  # Your Telegram Bot Token
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')      # Your Telegram Chat ID

# Define the base directory of the project
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Define the main data directory
DATA_DIR = os.path.join(BASE_DIR, 'data')

# Define the logs directory for storing log files
LOGS_DIR = os.path.join(BASE_DIR, 'logs')

# Define the path to the symbols file (e.g., for stock symbols)
SYMBOLS_FILE = os.path.join(DATA_DIR, 'symbols', 'symbols.csv')

# Define the directory for processed stock data (post-processed data)
STOCK_POST_DIR = os.path.join(DATA_DIR, 'processed_stock_data')

# Define the directory for raw stock data (before processing)
STOCK_PRE_DIR = os.path.join(DATA_DIR, 'raw_stock_data')

# Define the directory for signals (consolidated output files)
SIGNALS_DIR = os.path.join(DATA_DIR, 'signals')

# Define the consolidated output file path for stock signals
CONSOLIDATED_OUTPUT_FILE = os.path.join(SIGNALS_DIR, 'consolidated_signals.csv')

# Define the log file path with a timestamp
LOG_FILE = os.path.join(LOGS_DIR, f"download_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt")

# Ensure each directory exists; create it if it doesn't
directories = [DATA_DIR, LOGS_DIR, os.path.dirname(SYMBOLS_FILE), STOCK_POST_DIR, STOCK_PRE_DIR, SIGNALS_DIR]

for directory in directories:
    if not os.path.exists(directory):
        os.makedirs(directory)
        print(f"Created directory: {directory}")

# Output confirmation of key paths (optional for debugging)
print(f"Base Directory: {BASE_DIR}")
print(f"Data Directory: {DATA_DIR}")
print(f"Logs Directory: {LOGS_DIR}")
print(f"Symbols File: {SYMBOLS_FILE}")
print(f"Processed Stock Data Directory: {STOCK_POST_DIR}")
print(f"Raw Stock Data Directory: {STOCK_PRE_DIR}")
print(f"Signals Directory: {SIGNALS_DIR}")
print(f"Consolidated Output File: {CONSOLIDATED_OUTPUT_FILE}")
print(f"Log File: {LOG_FILE}")


# Stock data download configurations
INTERVAL = '1d'          # Time interval for data ('1m','2m','5m','15m','30m','60m','90m','1h','1d','5d','1wk','1mo','3mo')
PERIOD = '1y'           # Period for historical data ('1d','5d','1mo','3mo','6mo','1y','2y','5y','10y','ytd','max')

# Configurations for indicators
TEMA_CONFIG = {
    'length': 14  # Period for TEMA calculation
}

MACD_CONFIG = {
    'fast_length': 12,  # Fast EMA period
    'slow_length': 26,  # Slow EMA period
    'signal_length': 9  # Signal EMA period
}

RSI_CONFIG = {
    'period': 14,        # Period for RSI calculation
    'rsi_cutoff': 30     # RSI value below which a long signal is triggered
}