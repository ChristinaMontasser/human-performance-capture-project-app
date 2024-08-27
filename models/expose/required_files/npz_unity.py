import numpy as np
from scipy.spatial.transform import Rotation as R
import os
import argparse


def swap_y_and_z(trans_array):
    """
    Swap the Y and Z components of the translation vector for all frames.
    """
    # Create a new array for the swapped data
    trans_swapped = np.copy(trans_array)

    # Swap Y and Z
    trans_swapped[:, [1, 2]] = trans_swapped[:, [2, 1]]

    return trans_swapped


def convert_poses_to_left_hand(npz_file_path, output_folder):
    # 加载 npz 文件
    data = np.load(npz_file_path, allow_pickle=True)

    # 提取 poses 数组
    if 'poses' not in data:
        raise ValueError("The provided .npz file does not contain 'poses'.")

    poses = data['poses']
    trans = data['trans']
    swapped_trans = swap_y_and_z(trans)

    # 检查 poses 的形状
    if poses.shape[1] < 3:
        raise ValueError("The 'poses' array does not contain enough data (at least 3 elements per frame).")

    # 初始化保存转换后旋转向量的数组
    converted_rotation_vectors = []

    # 遍历每一帧
    for pose in poses:
        # 提取前三个浮点数作为 rotation vector
        rotation_vector = pose[:3]

        # 将 rotation vector 转换为四元数
        r = R.from_rotvec(rotation_vector)
        quaternion = r.as_quat()

        # 从右手坐标系转换到左手坐标系 (反转 y, z 分量)
        quaternion_left_hand = np.array([quaternion[0], quaternion[1], quaternion[2], quaternion[3]])

        q_x = R.from_euler('x', -90, degrees=True).as_quat()
        r_existing = R.from_quat(quaternion_left_hand)
        r_x = R.from_quat(q_x)
        q_result = r_x * r_existing

        # 将转换后的四元数转换回旋转向量
        r_from_quat_left_hand = R.from_quat(q_result.as_quat())
        rotation_vector_left_hand = r_from_quat_left_hand.as_rotvec()

        # 更新该帧的前三个值为新的旋转向量
        pose[:3] = rotation_vector_left_hand

    # 保存更新后的 poses 数组到一个新的 npz 文件
    data_dict = dict(data)  # 转换为字典以便修改
    data_dict['poses'] = poses
    data_dict['trans'] = swapped_trans

    # 确保输出文件夹存在
    os.makedirs(output_folder, exist_ok=True)

    output_file_name = os.path.basename(npz_file_path).replace('.npz', '_left_hand_updated.npz')
    output_path = os.path.join(output_folder, output_file_name)
    np.savez(output_path, **data_dict, allow_pickle=True)

    print(f"Updated .npz file saved as: {output_path}")


def process_folder(input_folder, output_folder):
    # 遍历输入文件夹中的所有 .npz 文件
    for file_name in os.listdir(input_folder):
        if file_name.endswith('.npz'):
            file_path = os.path.join(input_folder, file_name)
            convert_poses_to_left_hand(file_path, output_folder)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert poses from right-hand to left-hand coordinate system.")
    parser.add_argument("--input-folder", type=str, required=True,
                        help="Path to the input folder containing .npz files.")
    parser.add_argument("--output-folder", type=str, required=True,
                        help="Path to the output folder where converted files will be saved.")

    args = parser.parse_args()

    process_folder(args.input_folder, args.output_folder)
