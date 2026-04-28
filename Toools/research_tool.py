import os
import json
import pandas as pd
from utils.logger import get_logger
from langchain.tools import tool


logging = get_logger(__name__)

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "raw")

@tool
def fetch_local_data(data_type: str) -> str:
    """
    Fetches local financial data from the 'data' folder.
    
    Args:
        data_type (str): The type of data to fetch. Options are: 'bank_transactions', 'invoices', 'erp'.
        
    Returns:
        str: A string representation of the requested data (either CSV or JSON format converted to string), or an error message.
    """
    target_dir = os.path.join(DATA_DIR, data_type)
    
    logging.info(f"Fetching {data_type} from {target_dir}")


    if not os.path.exists(target_dir):
        return f"Error: Directory for '{data_type}' does not exist."
        
    files = os.listdir(target_dir)
    if not files:
        return f"Error: No data files found in '{data_type}' directory."
        
    # Read the first file in the directory
    file_path = os.path.join(target_dir, files[0])
    
    try:
        if file_path.endswith(".csv"):
            df = pd.read_csv(file_path)
            return df.to_string(index=False)
        elif file_path.endswith(".json"):
            with open(file_path, "r") as f:
                data = json.load(f)
            return json.dumps(data, indent=2)
        else:
            with open(file_path, "r") as f:
                return f.read()

        logging
    except Exception as e:
        return f"Failed to read file {files[0]}: {str(e)}"

## tool to normalize data
