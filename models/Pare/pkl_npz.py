import joblib
import numpy as np
import os

# Load data from a file
file_path = '/content/image04.pkl'  # Modify this with your file path
data = joblib.load(file_path)

# Create a directory to save the npz file
output_dir = 'extracted_data'
os.makedirs(output_dir, exist_ok=True)

# Initialize a dictionary to store all the data
all_data = {}

# Iterate over all keys in the loaded data
for key in data:
    key_data = data[key]

    # Check if key_data is a dictionary and has specific expected keys
    if isinstance(key_data, dict):
        # Extract 'pose', 'betas', and 'pred_cam' from the data if they exist
        pose = key_data.get('pose', None)
        betas = key_data.get('betas', None)
        pred_cam = key_data.get('pred_cam', None)

        # Check if all required data is present
        if pose is not None and betas is not None and pred_cam is not None:
            all_data[f'{key}_pose'] = pose
            all_data[f'{key}_betas'] = betas
            all_data[f'{key}_pred_cam'] = pred_cam
        else:
            print(f"Key {key} is missing data for pose, betas, or pred_cam and has been skipped.")
    else:
        # If key_data is not a dictionary, save it directly under its key
        all_data[key] = key_data

# Save all data into a single npz file
output_path = os.path.join(output_dir, 'all_data.npz')
np.savez(output_path, **all_data)
print(f"All data saved to {output_path}")

print("Data extraction complete.")
