import os, shutil
from flask import  current_app


def model_process(model, save_to_folder, output_types):
    model = model.split(':')[0]
    current_dir = os.path.dirname(__file__)
    input_path = os.path.abspath(os.path.join(current_app.config['UPLOAD_FOLDER']))
    folder_path = os.path.abspath(os.path.join(current_app.config['OUTPUT_FOLDER']))
    if "image" in output_types and "npz" in output_types:
        supported_extensions = ['.mp4', '.png', '.npz', '.pkl', '.npy']
    elif "image" in output_types:
        supported_extensions = ['.mp4', '.png']
    elif "npz" in output_types: 
        supported_extensions = ['.npz', '.pkl', '.npy']
        
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        file_name, file_extension = os.path.splitext(file_path)
        if file_extension in supported_extensions:
            shutil.move(file_path, save_to_folder)
        else:
            for filename in os.listdir(file_path):
                if filename not in ('tmp_images', 'tmp_images_output', 'img'): 
                    file = os.path.join(file_path, filename)
                    if os.path.isdir(file):
                        for filename in os.listdir(file):
                            file_path = os.path.join(file, filename)
                            file_name, file_extension = os.path.splitext(file_path)
                            shutil.move(file_path, save_to_folder)
                    else:
                        file_name, file_extension = os.path.splitext(file)
                        if file_extension in supported_extensions:
                            shutil.move(file, save_to_folder)

    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path):
            try: 
                os.remove(file_path)
                print(f"Deleted: {file_path}")
            except OSError as e:
                print(f"Error deleting {file_path}: {e}")
        elif os.path.isdir(file_path):
            try: 
                shutil.rmtree(file_path)
                print(f"Deleted: {file_path}")
            except OSError as e:
                print(f"Error deleting {file_path}: {e}")

    for filename in os.listdir(input_path):
        file_path = os.path.join(input_path, filename)
        if os.path.isfile(file_path):
            try: 
                os.remove(file_path)
                print(f"Deleted: {file_path}")
            except OSError as e:
                print(f"Error deleting {file_path}: {e}")
    print('success')
    return