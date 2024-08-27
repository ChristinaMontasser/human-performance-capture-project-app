import argparse
import numpy as np
from scipy.spatial.transform import Rotation as R
import os


# Function to convert a single rotation matrix to a rotation vector
def matrix_to_vector(matrix):
    return R.from_matrix(matrix).as_rotvec()


# Function to process npz files in the specified input folder and save to output folder
def process_npz_files(input_folder, output_folder):
    # Create output folder if it does not exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Traverse the input folder and find subfolders containing .npz files
    for item in os.listdir(input_folder):
        item_path = os.path.join(input_folder, item)
        if os.path.isdir(item_path):  # Check if it is a directory
            npz_files = [f for f in os.listdir(item_path) if f.endswith('.npz')]
            for npz_file in npz_files:
                file_path = os.path.join(item_path, npz_file)
                process_and_save_npz(file_path, output_folder)


def process_and_save_npz(file_path, output_folder):
    npz_data = np.load(file_path, allow_pickle=True)

    # Convert each pose component from rotation matrices to rotation vectors
    global_orient_vectors = matrix_to_vector(npz_data['global_orient'][0])
    body_pose_vectors = np.array([matrix_to_vector(matrix) for matrix in npz_data['body_pose']])
    jaw_pose_vectors = matrix_to_vector(npz_data['jaw_pose'][0])
    left_hand_pose_vectors = np.array([matrix_to_vector(matrix) for matrix in npz_data['left_hand_pose']])
    right_hand_pose_vectors = np.array([matrix_to_vector(matrix) for matrix in npz_data['right_hand_pose']])

    # Create zero vectors for left_eye_pose and right_eye_pose
    left_eye_pose_vectors = np.zeros(3)
    right_eye_pose_vectors = np.zeros(3)

    # Concatenate all vectors to form the 165-dimensional pose vector
    pose_vectors = np.concatenate([
        global_orient_vectors.flatten(),
        body_pose_vectors.flatten(),
        jaw_pose_vectors.flatten(),
        left_eye_pose_vectors.flatten(),
        right_eye_pose_vectors.flatten(),
        left_hand_pose_vectors.flatten(),
        right_hand_pose_vectors.flatten()
    ])

    # Extract betas and transl
    betas = npz_data['betas']
    transl = npz_data['transl']

    print("Pose vector:", pose_vectors[3:66])

    pose_vectors = pose_vectors.reshape(1, 165)
    transl = transl.reshape(1, 3)

    # Save the converted pose vectors, betas, and transl into a new npz file
    output_file_name = os.path.basename(file_path).replace('.npz', '_converted.npz')
    output_file_path = os.path.join(output_folder, output_file_name)
    np.savez(output_file_path, poses=pose_vectors, betas=betas, trans=transl)

    print(f"Converted data saved to {output_file_path}")


def main():
    # Create ArgumentParser object
    parser = argparse.ArgumentParser(
        description="Process npz files in the specified input folder and save to output folder")

    # Add --input-folder argument
    parser.add_argument('--input-folder', type=str, required=True, help='Path to the input folder')

    # Add --output-folder argument
    parser.add_argument('--output-folder', type=str, required=True, help='Path to the output folder')

    # Parse command-line arguments
    args = parser.parse_args()

    # Process npz files in the input folder and save to output folder
    process_npz_files(args.input_folder, args.output_folder)


if __name__ == "__main__":
    main()
