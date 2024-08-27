import os
import shutil
import argparse


def move_png(source_root, target_folder):
    file_name = 'hd_overlay.png'

    if not os.path.exists(target_folder):
        os.makedirs(target_folder)

    for subdir in os.listdir(source_root):
        subdir_path = os.path.join(source_root, subdir)

        if os.path.isdir(subdir_path):
            source_file = os.path.join(subdir_path, file_name)
            if os.path.isfile(source_file):
                unique_file_name = f"{subdir}_{file_name}"
                target_file = os.path.join(target_folder, unique_file_name)

                shutil.move(source_file, target_file)
                print(f"Moved: {source_file} -> {target_file}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Move specific file from subfolders to a target folder.")
    parser.add_argument('--input-folder', type=str, required=True,
                        help="The root folder containing subfolders with files.")
    parser.add_argument('--output-folder', type=str, required=True,
                        help="The folder where the specific file should be moved to.")

    args = parser.parse_args()

    move_png(args.input_folder, args.output_folder)
