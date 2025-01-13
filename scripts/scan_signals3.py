import os
import pandas as pd
from pipeline.ta_functions import calculate_macd, calculate_rsi, itg_scalper

# Scan each stock file and generate signals
def scan_and_save_signals(folder_path, output_file_path):
    strategies_dict = {
        'ITG Scalper + MACD': [],
        'RSI': [],
    }
    
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        if file_path.endswith('.csv'):
            stock_symbol = os.path.splitext(file_name)[0]
            data = pd.read_csv(file_path)

            # Generate signals for the stock
            itg_signals = itg_scalper(data)
            macd_signals = calculate_macd(data)
            rsi_signals = calculate_rsi(data)
            
            # Check the last two intervals for signals
            if itg_signals.iloc[-1] == 1 or macd_signals.iloc[-1] == 1:
                strategies_dict['ITG Scalper + MACD'].append(stock_symbol)
            if rsi_signals.iloc[-1] == 1:
                strategies_dict['RSI'].append(stock_symbol)
    
    # Write the results to the output file
    with open(output_file_path, 'w') as f:
        f.write(f"Stock Scanning Results - {pd.Timestamp.now()}\n\n")
        for strategy, stocks in strategies_dict.items():
            f.write(f"{strategy}:\n")
            for stock in stocks:
                f.write(f"  {stock}\n")
            f.write("\n")

    print(f"Signals saved to {output_file_path}")
