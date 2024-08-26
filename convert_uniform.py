# # import pickle
# # import joblib, torch
# # import numpy as np
# # from scipy.spatial.transform import Rotation as R

# # class Human4D_Postprocessing():
import os 
# # def cam_crop_to_full(cam_bbox, box_center, box_size, img_size, focal_length=5000.):
# #     # Convert cam_bbox to full image
# #     img_w, img_h = img_size[:, 0], img_size[:, 1]
# #     cx, cy, b = box_center[:, 0], box_center[:, 1], box_size
# #     # print("Shape of cam_bbox:", cam_bbox.shape)
# #     # print("Shape of box_center:", box_center.shape)
# #     # print("Shape of box_size:", box_size.shape)
# #     # print("Shape of img_size:", img_size.shape)
# #     w_2, h_2 = img_w / 2., img_h / 2.
# #     bs = b * cam_bbox[:, 0] + 1e-9
# #     tz = 2 * focal_length / bs
# #     tx = (2 * (cx - w_2) / bs) + cam_bbox[:, 1]
# #     ty = (2 * (cy - h_2) / bs) + cam_bbox[:, 2]
# #     full_cam = torch.stack([tx, ty, tz], dim=-1)
# #     #print(full_cam.shape)
# #     return full_cam


# # def map_to_cam_params(data):
# #     """
# #     Maps variables from the input dictionary to parameters used in the cam_crop_to_full function.

# #     :param data: Dictionary containing all input data for a single frame.
# #     :return: Tuple of parameters (cam_bbox, box_center, box_size, img_size)
# #     """
    
# #     # Extract cam_bbox from the data dictionary (camera translation wrt bbox)
# #     cam_bbox = torch.tensor(data.get('camera_bbox', []), dtype=torch.float32)
    
# #     # Extract box_center from the data dictionary (2D center of bbox)
# #     box_center = torch.tensor(data.get('center', []), dtype=torch.float32)
    
# #     # Extract box_size from the data dictionary (scale or bbox dimensions)
# #     box_size = torch.tensor([bbox[2] for bbox in data.get('bbox', [])], dtype=torch.float32)
    
# #     # Extract img_size from the data dictionary (image dimensions)
# #     img_size = torch.tensor(data.get('size', []), dtype=torch.float32)
    
# #     return cam_bbox, box_center, box_size, img_size


# # def convert_pkl_to_npz_4dHumans(pkl_file_path, npz_file_path):
# #     """
# #     Converts a .pkl file containing frame data into a .npz file with Translation, Pose, and Shape parameters.
    
# #     Args:
# #     - pkl_file_path (str): Path to the input .pkl file.
# #     - npz_file_path (str): Path to the output .npz file.
# #     """
# #     # Load the .pkl file
# #     with open(pkl_file_path, 'rb') as f:
# #         results = joblib.load(f)
    
# #     # Initialize lists for frames
# #     translations = []
# #     poses = [] 
# #     shapes = []

# #     # Process each frame
# #     for frame_id, frame_data in results.items():
# #         if isinstance(frame_data, dict):
# #             # Extracting parameters
# #             camera = frame_data.get('camera', [])
# #             smpl = frame_data.get('smpl', [])

# #             # Process camera translation
# #             if camera:
# #                 #The logic should be here 
# #                 cam_bbox, box_center, box_size, img_size = map_to_cam_params(frame_data)
# #                 #for i in len(cam_bbox):
# #                     #The logic should be here 
# #                 #print(img_size)
# #                 translation = cam_crop_to_full(cam_bbox, box_center, box_size, img_size, focal_length=5000.)
# #                 print(translation.shape)
# #                 if translation is not None:
# #                 # Ensure `translation` is iterable
# #                     translations.extend([np.array(translation)])
# #                 else:
# #                     raise ValueError(f"Expected `translation` to be list or array, but got {type(translation)}.")
# #             # Process SMPL parameters
# #             if smpl:
# #                 poses_smplx = [] 
# #                 shapes_smplx = []
# #                # print(len(smpl))
# #                 for smpl_params in smpl:
# #                     betas = smpl_params.get('betas', None)
# #                     if betas.size < 16:
# #                         # Calculate how much padding is needed
# #                         padding_size = 16 - betas.size
                        
# #                         # Pad the array at the end with zeros
# #                         betas = np.pad(betas, (0, padding_size), mode='constant')
# #                     # print(betas)
# #                     # print(betas.shape)
        
# #                     pose = smpl_params.get('body_pose', None)  # Extracting pose from SMPL   
# #                     # Extract global orientation (3x3)
# #                     global_orient = smpl_params.get('global_orient', None)
# #                     #print(type(pose))
# #                     if global_orient is not None and pose is not None:
# #                         # Combine global orientation and body pose
# #                         # Assuming global_orient and body_pose are numpy arrays or tensors
# #                         pose = np.concatenate((global_orient, pose), axis=0)
# #                         # Now pose has the shape (24, 3, 3) with global_orient at the start
# #                     if betas is not None:
# #                         #print(type(betas))
# #                         shapes_smplx.append(np.array(betas))
# #                     else:
# #                         raise ValueError(f"Betas are missing in SMPL parameters for frame '{frame_id}'.")
                    
# #                     if pose is not None:
# #                         poses_smplx.append(np.array(pose))
# #                     else:
# #                         raise ValueError(f"Pose is missing in SMPL parameters for frame '{frame_id}'.")
                    

# #                 shapes.append(np.array(shapes_smplx))
# #                 poses.append(np.array(poses_smplx))

