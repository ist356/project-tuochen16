import os
from kaggle.api.kaggle_api_extended import KaggleApi
 
def download_kaggle_dataset(dataset_path, save_dir="cache"):
    """
    Downloads a Kaggle dataset to the specified directory and removes any unneeded files.
    """
    # Check if Superstore.xlsx already exists
    excel_file_path = os.path.join(save_dir, "Superstore.xlsx") 
    if os.path.exists(excel_file_path):
        print(f"'{excel_file_path}' already exists. Skipping download.")
        return

    # Initialize and authenticate Kaggle API
    api = KaggleApi()
    api.authenticate()

    # Create save directory if it does not exist
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    print(f"Downloading dataset {dataset_path} to {save_dir}...")
    # Download dataset and unzip it
    api.dataset_download_files(dataset_path, path=save_dir, unzip=True)

    # Remove unnecessary file Superstore.csv
    file_path = os.path.join(save_dir, "Superstore.csv")
    if os.path.exists(file_path):
        try:
            os.remove(file_path)
            print(f"Unnecessary file '{file_path}' deleted.")
        except OSError as e:
            print(f"Error deleting file '{file_path}': {e}")

    print("Download complete.")