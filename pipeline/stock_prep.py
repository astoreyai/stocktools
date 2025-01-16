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

import os
import pandas as pd
from datetime import datetime, timedelta

class StockFilter:
    """
    A class to tally and combine stock signals within a lookback period.
    """
    def __init__(self, file_path, lookback_days=3):
        self.file_path = file_path
        self.lookback_days = lookback_days
        self.filtered_data = None

    def tally_signals(self):
        """
        Tally and combine stock signals within the lookback period, grouped by symbol and date.
        """
        if not os.path.exists(self.file_path):
            raise FileNotFoundError(f"The file '{self.file_path}' does not exist.")

        # Read data
        data = pd.read_csv(self.file_path)

        # Ensure column names are consistent (case-insensitive)
        data.columns = [col.lower() for col in data.columns]

        # Check for required columns
        required_columns = {'datetime', 'symbol', 'signal type'}
        if not required_columns.issubset(data.columns):
            raise ValueError(f"The file must contain the following columns: {required_columns}")

        # Convert 'datetime' column to datetime format
        data['datetime'] = pd.to_datetime(data['datetime'], errors='coerce')

        # Filter data within the lookback period
        cutoff_date = datetime.now() - timedelta(days=self.lookback_days)
        recent_data = data[data['datetime'] >= cutoff_date]

        if recent_data.empty:
            print("No recent signals found.")
            self.filtered_data = None
            return

        # Group data by symbol and datetime, combining signal types
        recent_data = recent_data.copy()  # Ensure recent_data is a copy
        recent_data['signal type'] = recent_data['signal type'].fillna('Unknown')
        tally = (
            recent_data.groupby(['symbol', 'datetime'])['signal type']
            .apply(lambda x: ', '.join(set(x)))  # Combine unique signal types for each symbol-date
            .reset_index(name='signals')
        )

        self.filtered_data = tally


    def save_filtered_data(self, output_file):
        """
        Save the tallied data to a file in a structured format.
        """
        if self.filtered_data is None:
            raise ValueError("No filtered data to save. Run 'tally_signals' first.")

        self.filtered_data.to_csv(output_file, index=False)
        print(f"Filtered data saved to {output_file}.")

    def display_filtered_data(self):
        """
        Display the tallied data for review.
        """
        if self.filtered_data is None:
            raise ValueError("No filtered data to display. Run 'tally_signals' first.")

        print(self.filtered_data)