# #     #print(translations)
# #     # Convert lists to numpy arrays
# #     translations = np.array(translations, dtype=np.float32)
# #     poses = np.array(poses, dtype=np.float32)
# #     shapes = np.array(shapes, dtype=np.float32)
# #     print(len(translations), len(poses), len(shapes))
# #    # Save to .npz file
# #     np.savez(npz_file_path, translation=translations, pose=poses, shape=shapes)
# #     print(f"Data successfully saved to {npz_file_path}")

# # # Example usage
# # file_path = 'pkl_files/output_cam_file_4d_smpl.npz'
# # # convert_pkl_to_npz_4dHumans(file_path, 'pkl_files/output_cam_file_4d_smpl.npz')


# # def split_npz_to_people(file_path, people_number):
# #     npz_data = np.load(file_path, allow_pickle=True)

# #     # Iterate over the 5 slices along the second dimension
# #     for i in range(people_number):
# #         # Create a dictionary to hold the data for the current slice
# #         split_data = {}
        
# #         # Extract the slice for each key
# #         for key in npz_data.files:
# #             split_data[key] = npz_data[key][:, i, ...]

# #         # Save the current slice to a new .npz file
# #         split_file_path = f'pkl_files/split_file_{i+1}.npz'
# #         np.savez(split_file_path, **split_data)

# #         print(f"Saved {split_file_path} with shapes:")
# #         for key in split_data:
# #             print(f" - {key}: {split_data[key].shape}")

# # split_npz_to_people(file_path, 5)




# # def convert_npz_pose_to_vector(file_path, output_file_path, num_of_frames=263):
# #     """
# #     Converts 'pose' data from rotation matrices to rotation vectors in an npz file,
# #     and reshapes the vectors to a flattened format.

# #     Parameters:
# #     - file_path (str): Path to the input .npz file containing pose data as rotation matrices.
# #     - output_file_path (str): Path to save the output .npz file with pose data as flattened rotation vectors.
# #     - num_of_frames (int): Number of frames to process (default is 263).

# #     Returns:
# #     - None
# #     """
# #     def matrix_to_vector(matrix):
# #         """Convert a rotation matrix to a rotation vector."""
# #         return R.from_matrix(matrix).as_rotvec()

# #     try:
# #         # Load the npz file
# #         npz_data = np.load(file_path, allow_pickle=True)
# #         new_poses_vec = []

# #         # Convert each rotation matrix to a rotation vector for each frame
# #         for i in range(num_of_frames):
# #             print(f"Processing frame {i+1}/{num_of_frames}")
# #             new_poses_vec.append(matrix_to_vector(npz_data['pose'][i]))
        
# #         # Convert to numpy array
# #         new_poses_vec = np.array(new_poses_vec)

# #         # Reshape the pose data to [num_of_frames, 24*3]
# #         new_poses_vec = new_poses_vec.reshape(num_of_frames, 24*3)

# #         # Ensure the shapes are consistent
# #         assert new_poses_vec.shape == (num_of_frames, 24*3), "Output shape should be (num_of_frames, 24*3)"

# #         # Prepare updated data dictionary
# #         updated_data = {key: npz_data[key] for key in npz_data if key != 'pose'}
# #         updated_data['pose'] = new_poses_vec

# #         # Save the updated data back to a new .npz file
# #         np.savez(output_file_path, **updated_data)
# #         print(f"Updated file saved to {output_file_path}")
    
# #     except Exception as e:
# #         print(f"An error occurred: {e}")

# # # Example usage
# # convert_npz_pose_to_vector('split_file_1.npz', 'split_file_person_1_vec_pose_flattened.npz')




# import numpy as np
# import torch
# from scipy.spatial.transform import Rotation as R
# import joblib

# class Human4D_Postprocessing:
    
#     def cam_crop_to_full(self, cam_bbox, box_center, box_size, img_size, focal_length=5000.):
#         """Convert camera parameters from cropped to full image coordinates."""
#         img_w, img_h = img_size[:, 0], img_size[:, 1]
#         cx, cy, b = box_center[:, 0], box_center[:, 1], box_size
#         w_2, h_2 = img_w / 2., img_h / 2.
#         bs = b * cam_bbox[:, 0] + 1e-9
#         tz = 2 * focal_length / bs
#         tx = (2 * (cx - w_2) / bs) + cam_bbox[:, 1]
#         ty = (2 * (cy - h_2) / bs) + cam_bbox[:, 2]
#         full_cam = torch.stack([tx, ty, tz], dim=-1)
#         return full_cam

#     def map_to_cam_params(self, data):
#         """Map dictionary data to camera parameters required for full image conversion."""
#         cam_bbox = torch.tensor(data.get('camera_bbox', []), dtype=torch.float32)
#         box_center = torch.tensor(data.get('center', []), dtype=torch.float32)
#         box_size = torch.tensor([bbox[2] for bbox in data.get('bbox', [])], dtype=torch.float32)
#         img_size = torch.tensor(data.get('size', []), dtype=torch.float32)
#         return cam_bbox, box_center, box_size, img_size

#     def convert_pkl_to_npz_4dHumans(self, pkl_file_path, npz_file_path):
#         """Convert a .pkl file to .npz format for 4D Humans data."""
#         with open(pkl_file_path, 'rb') as f:
#             results = joblib.load(f)
        
#         translations, poses, shapes = [], [], []

#         for frame_id, frame_data in results.items():
#             if isinstance(frame_data, dict):
#                 camera = frame_data.get('camera', [])
#                 smpl = frame_data.get('smpl', [])

