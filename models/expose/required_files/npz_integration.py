import argparse
import numpy as np
import os
import re

def natural_sort_key(s, _nsre=re.compile(r'(\d+)')):
    return [int(text) if text.isdigit() else text.lower() for text in re.split(_nsre, s)]

def merge_npz_files(input_folder, output_folder):
    poses_list = []
    trans_list = []
    betas_list = []

    # Get sorted list of npz files using natural sort
    npz_files = sorted([f for f in os.listdir(input_folder) if f.endswith('.npz')], key=natural_sort_key)

    # Traverse the input folder and find all .npz files
    for npz_file in npz_files:
        file_path = os.path.join(input_folder, npz_file)
        if os.path.isfile(file_path):  # Ensure it is a file
            npz_data = np.load(file_path)
            poses_list.append(npz_data['poses'])
            trans_list.append(npz_data['trans'])
            betas_list.append(npz_data['betas'])

    # Concatenate all the pose and trans arrays
    all_poses = np.concatenate(poses_list, axis=0)
    all_trans = np.concatenate(trans_list, axis=0)

    # Calculate the median of betas
    all_betas = np.array(betas_list)
    median_betas = np.median(all_betas, axis=0)

    # Set mocap_frame_rate
    mocap_frame_rate = 30

    # Create the output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    # Define the output file path
    output_file_path = os.path.join(output_folder, 'merged_data.npz')

    # Save the concatenated arrays and median betas into a new npz file
    np.savez(output_file_path, poses=all_poses, trans=all_trans, betas=median_betas, mocap_frame_rate=mocap_frame_rate)
    print(f"Merged data saved to {output_file_path}")

def main():
    # Create ArgumentParser object
    parser = argparse.ArgumentParser(description="Merge poses, trans, and median betas from npz files into a single file")

    # Add --input-folder argument
    parser.add_argument('--input-folder', type=str, required=True, help='Path to the input folder')

    # Add --output-folder argument
    parser.add_argument('--output-folder', type=str, required=True, help='Path to the output folder')

    # Parse command-line arguments
    args = parser.parse_args()

    # Merge npz files in the input folder and save to the output folder
    merge_npz_files(args.input_folder, args.output_folder)

if __name__ == "__main__":
    main()
