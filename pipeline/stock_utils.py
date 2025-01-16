import os
import shutil
from datetime import datetime
import config


class DataUtils:
    def __init__(self):
        self.base_dir = config.BASE_DIR
        self.data_dir = config.DATA_DIR
        self.logs_dir = config.LOGS_DIR
        self.symbols_file = config.SYMBOLS_FILE
        self.stock_post_dir = config.STOCK_POST_DIR
        self.stock_pre_dir = config.STOCK_PRE_DIR
        self.signals_dir = config.SIGNALS_DIR
        self.consolidated_output_file = config.CONSOLIDATED_OUTPUT_FILE
        self.signal_backup_folder = config.BACKUP_FOLDER

    def safe_remove_directory(self, path):
        """Remove a directory and its contents if it exists."""
        if os.path.exists(path):
            try:
                shutil.rmtree(path)
                print(f"Successfully removed directory: {path}")
            except Exception as e:
                print(f"Error removing directory {path}: {str(e)}")
        else:
            print(f"Directory does not exist: {path}")

    def delete_files_in_directory(self, path):
        """Delete all files in a directory."""
        if os.path.exists(path):
            try:
                files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
                for file in files:
                    os.remove(os.path.join(path, file))
                print(f"Deleted {len(files)} files from directory: {path}")
            except Exception as e:
                print(f"Error deleting files in directory {path}: {str(e)}")
        else:
            print(f"Directory does not exist: {path}")

    def backup_and_rename_signals(self):
        """Backup the consolidated signals file with a timestamp."""
        if not os.path.exists(self.signal_backup_folder):
            os.makedirs(self.signal_backup_folder)

        if os.path.exists(self.consolidated_output_file):
            try:
                timestamp = datetime.now().strftime('%Y%m%d_%H%M')
                backup_filename = f"consolidated_signals_{timestamp}.csv"
                backup_path = os.path.join(self.signal_backup_folder, backup_filename)
                shutil.move(self.consolidated_output_file, backup_path)
                print(f"Backup created: {backup_path}")
            except Exception as e:
                print(f"Error backing up signals file: {str(e)}")
        else:
            print(f"No consolidated output file found at: {self.consolidated_output_file}")

    def reset_signal_generator(self):
        """Reset the signal generator by cleaning up files and backing up signals."""
        self.delete_files_in_directory(self.signals_dir)
        self.backup_and_rename_signals()
