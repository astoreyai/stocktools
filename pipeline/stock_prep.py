import os
import pandas as pd
import logging
from config import STOCK_PRE_DIR, STOCK_POST_DIR
from datetime import datetime, timedelta

class StockPrep:
    """
    A class to handle the preprocessing of stock data.
    """

    def __init__(self, raw_data_dir=STOCK_PRE_DIR, processed_data_dir=STOCK_POST_DIR):
        """
        Initialize the StockPrep class with configurations.
        """
        self.raw_data_dir = raw_data_dir  # Directory for raw stock data
        self.processed_data_dir = processed_data_dir  # Directory for processed stock data

        # Ensure required directories exist
        self._ensure_directory_exists(self.processed_data_dir)

    @staticmethod
    def _ensure_directory_exists(directory):
        """
        Ensure the specified directory exists.
        """
        if not os.path.exists(directory):
            os.makedirs(directory)
            logging.info(f"Created directory: {directory}")

    def preprocess_file(self, csv_file_path):
        """
        Preprocess a single raw stock data file.

        :param csv_file_path: Path to the raw stock data file.
        :return: Path to the preprocessed file or None if an error occurs.
        """
        try:
            # Read the raw CSV file
            data = pd.read_csv(csv_file_path, header=0)

            # Rename the 'Price' column to 'Datetime'
            data.rename(columns={"Price": "Datetime"}, inplace=True)

            # Drop rows 1 and 2 (Ticker and Date rows)
            data = data.iloc[2:].reset_index(drop=True)

            # Ensure the 'Datetime' column exists and convert to datetime format
            data["Datetime"] = pd.to_datetime(data["Datetime"], format="%Y-%m-%d", errors="coerce")

            # Drop rows with invalid dates
            invalid_dates = data["Datetime"].isnull().sum()
            if invalid_dates > 0:
                logging.warning(f"File {csv_file_path} contains {invalid_dates} invalid dates. Dropping those rows.")
                data = data[~data["Datetime"].isnull()]

            # Sort by 'Datetime'
            data.sort_values("Datetime", inplace=True)

            # Save the preprocessed file to the processed data directory
            processed_file_path = os.path.join(self.processed_data_dir, os.path.basename(csv_file_path))
            data.to_csv(processed_file_path, index=False)

            logging.info(f"Preprocessed data saved to {processed_file_path}")
            return processed_file_path
        except Exception as e:
            logging.error(f"Error preprocessing file {csv_file_path}: {e}")
            return None

    def preprocess_all(self):
        """
        Preprocess all raw stock data files in the raw data directory.

        :return: List of paths to preprocessed files.
        """
        preprocessed_files = []
        for file_name in os.listdir(self.raw_data_dir):
            if file_name.endswith(".csv"):
                csv_file_path = os.path.join(self.raw_data_dir, file_name)
                processed_file = self.preprocess_file(csv_file_path)
                if processed_file:
                    preprocessed_files.append(processed_file)
        return preprocessed_files

class StockFilter:
    def __init__(self, file_path):
        self.output_file = file_path
        self.lookback_days = 3
        self.filtered_data = None

    def filter_and_sort_data(self):
        print("Executing filter_and_sort_data in StockFilter")
        if not os.path.exists(self.output_file):
            raise FileNotFoundError(f"The file '{self.output_file}' does not exist.")
        
        data = pd.read_csv(self.output_file, sep=",")  # Adjust delimiter if necessary
        print("Columns in the dataset:", data.columns.tolist())
        
        # Ensure 'Last Signal Date' exists
        if 'Last Signal Date' not in data.columns:
            raise KeyError("'Last Signal Date' column is missing from the dataset.")
        
        data['Last Signal Date'] = pd.to_datetime(data['Last Signal Date'], errors='coerce')
        data = data.dropna(subset=['Last Signal Date'])

        cutoff_date = datetime.now() - timedelta(days=self.lookback_days)
        print(f"Cutoff Date: {cutoff_date}")

        filtered = data[data['Last Signal Date'] >= cutoff_date]
        if filtered.empty:
            print("No rows match the filtering criteria.")
        else:
            print("Filtered Rows:")
            print(filtered)

        self.filtered_data = filtered.sort_values(by='Stock Symbol').reset_index(drop=True)

    def save_filtered_data(self):
        if self.filtered_data is None:
            raise ValueError("No filtered data to save. Run 'filter_and_sort_data' first.")
        self.filtered_data.to_csv(self.output_file, sep=",", index=False)
        print(f"Filtered data saved to {self.output_file}.")



