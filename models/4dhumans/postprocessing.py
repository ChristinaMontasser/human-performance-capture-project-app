import pickle
import numpy as np
import argparse
import joblib
import torch 
import os

class Human4D_Postprocessing_smpl:
    
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

    def convert_pkl_to_npz_smpl(self, pkl_file_path, npz_file_path):
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



def pkl_to_npz(pkl_file_path, npz_file_path):
    """
    Convert a Pickle (.pkl) file to a NumPy compressed (.npz) file.

    Parameters:
    - pkl_file_path: str, the path to the input .pkl file.
    - npz_file_path: str, the path to the output .npz file.
    """
    # Load the data from the pickle file
    with open(pkl_file_path, 'rb') as pkl_file:
        data = joblib.load(pkl_file)

    
    # Check if the data is a dictionary or another structure
    if isinstance(data, dict):
        # Save the dictionary directly to .npz
        np.savez_compressed(npz_file_path, **data)
    elif isinstance(data, (list, tuple)):
        # If data is a list or tuple, save each element with a default name
        np.savez_compressed(npz_file_path, *data)
    else:
        # If data is a single numpy array or any other object, save it directly
        np.savez_compressed(npz_file_path, data=data)

    print(f"Converted {pkl_file_path} to {npz_file_path} successfully.")

if __name__ == "__main__":
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Convert a Pickle (.pkl) file to a NumPy compressed (.npz) file.")
    parser.add_argument('--input_file', type=str, required=True, help='The path to the input .pkl file.')
    parser.add_argument('--output_file', type=str, required=True, help='The path to the output .npz file.')
    args = parser.parse_args()
    name, exe = os.path.splitext(args.output_file)
    # Call the function with the command-line arguments
    pkl_to_npz(args.input_file, name+'_4dhumans_format'+exe)


    # Instantiate the class and call the method with command-line arguments
    processor = Human4D_Postprocessing_smpl()
    
    processor.convert_pkl_to_npz_smpl(args.input_file, name+'_SMPL_format'+exe)


