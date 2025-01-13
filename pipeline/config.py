import os
from datetime import datetime

# Telegram Configuration
TOKEN = "fill in"
CHAT_ID = 'fill in'

# Define project directories
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')
LOGS_DIR = os.path.join(BASE_DIR, 'logs')

# Paths for stock data and symbols
SYMBOLS_FILE = os.path.join(DATA_DIR, 'symbols', 'tv_tickers.csv')
STOCK_DATA_DIR = os.path.join(DATA_DIR, 'stock_data')
OUTPUT_DIR = os.path.join(DATA_DIR, 'txt_files')
CONSOLIDATED_OUTPUT_FILE = os.path.join(DATA_DIR, 'consolidated_signals.csv')

# Create log file with timestamp
LOG_FILE = os.path.join(LOGS_DIR, f"download_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt")

# Configurations for stock data download
OUTPUT_DIR = 'output_data'
LOG_FILE = 'log.txt'
INTERVAL = '1d'
PERIOD = '30d'
BACKLOOK_DAYS = 3  # Number of days to look back for signals

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

# Ensure logs directory exists
if not os.path.exists(LOGS_DIR):
    os.makedirs(LOGS_DIR)