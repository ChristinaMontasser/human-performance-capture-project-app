import joblib
import numpy as np

# Load the file using joblib
file_path = '/content/image04.pkl'
data = joblib.load(file_path)

# Function to inspect the structure and dimensions of each field in the data
def inspect_data_dimensions(data):
    structure = {}

    if isinstance(data, dict):
        # Assuming data is a dictionary that might contain dictionaries or arrays
        for key, value in data.items():
            if isinstance(value, dict):
                structure[key] = {}
                for subkey, subvalue in value.items():
                    if isinstance(subvalue, np.ndarray):
                        structure[key][subkey] = subvalue.shape
                    else:
                        structure[key][subkey] = type(subvalue).__name__
            elif isinstance(value, np.ndarray):
                structure[key] = value.shape
            else:
                structure[key] = type(value).__name__
    elif isinstance(data, np.ndarray):
        # Handle case where data is directly an array
        structure['root'] = data.shape
    else:
        structure['root'] = type(data).__name__

    return structure

# Inspect the dimensions of the data for all keys
data_dimensions = inspect_data_dimensions(data)

# Print the structure and dimensions
for key, value in data_dimensions.items():
    if isinstance(value, dict):
        print(f"\nKey: {key}")
        for subkey, dim in value.items():
            print(f"Field: {subkey}, Dimensions/Type: {dim}")
    else:
        print(f"Key: {key}, Dimensions/Type: {value}")