#                 if camera:
#                     cam_bbox, box_center, box_size, img_size = self.map_to_cam_params(frame_data)
#                     translation = self.cam_crop_to_full(cam_bbox, box_center, box_size, img_size, focal_length=5000.)
#                     if translation is not None:
#                         translations.extend([np.array(translation)])
#                     else:
#                         raise ValueError(f"Expected `translation` to be list or array, but got {type(translation)}.")

#                 if smpl:
#                     poses_smplx, shapes_smplx = [], []
#                     for smpl_params in smpl:
#                         betas = smpl_params.get('betas', None)
#                         if betas.size < 16:
#                             padding_size = 16 - betas.size
#                             betas = np.pad(betas, (0, padding_size), mode='constant')

#                         pose = smpl_params.get('body_pose', None)
#                         global_orient = smpl_params.get('global_orient', None)
#                         if global_orient is not None and pose is not None:
#                             pose = np.concatenate((global_orient, pose), axis=0)
#                         if betas is not None:
#                             shapes_smplx.append(np.array(betas))
#                         else:
#                             raise ValueError(f"Betas are missing in SMPL parameters for frame '{frame_id}'.")
                        
#                         if pose is not None:
#                             poses_smplx.append(np.array(pose))
#                         else:
#                             raise ValueError(f"Pose is missing in SMPL parameters for frame '{frame_id}'.")

#                     shapes.append(np.array(shapes_smplx))
#                     poses.append(np.array(poses_smplx))

#         translations = np.array(translations, dtype=np.float32)
#         poses = np.array(poses, dtype=np.float32)
#         shapes = np.array(shapes, dtype=np.float32)
#         np.savez(npz_file_path, translation=translations, pose=poses, shape=shapes)
#         print(f"Data successfully saved to {npz_file_path}")

#     def split_npz_to_people(self, file_path):
#         """Split a .npz file into individual people data if more than one person is present."""
#         npz_data = np.load(file_path, allow_pickle=True)

#         # Determine the number of people from the second dimension of any key
#         number_of_people = npz_data['pose'].shape[1]  # Assuming 'pose' is always present and has shape [frames, people, ...]

#         if number_of_people == 1:
#             print("Only one person found in the data. No splitting required.")
#             return number_of_people # No splitting needed

#         # If more than one person, proceed with splitting
#         for i in range(number_of_people):
#             split_data = {}
#             for key in npz_data.files:
#                 split_data[key] = npz_data[key][:, i, ...]

#             split_file_path = f'pkl_files/people_npz/split_file_{i+1}.npz'
#             np.savez(split_file_path, **split_data)

#             print(f"Saved {split_file_path} with shapes:")
#             for key in split_data:
#                 print(f" - {key}: {split_data[key].shape}")
#         return number_of_people
#     def convert_npz_pose_to_vector(self, file_path, output_file_path, num_of_frames=263):
#         """Convert 'pose' data in a .npz file from rotation matrices to vectors and flatten."""
#         def matrix_to_vector(matrix):
#             return R.from_matrix(matrix).as_rotvec()

#         try:
#             npz_data = np.load(file_path, allow_pickle=True)
#             new_poses_vec = []

#             for i in range(num_of_frames):
#                 print(f"Processing frame {i+1}/{num_of_frames}")
#                 new_poses_vec.append(matrix_to_vector(npz_data['pose'][i]))
            
#             new_poses_vec = np.array(new_poses_vec)
#             new_poses_vec = new_poses_vec.reshape(num_of_frames, 24*3)
#             assert new_poses_vec.shape == (num_of_frames, 24*3), "Output shape should be (num_of_frames, 24*3)"

#             updated_data = {key: npz_data[key] for key in npz_data if key != 'pose'}
#             updated_data['pose'] = new_poses_vec

#             np.savez(output_file_path, **updated_data)
#             print(f"Updated file saved to {output_file_path}")
        
#         except Exception as e:
#             print(f"An error occurred: {e}")

#     def start_unify_pkl(self, pkl_file_path, npz_file_path, output_file_path, num_of_frames=263):
#         """
#         Perform the complete process of converting a .pkl file to .npz, 
#         splitting data if necessary, and converting poses.
        
#         Parameters:
#         - pkl_file_path (str): Path to the input .pkl file.
#         - npz_file_path (str): Path to save the converted .npz file.
#         - output_file_path (str): Path to save the final output .npz file with pose vectors.
#         - num_of_frames (int): Number of frames to process (default is 263).
        
#         Returns:
#         - None
#         """
#         print("Starting PKL to NPZ conversion...")
#         self.convert_pkl_to_npz_4dHumans(pkl_file_path, npz_file_path)
        
#         print("Checking if data needs to be split by people...")
#         number_of_people = self.split_npz_to_people(npz_file_path)
        
#         print("Converting NPZ poses to vectors...")
#         for i in range(1):  # Always run at least once, no need to split if only one person
#             split_file_path = f'pkl_files/people_npz/split_file_{i+1}.npz' if number_of_people > 1 else npz_file_path
#             self.convert_npz_pose_to_vector(split_file_path, output_file_path.format(i+1), num_of_frames)
#         print("All processes completed.")

# # Example usage
# # Create an instance of the class
# human4d = Human4D_Postprocessing()

# # # # Call the method that performs all steps
# # human4d.start_unify_pkl(
# #     pkl_file_path='pkl_files/demo_gymnasts.pkl',
# #     npz_file_path='pkl_files/output_file.npz',
# #     output_file_path='pkl_files/split_file_{}_vec_pose_flattened.npz',
# #     num_of_frames=263
# # )



