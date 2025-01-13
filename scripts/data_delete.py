import os
import shutil

def safe_remove_directory(path):
    try:
        if os.path.exists(path):
            print(f"Removing directory: {path}")
            shutil.rmtree(path)
            print(f"Successfully removed: {path}")
        else:
            print(f"Directory does not exist: {path}")
    except Exception as e:
        print(f"Error removing directory {path}: {str(e)}")

def delete_files_in_directory(path):
    try:
        if os.path.exists(path):
            file_count = 0
            for filename in os.listdir(path):
                file_path = os.path.join(path, filename)
                if os.path.isfile(file_path):
                    try:
                        os.remove(file_path)
                        file_count += 1
                    except Exception as e:
                        print(f"Error deleting file {file_path}: {str(e)}")
            print(f"Successfully deleted {file_count} files from: {path}")
        else:
            print(f"Directory does not exist: {path}")
    except Exception as e:
        print(f"Error accessing directory {path}: {str(e)}")

def main():
    # Base location for directory removal
    location = r'C:\Users\aaron\OneDrive\Desktop\stocktools_main\data\stock_data'

    # Directories to remove
    directories = [
        "1hour_data",
        "30min_data",
        "15min_data",
        "1day_data",
    ]

    # Iterate through directories and remove them
    for dir_name in directories:
        path = os.path.join(location, dir_name)
        safe_remove_directory(path)

    # Path to the folder where we want to delete all files
    txt_files_path = r'C:\Users\aaron\OneDrive\Desktop\stocktools_main\scripts\txt_files'
    
    # Delete all files in the txt_files folder
    delete_files_in_directory(txt_files_path)

if __name__ == "__main__":
    main()