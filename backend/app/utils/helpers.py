import os
from werkzeug.utils import secure_filename
import json
import os
import docker
import cmd 
import logging, shutil
import subprocess
from flask import  current_app


def run_docker_container(image_name):
    command = f'docker run {image_name}'
    subprocess.run(command, shell=True)


def save_uploaded_file(file, upload_folder):
    filename = secure_filename(file.filename)
    file_path = os.path.join(upload_folder, filename)
    file.save(file_path)
    return file_path


# Configure logging
logging.basicConfig(level=logging.DEBUG)

def filter_files(files, extensions):
    return [f for f in files if any(f.endswith(ext) for ext in extensions)]

def copy_files(src_folder, dst_folder, extensions):
    if not os.path.exists(src_folder):
        logging.error(f"Source folder {src_folder} does not exist.")
        return

    if not os.path.exists(dst_folder):
        os.makedirs(dst_folder)
        logging.info(f"Destination folder {dst_folder} created.")
    
    try:
        for root, dirs, files in os.walk(src_folder):
            filtered_files = filter_files(files, extensions)
            for file in filtered_files:
                s = os.path.join(root, file)
                rel_path = os.path.relpath(s, src_folder)
                d = os.path.join(dst_folder, rel_path)
                dst_dir = os.path.dirname(d)
                if not os.path.exists(dst_dir):
                    os.makedirs(dst_dir)
                shutil.copy2(s, d)
                logging.info(f"Copied {s} to {d}")
        logging.info(f"Files copied from {src_folder} to {dst_folder} successfully.")
    except Exception as e:
        logging.error(f"An error occurred while copying files: {e}")



def load_model_container_mapping():
    current_dir = os.path.dirname(__file__)
    print(os.path.join(current_dir, '..', '..', 'database', 'image_container_mapping.json'))
    json_file = os.path.abspath(os.path.join(current_dir, '..', '..', '..', 'database', 'image_container_mapping.json'))
    # Load JSON data from the file
    if os.path.exists(json_file):
        with open(json_file, 'r') as f:
            image_container_mapping = json.load(f)
    else:
        raise FileNotFoundError(f"JSON file '{json_file}' does not exist.")
    return image_container_mapping