# def check_last_file_dimensions(file_path):
#     """
#     Checks and prints the dimensions of all arrays in a specified .npz file.

#     Parameters:
#     - file_path (str): Path to the .npz file to be checked.

#     Returns:
#     - None
#     """
#     try:
#         # Load the npz file
#         npz_data = np.load(file_path, allow_pickle=True)
        
#         # Iterate over each key and print its shape
#         for key in npz_data.files:
#             print(f"Key: '{key}', Shape: {npz_data[key].shape}")
    
#     except Exception as e:
#         print(f"An error occurred while checking the file dimensions: {e}")

# # Example usage
# check_last_file_dimensions('pkl_files/smplx_gyman_keys_new_coordinate_one_frame.npz')



# import numpy as np

# def rename_keys_in_npz(npz_file_path, output_file_path):
#     """
#     Renames keys in a .npz file from 'translation' to 'trans', 'shape' to 'betas', and 'pose' to 'poses'.

#     Parameters:
#     - npz_file_path (str): Path to the input .npz file.
#     - output_file_path (str): Path to save the output .npz file with renamed keys.

#     Returns:
#     - None
#     """
#     # Load the data from the .npz file
#     data = np.load(npz_file_path, allow_pickle=True)
    
#     # Create a dictionary to hold the renamed data
#     renamed_data = {}
    
#     # Rename keys as specified
#     for key in data.files:
#         if key == 'translation':
#             renamed_data['trans'] = data[key]
#         elif key == 'shape':
#             renamed_data['betas'] = data[key]
#         elif key == 'pose':
#             renamed_data['poses'] = data[key]
#         else:
#             renamed_data[key] = data[key]  # Keep other keys unchanged

#     # Save the renamed data to a new .npz file
#     np.savez(output_file_path, **renamed_data)
#     print(f"Successfully renamed keys and saved to {output_file_path}")

# # Example usage
# #rename_keys_in_npz('pkl_files/smplx_gyman.npz', 'pkl_files/smplx_gyman_to_unity.npz')


# import numpy as np

# def reshape_and_reduce_data(npz_file_path, output_file_path):
#     """
#     Reshapes 'data' from (263, 184) into 'trans', 'betas', 'poses' and reduces 'betas' to (263, 10) by removing last six points.

#     Parameters:
#     - npz_file_path (str): Path to the input .npz file.
#     - output_file_path (str): Path to save the output .npz file with reshaped data.

#     Returns:
#     - None
#     """
#     # Load the data from the .npz file
#     data = np.load(npz_file_path, allow_pickle=True)
    
#     # Extract the 'data' array
#     full_data = data['data']  # Shape is (263, 184)

#     # Reshape into 'trans', 'betas', and 'poses'
#     trans = full_data[:, :3]          # Shape will be (263, 3)
#     betas = full_data[:, 3:19]        # Shape will be (263, 16)
#     poses = full_data[:, 19:]         # Shape will be (263, 165)

#     # Reduce 'betas' by removing the last six points
#     betas = betas[:, :10]             # Shape will be (263, 10)

#     # Save the reshaped data to a new .npz file
#     np.savez(output_file_path, trans=trans, betas=betas, poses=poses)
#     print(f"Successfully reshaped and reduced data, saved to {output_file_path}")

# # Example usage
# #reshape_and_reduce_data('pkl_files/smplx_gyman.npz', 'pkl_files/smplx_gyman_keys.npz')



# import numpy as np

# def extract_middle_frame_and_save(npz_file_path, output_file_path):
#     """
#     Extracts the middle frame from 'trans', 'betas', and 'poses' arrays and saves them in a new .npz file.

#     Parameters:
#     - npz_file_path (str): Path to the input .npz file.
#     - output_file_path (str): Path to save the output .npz file with the middle frame data.

#     Returns:
#     - None
#     """
#     # Load the data from the .npz file
#     data = np.load(npz_file_path, allow_pickle=True)

#     # Calculate the index of the middle frame
#     middle_index = data['trans'].shape[0] // 2

#     # Extract the middle frame for each key
#     trans_middle = data['trans'][middle_index:middle_index+1, :]  # Shape will be (1, 3)
#     betas_middle = data['betas'][middle_index, :]                 # Shape will be (10,)
#     poses_middle = data['poses'][middle_index:middle_index+1, :]  # Shape will be (1, 165)

#     # Save the extracted middle frame data to a new .npz file
#     np.savez(output_file_path, trans=trans_middle, betas=betas_middle, poses=poses_middle)
#     print(f"Successfully extracted the middle frame and saved to {output_file_path}")

# # Example usage
# #extract_middle_frame_and_save('pkl_files/smplx_gyman_keys_new_coordinate.npz', 'pkl_files/smplx_gyman_keys_new_coordinate_one_frame.npz')

# import numpy as np

# def transform_coordinates_to_new_system(npz_file_path, output_file_path):
#     """
#     Transforms the coordinate system of 'trans', 'betas', and 'poses' in a .npz file to align with:
#     X-axis upwards, Y-axis left, Z-axis downwards.

#     Parameters:
#     - npz_file_path (str): Path to the input .npz file.
#     - output_file_path (str): Path to save the output .npz file with transformed coordinates.

#     Returns:
#     - None
#     """
#     # Load the data from the .npz file
#     data = np.load(npz_file_path, allow_pickle=True)

#     # Extract the existing data
#     trans = data['trans']  # Shape: (263, 3)
#     betas = data['betas']  # Shape: (263, 10)
#     poses = data['poses']  # Shape: (263, 165)

