import numpy as np

# Function to load and display the contents of an npz file
def display_npz_contents(file_path):
    # Load the npz file
    with np.load(file_path) as data:
        # Iterate through each item in the file
        for key in data.files:
            print(f"Key: {key}")
            print("Data:")
            print(data[key])
            print()  # Add a blank line for better readability between entries

# Specify the path to the npz file
npz_file_path = '/content/extracted_data/all_data.npz'  # Modify this with your file path

# Call the function to display the contents
display_npz_contents(npz_file_path)
