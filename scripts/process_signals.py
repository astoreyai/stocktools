import pandas as pd
from pipeline.ta_functions import process_signals, ensure_directory_exists
import os
import glob

def process_all_data(input_dir, output_dir):
    """Process all CSV files in the input directory and generate signals."""
    ensure_directory_exists(output_dir)
    
    for csv_file in glob.glob(os.path.join(input_dir, '*.csv')):
        data = pd.read_csv(csv_file, parse_dates=['Datetime'], index_col='Datetime')
        # Ensure the required columns are present
        data.columns = ['Open', 'High', 'Low', 'Close', 'Volume']
        
        # Extract the symbol from the filename
        symbol = os.path.basename(csv_file).replace('.csv', '')
        
        # Process signals
        process_signals(data, symbol, output_dir)

def main():
    """Main function to process all files."""
    input_dir = '/home/aaron/Documents/stocktools_main/data/stock_data'
    output_dir = '/home/aaron/Documents/stocktools_main/txt_files'
    
    process_all_data(input_dir, output_dir)
    print("Signal generation complete for all files in the directory.")

if __name__ == "__main__":
    main()