#     # Transform the coordinates
#     # Assuming the first three elements in 'trans' represent the coordinates (x, y, z)
#     trans_transformed = np.zeros_like(trans)
#     trans_transformed[:, 0] = trans[:, 1]    # new_x = old_y
#     trans_transformed[:, 1] = trans[:, 0]    # new_y = old_x
#     trans_transformed[:, 2] = -trans[:, 2]   # new_z = -old_z

#     # Transform poses similarly
#     poses_transformed = poses.copy()
#     for i in range(0, poses.shape[1], 3):
#         x = poses[:, i+1]    # old_y becomes new_x
#         y = poses[:, i]      # old_x becomes new_y
#         z = -poses[:, i+2]   # -old_z becomes new_z
#         poses_transformed[:, i] = x
#         poses_transformed[:, i+1] = y
#         poses_transformed[:, i+2] = z

#     # Betas are shape parameters; no need to transform their coordinates
#     betas_transformed = betas.copy()  # Shape: (263, 10)

#     # Save the transformed data to a new .npz file
#     np.savez(output_file_path, trans=trans_transformed, betas=betas_transformed, poses=poses_transformed)
#     print(f"Successfully transformed coordinates and saved to {output_file_path}")

# # Example usage
# #transform_coordinates_to_new_system('pkl_files/smplx_gyman_keys.npz', 'pkl_files/smplx_gyman_keys_new_coordinate.npz')



import numpy as np
import torch
from scipy.spatial.transform import Rotation as R
import joblib

