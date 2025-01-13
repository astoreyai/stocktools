import os
import shutil
import fnmatch
import pandas as pd

def rename_and_move_files(src_directory, dest_directory, old_prefix, new_filename, file_extension):
    # Ensure the destination directory exists
    if not os.path.exists(dest_directory):
        os.makedirs(dest_directory)
   
    # Define the pattern to match files
    pattern = f"{old_prefix}*{file_extension}"
   
    # Iterate over files in the source directory
    for filename in os.listdir(src_directory):
        # Check if the file name matches the pattern
        if fnmatch.fnmatch(filename, pattern):
            # Construct full file paths
            src_file_path = os.path.join(src_directory, filename)
            dest_file_path = os.path.join(dest_directory, new_filename)
           
            # Rename and move the file
            shutil.move(src_file_path, dest_file_path)
            print(f"Moved: {src_file_path} -> {dest_file_path}")
            
            # Process the file to remove 5-letter symbols
            process_file(dest_file_path)
            
            # Break after the first match since we want only one file renamed and moved
            break

def process_file(file_path):
    # Read the CSV file
    df = pd.read_csv(file_path)
    
    # Remove rows where the symbol length is 5
    df = df[df['Symbol'].str.len() != 5]
    
    # Save the processed dataframe back to the same file
    df.to_csv(file_path, index=False)
    print(f"Processed file: {file_path}. Removed 5-letter symbols.")

# Example usage:
src_directory = '/home/aaron/Desktop'  # Source directory
dest_directory = '/home/aaron/Documents/stocktools_main/data/symbols'  # Destination directory
old_prefix = 'Daily'  # Old prefix
new_filename = 'tv_tickers.csv'  # New fixed filename
file_extension = '.csv'  # File extension to match

rename_and_move_files(src_directory, dest_directory, old_prefix, new_filename, file_extension)