import os
from datetime import datetime

# Telegram Configuration
TOKEN = "blank"
CHAT_ID = 'blank'

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

# Ensure logs directory exists
if not os.path.exists(LOGS_DIR):
    os.makedirs(LOGS_DIR)