class Human4D_Postprocessing_smpl:
    def convert_global_orient_to_left_hand(self, npz_file_path, output_file_path):
        """
        Converts all 'global_orient' rotation matrices in the .npz file to a left-handed coordinate system.

        Parameters:
        - npz_file_path (str): Path to the input .npz file.
        - output_file_path (str): Path to save the output .npz file with converted 'global_orient'.

        Returns:
        - None
        """
        # Load the data from the .npz file
        data = joblib.load(npz_file_path)
        
        # Iterate over each frame in the data
        for frame_id, frame_data in data.items():
            smpl = frame_data.get('smpl', [])
            for smpl_params in smpl:
                global_orient_matrix = smpl_params.get('global_orient', None)

                if global_orient_matrix is not None:
                    if global_orient_matrix.shape != (1, 3, 3):
                        raise ValueError("The 'global_orient' matrix is not in the expected shape (1, 3, 3).")
                    
                    # Extract the rotation matrix
                    rotation_matrix = global_orient_matrix[0]

                    # Convert rotation matrix to quaternion
                    r = R.from_matrix(rotation_matrix)
                    quaternion = r.as_quat()

                    # Convert quaternion to left-handed coordinate system
                    quaternion_left_hand = np.array([quaternion[0], quaternion[1], quaternion[2], quaternion[3]])

                    # Apply a -90 degree rotation around the X-axis for left-handed conversion
                    q_x = R.from_euler('x', -90, degrees=True).as_quat()
                    r_existing = R.from_quat(quaternion_left_hand)
                    r_x = R.from_quat(q_x)
                    q_result = r_x * r_existing

                    # Transform back from quaternion to rotation matrix
                    r_from_quat_left_hand = R.from_quat(q_result.as_quat())
                    rotation_matrix_left_hand = r_from_quat_left_hand.as_matrix()

                    # Update the 'global_orient' matrix with the converted left-handed matrix
                    smpl_params['global_orient'][0] = rotation_matrix_left_hand

        # Save the updated data back to a new .npz file
        joblib.dump(data, output_file_path)
        print(f"Successfully converted 'global_orient' to left-handed coordinate system and saved to {output_file_path}")

    
    def cam_crop_to_full(self, cam_bbox, box_center, box_size, img_size, focal_length=5000.):
        """Convert camera parameters from cropped to full image coordinates."""
        img_w, img_h = img_size[:, 0], img_size[:, 1]
        cx, cy, b = box_center[:, 0], box_center[:, 1], box_size
        w_2, h_2 = img_w / 2., img_h / 2.
        bs = b * cam_bbox[:, 0] + 1e-9
        tz = 2 * focal_length / bs
        tx = (2 * (cx - w_2) / bs) + cam_bbox[:, 1]
        ty = (2 * (cy - h_2) / bs) + cam_bbox[:, 2]
        full_cam = torch.stack([tx, ty, tz], dim=-1)
        return full_cam

    def map_to_cam_params(self, data):
        """Map dictionary data to camera parameters required for full image conversion."""
        cam_bbox = torch.tensor(data.get('camera_bbox', []), dtype=torch.float32)
        box_center = torch.tensor(data.get('center', []), dtype=torch.float32)
        box_size = torch.tensor([bbox[2] for bbox in data.get('bbox', [])], dtype=torch.float32)
        img_size = torch.tensor(data.get('size', []), dtype=torch.float32)
        return cam_bbox, box_center, box_size, img_size

    def convert_pkl_to_npz_4dHumans(self, pkl_file_path, npz_file_path):
        """Convert a .pkl file to .npz format for 4D Humans data."""
        with open(pkl_file_path, 'rb') as f:
            results = joblib.load(f)
        
        translations, poses, shapes = [], [], []

        for frame_id, frame_data in results.items():
            if isinstance(frame_data, dict):
                camera = frame_data.get('camera', [])
                smpl = frame_data.get('smpl', [])

                if camera:
                    cam_bbox, box_center, box_size, img_size = self.map_to_cam_params(frame_data)
                    translation = self.cam_crop_to_full(cam_bbox, box_center, box_size, img_size, focal_length=5000.)
                    if translation is not None:
                        translations.extend([np.array(translation)])
                    else:
                        raise ValueError(f"Expected `translation` to be list or array, but got {type(translation)}.")

                if smpl:
                    poses_smplx, shapes_smplx = [], []
                    for smpl_params in smpl:
                        betas = smpl_params.get('betas', None)
                        if betas.size < 16:
                            padding_size = 16 - betas.size
                            betas = np.pad(betas, (0, padding_size), mode='constant')

                        pose = smpl_params.get('body_pose', None)
                        global_orient = smpl_params.get('global_orient', None)
                        if global_orient is not None and pose is not None:
                            pose = np.concatenate((global_orient, pose), axis=0)
                        if betas is not None:
                            shapes_smplx.append(np.array(betas))
                        else:
                            raise ValueError(f"Betas are missing in SMPL parameters for frame '{frame_id}'.")
                        
                        if pose is not None:
                            poses_smplx.append(np.array(pose))
                        else:
                            raise ValueError(f"Pose is missing in SMPL parameters for frame '{frame_id}'.")

                    shapes.append(np.array(shapes_smplx))
                    poses.append(np.array(poses_smplx))

        translations = np.array(translations, dtype=np.float32)
        poses = np.array(poses, dtype=np.float32)
        shapes = np.array(shapes, dtype=np.float32)
        np.savez(npz_file_path, translation=translations, pose=poses, shape=shapes)
        print(f"Data successfully saved to {npz_file_path}")

    def split_npz_to_people(self, file_path,  name, exe):
        """Split a .npz file into individual people data if more than one person is present."""
        npz_data = np.load(file_path, allow_pickle=True)

        # Determine the number of people from the second dimension of any key
        number_of_people = npz_data['pose'].shape[1]  # Assuming 'pose' is always present and has shape [frames, people, ...]

        if number_of_people == 1:
            print("Only one person found in the data. No splitting required.")
            return number_of_people # No splitting needed

        # If more than one person, proceed with splitting
        for i in range(number_of_people):
            split_data = {}
            for key in npz_data.files:
                split_data[key] = npz_data[key][:, i, ...]

            split_file_path = f'{name}_SMPL_{i+1}.npz'
            np.savez(split_file_path, **split_data)

            print(f"Saved {split_file_path} with shapes:")
            for key in split_data:
                print(f" - {key}: {split_data[key].shape}")
        return number_of_people
    def convert_npz_pose_to_vector(self, file_path, output_file_path, num_of_frames=263):
        """Convert 'pose' data in a .npz file from rotation matrices to vectors and flatten."""
        def matrix_to_vector(matrix):
            return R.from_matrix(matrix).as_rotvec()

        try:
            npz_data = np.load(file_path, allow_pickle=True)
            new_poses_vec = []

            for i in range(num_of_frames):
                print(f"Processing frame {i+1}/{num_of_frames}")
                new_poses_vec.append(matrix_to_vector(npz_data['pose'][i]))
            
            new_poses_vec = np.array(new_poses_vec)
            new_poses_vec = new_poses_vec.reshape(num_of_frames, 24*3)
            assert new_poses_vec.shape == (num_of_frames, 24*3), "Output shape should be (num_of_frames, 24*3)"

            updated_data = {key: npz_data[key] for key in npz_data if key != 'pose'}
            updated_data['pose'] = new_poses_vec

            np.savez(output_file_path, **updated_data)
            print(f"Updated file saved to {output_file_path}")
        
        except Exception as e:
            print(f"An error occurred: {e}")

    def start_unify_pkl(self, pkl_file_path, npz_file_path, num_of_frames=263):
        """
        Perform the complete process of converting a .pkl file to .npz, 
        splitting data if necessary, and converting poses.
        
        Parameters:
        - pkl_file_path (str): Path to the input .pkl file.
        - npz_file_path (str): Path to save the converted .npz file.
        - output_file_path (str): Path to save the final output .npz file with pose vectors.
        - num_of_frames (int): Number of frames to process (default is 263).
        
        Returns:
        - None
        """
        print("Starting PKL to NPZ conversion...")
        name, exe = os.path.splitext(npz_file_path) 
        self.convert_global_orient_to_left_hand(pkl_file_path, npz_file_path)
        self.convert_pkl_to_npz_4dHumans(npz_file_path, name+'_SMPL'+exe)
        
        print("Checking if data needs to be split by people...")
        number_of_people = self.split_npz_to_people(name+'_SMPL'+exe, name, exe)
        print(number_of_people)
        print("Converting NPZ poses to vectors...")
        
        for i in range(number_of_people):  # Always run at least once, no need to split if only one person
            split_file_path = f'{name}_SMPL_{i+1}.npz' if number_of_people > 1 else npz_file_path
            output_file_path = f'{name}_SMPL_{i+1}_posevec.npz'
            self.convert_npz_pose_to_vector(split_file_path, output_file_path, num_of_frames)
        print("All processes completed.")

# # Example usage
# # Create an instance of the class
human4d = Human4D_Postprocessing_smpl()

# Call the method that performs all steps
# human4d.start_unify_pkl(
#     pkl_file_path='tmp/demo_gymnasts.pkl',
#     npz_file_path='tmp/gymnasts_new_coordinate.npz',
#     num_of_frames=263
# )



def check_last_file_dimensions(file_path):
    """
    Checks and prints the dimensions of all arrays in a specified .npz file.

    Parameters:
    - file_path (str): Path to the .npz file to be checked.

    Returns:
    - None
    """
    try:
        # Load the npz file
        npz_data = np.load(file_path, allow_pickle=True)
        
        # Iterate over each key and print its shape
        for key in npz_data.files:
            print(f"Key: '{key}', Shape: {npz_data[key].shape}")
    
    except Exception as e:
        print(f"An error occurred while checking the file dimensions: {e}")

# Example usage
#check_last_file_dimensions('tmp/gymnasts_new_coordinate_SMPL_1_posevec.npz')

import numpy as np
import joblib
from scipy.spatial.transform import Rotation as R

class Human4D_Postprocessing_smplx:
    
    def rename_keys_in_npz(self, npz_file_path, output_file_path):
        """
        Renames keys in a .npz file from 'translation' to 'trans', 'shape' to 'betas', and 'pose' to 'poses'.

        Parameters:
        - npz_file_path (str): Path to the input .npz file.
        - output_file_path (str): Path to save the output .npz file with renamed keys.

        Returns:
        - None
        """
        # Load the data from the .npz file
        data = np.load(npz_file_path, allow_pickle=True)
        
        # Create a dictionary to hold the renamed data
        renamed_data = {}
        
        # Rename keys as specified
        for key in data.files:
            if key == 'translation':
                renamed_data['trans'] = data[key]
            elif key == 'shape':
                renamed_data['betas'] = data[key]
            elif key == 'pose':
                renamed_data['poses'] = data[key]
            else:
                renamed_data[key] = data[key]  # Keep other keys unchanged

        # Save the renamed data to a new .npz file
        np.savez(output_file_path, **renamed_data)
        print(f"Successfully renamed keys and saved to {output_file_path}")

    def reshape_and_reduce_data(self, npz_file_path, output_file_path):
        """
        Reshapes 'data' from (263, 184) into 'trans', 'betas', 'poses' and reduces 'betas' to (263, 10) by removing the last six points.

        Parameters:
        - npz_file_path (str): Path to the input .npz file.
        - output_file_path (str): Path to save the output .npz file with reshaped data.

        Returns:
        - None
        """
        # Load the data from the .npz file
        data = np.load(npz_file_path, allow_pickle=True)
        
        # Extract the 'data' array
        full_data = data['data']  # Shape is (263, 184)

        # Reshape into 'trans', 'betas', and 'poses'
        trans = full_data[:, :3]          # Shape will be (263, 3)
        betas = full_data[:, 3:19]        # Shape will be (263, 16)
        poses = full_data[:, 19:]         # Shape will be (263, 165)

        # Reduce 'betas' by removing the last six points
        betas = betas[:, :10]             # Shape will be (263, 10)

        # Save the reshaped data to a new .npz file
        np.savez(output_file_path, trans=trans, betas=betas, poses=poses)
        print(f"Successfully reshaped and reduced data, saved to {output_file_path}")

    def extract_middle_frame_and_save(self, npz_file_path, output_file_path):
        """
        Extracts the middle frame from 'trans', 'betas', and 'poses' arrays and saves them in a new .npz file.

        Parameters:
        - npz_file_path (str): Path to the input .npz file.
        - output_file_path (str): Path to save the output .npz file with the middle frame data.

        Returns:
        - None
        """
        # Load the data from the .npz file
        data = np.load(npz_file_path, allow_pickle=True)

        # Calculate the index of the middle frame
        middle_index = data['trans'].shape[0] // 2

        # Extract the middle frame for each key
        trans_middle = data['trans'][middle_index:middle_index+1, :]  # Shape will be (1, 3)
        betas_middle = data['betas'][middle_index, :]                 # Shape will be (10,)
        poses_middle = data['poses'][middle_index:middle_index+1, :]  # Shape will be (1, 165)

        # Save the extracted middle frame data to a new .npz file
        np.savez(output_file_path, trans=trans_middle, betas=betas_middle, poses=poses_middle)
        print(f"Successfully extracted the middle frame and saved to {output_file_path}")

    def start_process_smplx_to_unity(self, input_file):
        # Rename keys in a .npz file
        #self.rename_keys_in_npz('input_file, 'pkl_files_LH/smplx_gyman_to_unity.npz')
        name, exe = os.path.splitext(input_file)   
        # Reshape and reduce data
        self.reshape_and_reduce_data(input_file, f'{name}_unity_keys_{exe}')

        # Extract middle frame and save
        self.extract_middle_frame_and_save(f'{name}_unity_keys_{exe}', f'{name}_unity_keys_one_frame_{exe}')


# Example usage:
# Create an instance of the class
processor = Human4D_Postprocessing_smplx()

processor.start_process_smplx_to_unity('tmp/gymnasts_new_coordinate_SMPLX_1_posevec.npz')

# Convert global orient to left-handed coordinate system
# processor.convert_global_orient_to_left_hand('your_input_file.npz', 'your_output_file.npz')


# ###AFTER The conversion 
# import numpy as np
# class Human4D_Postprocessing_smplx:
# def rename_keys_in_npz(npz_file_path, output_file_path):
#     """
#     Renames keys in a .npz file from 'translation' to 'trans', 'shape' to 'betas', and 'pose' to 'poses'.

#     Parameters:
#     - npz_file_path (str): Path to the input .npz file.
#     - output_file_path (str): Path to save the output .npz file with renamed keys.

#     Returns:
#     - None
#     """
#     # Load the data from the .npz file
#     data = np.load(npz_file_path, allow_pickle=True)
    
#     # Create a dictionary to hold the renamed data
#     renamed_data = {}
    
#     # Rename keys as specified
#     for key in data.files:
#         if key == 'translation':
#             renamed_data['trans'] = data[key]
#         elif key == 'shape':
#             renamed_data['betas'] = data[key]
#         elif key == 'pose':
#             renamed_data['poses'] = data[key]
#         else:
#             renamed_data[key] = data[key]  # Keep other keys unchanged

#     # Save the renamed data to a new .npz file
#     np.savez(output_file_path, **renamed_data)
#     print(f"Successfully renamed keys and saved to {output_file_path}")

# # Example usage
# #rename_keys_in_npz('pkl_files_LH/smplx_gyman.npz', 'pkl_files_LH/smplx_gyman_to_unity.npz')


# import numpy as np

# def reshape_and_reduce_data(npz_file_path, output_file_path):
#     """
#     Reshapes 'data' from (263, 184) into 'trans', 'betas', 'poses' and reduces 'betas' to (263, 10) by removing last six points.

#     Parameters:
#     - npz_file_path (str): Path to the input .npz file.
#     - output_file_path (str): Path to save the output .npz file with reshaped data.

#     Returns:
#     - None
#     """
#     # Load the data from the .npz file
#     data = np.load(npz_file_path, allow_pickle=True)
    
#     # Extract the 'data' array
#     full_data = data['data']  # Shape is (263, 184)

#     # Reshape into 'trans', 'betas', and 'poses'
#     trans = full_data[:, :3]          # Shape will be (263, 3)
#     betas = full_data[:, 3:19]        # Shape will be (263, 16)
#     poses = full_data[:, 19:]         # Shape will be (263, 165)

#     # Reduce 'betas' by removing the last six points
#     betas = betas[:, :10]             # Shape will be (263, 10)

#     # Save the reshaped data to a new .npz file
#     np.savez(output_file_path, trans=trans, betas=betas, poses=poses)
#     print(f"Successfully reshaped and reduced data, saved to {output_file_path}")

# # Example usage
# #reshape_and_reduce_data('pkl_files_LH/smplx_gyman.npz', 'pkl_files_LH/smplx_gyman_keys.npz')



# import numpy as np

# def extract_middle_frame_and_save(npz_file_path, output_file_path):
#     """
#     Extracts the middle frame from 'trans', 'betas', and 'poses' arrays and saves them in a new .npz file.

#     Parameters:
#     - npz_file_path (str): Path to the input .npz file.
#     - output_file_path (str): Path to save the output .npz file with the middle frame data.

#     Returns:
#     - None
#     """
#     # Load the data from the .npz file
#     data = np.load(npz_file_path, allow_pickle=True)

#     # Calculate the index of the middle frame
#     middle_index = data['trans'].shape[0] // 2

#     # Extract the middle frame for each key
#     trans_middle = data['trans'][middle_index:middle_index+1, :]  # Shape will be (1, 3)
#     betas_middle = data['betas'][middle_index, :]                 # Shape will be (10,)
#     poses_middle = data['poses'][middle_index:middle_index+1, :]  # Shape will be (1, 165)

#     # Save the extracted middle frame data to a new .npz file
#     np.savez(output_file_path, trans=trans_middle, betas=betas_middle, poses=poses_middle)
#     print(f"Successfully extracted the middle frame and saved to {output_file_path}")

# # Example usage
# extract_middle_frame_and_save('pkl_files_LH/smplx_gyman_keys.npz', 'pkl_files_LH/smplx_gyman_keys_LH_one_frame.npz')

# # import numpy as np

# # def transform_coordinates_to_new_system(npz_file_path, output_file_path):
# #     """
# #     Transforms the coordinate system of 'trans', 'betas', and 'poses' in a .npz file to align with:
# #     X-axis upwards, Y-axis left, Z-axis downwards.

# #     Parameters:
# #     - npz_file_path (str): Path to the input .npz file.
# #     - output_file_path (str): Path to save the output .npz file with transformed coordinates.

# #     Returns:
# #     - None
# #     """
# #     # Load the data from the .npz file
# #     data = np.load(npz_file_path, allow_pickle=True)

# #     # Extract the existing data
# #     trans = data['trans']  # Shape: (263, 3)
# #     betas = data['betas']  # Shape: (263, 10)
# #     poses = data['poses']  # Shape: (263, 165)

# #     # Transform the coordinates
# #     # Assuming the first three elements in 'trans' represent the coordinates (x, y, z)
# #     trans_transformed = np.zeros_like(trans)
# #     trans_transformed[:, 0] = trans[:, 1]    # new_x = old_y
# #     trans_transformed[:, 1] = trans[:, 0]    # new_y = old_x
# #     trans_transformed[:, 2] = -trans[:, 2]   # new_z = -old_z

# #     # Transform poses similarly
# #     poses_transformed = poses.copy()
# #     for i in range(0, poses.shape[1], 3):
# #         x = poses[:, i+1]    # old_y becomes new_x
# #         y = poses[:, i]      # old_x becomes new_y
# #         z = -poses[:, i+2]   # -old_z becomes new_z
# #         poses_transformed[:, i] = x
# #         poses_transformed[:, i+1] = y
# #         poses_transformed[:, i+2] = z

# #     # Betas are shape parameters; no need to transform their coordinates
# #     betas_transformed = betas.copy()  # Shape: (263, 10)

# #     # Save the transformed data to a new .npz file
# #     np.savez(output_file_path, trans=trans_transformed, betas=betas_transformed, poses=poses_transformed)
# #     print(f"Successfully transformed coordinates and saved to {output_file_path}")

# # # Example usage
# # #transform_coordinates_to_new_system('pkl_files/smplx_gyman_keys.npz', 'pkl_files/smplx_gyman_keys_new_coordinate.npz')
