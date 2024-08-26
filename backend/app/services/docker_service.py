#This file handles interactions with Docker

import docker, json
import os 
import subprocess
from flask import  current_app
from utils.helpers import copy_files
client = docker.from_env()
from docker.errors import ContainerError, ImageNotFound, APIError
import cv2
import shutil
import shlex
from  models_preprocessing.human import image_to_video, split_video_to_frames

def get_command(model, file_extension, filename): 
    current_dir = os.path.dirname(__file__)
    json_file = os.path.abspath(os.path.join(current_dir, '..', '..', '..', 'models', 'command.json'))

    # Path to the uploads folder
    if file_extension in [".jpg", ".jpeg", ".png"]:
        data_type =  "image"
    elif file_extension in [".mp4", ".avi"]:
        data_type =  "video"
    else:
        raise ValueError(f"Unsupported file extension: {file_extension}")

    # Load the JSON commands
    if os.path.exists(json_file):
        with open(json_file, 'r', encoding='utf-8') as f:
            commands = json.load(f)
    else:
        raise FileNotFoundError(f"JSON file '{json_file}' does not exist.")

    # Generate key based on model and data_type
    model = model.split(':')[0]
    key = f'{model}_{data_type}'

    # Retrieve the command and replace the placeholder
    if key in commands:
        command = commands.get(key)
        if 'FILENAME' in command:
            # Replace placeholder with actual filename
            command = command.replace('FILENAME', filename)
            print(command)
            #return command
        if 'WithoutExte' in command:
            command = command.replace('WithoutExte', os.path.splitext(filename)[0])
        
        return command  # No placeholder, use as is
    else:
        raise KeyError(f"Command not found for {key} in {json_file}")
    

def extract_frames(video_path, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    cap = cv2.VideoCapture(video_path)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    print(f'Total frames in video {video_path}: {total_frames}')

    frame_count = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frame_filename = os.path.join(output_dir, f'{os.path.splitext(os.path.basename(video_path))[0]}_frame_{frame_count:04d}.jpg')
        cv2.imwrite(frame_filename, frame)
        frame_count += 1

    cap.release()
    print(f'Total frames extracted from {video_path}: {frame_count}')

def model_process(model, save_to_folder, output_types):
    model = model.split(':')[0]
    current_dir = os.path.dirname(__file__)
    input_path = os.path.abspath(os.path.join(current_dir, '..', '..', '..', 'data','uploads'))
    folder_path = os.path.abspath(os.path.join(current_dir, '..', '..', '..', 'data','outputs'))
    if "image" in output_types and "npz" in output_types:
        supported_extensions = ['.mp4', '.png', '.npz', '.pkl']
    elif "image" in output_types:
        supported_extensions = ['.mp4', '.png']
    elif "npz" in output_types: 
        supported_extensions = ['.npz', '.pkl']
        
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        file_name, file_extension = os.path.splitext(file_path)
        if file_extension in supported_extensions:
            shutil.move(file_path, save_to_folder)
        else:
            for filename in os.listdir(file_path):
                if filename not in ('tmp_images', 'tmp_images_output'): 
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

def expose_preprocess():
    current_dir = os.path.dirname(__file__)
    folder_path = os.path.abspath(os.path.join(current_dir, '..', '..', '..', 'data','uploads'))
    for filename in os.listdir(folder_path):
        if filename.endswith(('.mp4', '.avi', '.mov')):
            video_path = os.path.join(folder_path, filename)
            extract_frames(video_path, folder_path)
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path) and filename.endswith('.mp4'):
            try: 
                os.remove(file_path)
                print(f"Deleted: {file_path}")
            except OSError as e:
                print(f"Error deleting {file_path}: {e}")
    print('The process of video has finished')
    return

def delete_files_in_directory(directory, extensions=None):
    if not os.path.exists(directory):
        print(f"Directory {directory} does not exist.")
        return
    
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path):
            if extensions:
                if any(filename.endswith(ext) for ext in extensions):
                    os.remove(file_path)
                    print(f"Deleted file: {file_path}")
            else:
                os.remove(file_path)
                print(f"Deleted file: {file_path}")


def inspect_container_volumes(container, volumes):
        mounts = container.attrs['Mounts']
        for mount in mounts:
            host_path = os.path.abspath(mount['Source'])
            container_path = mount['Destination']
            # Check if the mount matches any of the specified volumes
            for vol_host_path, vol_container_path in volumes.items():
                if host_path == vol_host_path and container_path == vol_container_path['bind']:
                    print(f"Match found: Host Path: {host_path}, Container Path: {container_path}")
                    return True 
                else:
                    print(f"No match: Host Path: {host_path}, Container Path: {container_path}")
                    return False 

def load_model_container_mapping():
    current_dir = os.path.dirname(__file__)
    json_file = os.path.abspath(os.path.join(current_dir, '..', '..', '..', 'image_container_mapping.json'))
    # Load JSON data from the file
    if os.path.exists(json_file):
        with open(json_file, 'r') as f:
            image_container_mapping = json.load(f)
    else:
        raise FileNotFoundError(f"JSON file '{json_file}' does not exist.")
    return image_container_mapping

def get_container_name(image_container_mapping, image_name): 
    container_name = None
    for key in image_container_mapping.keys():
        if key == image_name:
            container_name = image_container_mapping[key]
    return container_name

def run_container_existing_image(image_name, volumes, command_python):
    print('I run container with existing image and heres the image name')
    container = client.containers.run(
    image=image_name.split(':')[0],
    volumes=volumes,
    # name=image_name.split(':')[0] + '1',
    name=image_name.split(':')[0],
    detach=True,
    shm_size='1g',  
    device_requests=[
        docker.types.DeviceRequest(
            count=-1,
            capabilities=[['gpu']]
        )
    ],
    environment={"NVIDIA_VISIBLE_DEVICES": "all", "DISPLAY": ":0"},  # Adjust as necessary for your setup,
     command=[
        "/bin/bash", "-c", 
     command_python
    ],
    tty=True,
    stdin_open=True,
    #command=["/bin/bash", "/opt/conda/envs/4D-humans/bin/pip install phalp[all]@git+https://github.com/brjathu/PHALP.git", command_python]
    )
    container.reload()
    
    # Check container status
    if container.status != 'running':
        print(f'Error: Container {container.id} is not running. Status: {container.status}')
        logs = container.logs().decode('utf-8')
        print(f'Container logs:\n{logs}')
        raise ContainerError(container, container.status, logs, image_name, "Container failed to start")

    # Wait for the container to finish its task
    result = container.wait()
    exit_code = result['StatusCode']
    
    # Print container logs
    logs = container.logs().decode('utf-8')
    print(f'Container logs:\n{logs}')

    if exit_code != 0:
        raise ContainerError(container, exit_code, logs, image_name, "Non-zero exit code")

    
    # return {'container_id':container.id, 
    #         'container_name': container.name}
    return container

def run_container_new_image(image_name, volumes, command_python):
    container = client.containers.run(image_name, name=image_name, volumes=volumes,  runtime="gpus", environment={"gpus": "all"}, detach=True,
                                        command=command_python)

    return container

def get_image_docker_file(image_name):
    current_dir = os.path.dirname(__file__)
    os.path.abspath(os.path.join(current_dir, '..', '..', '..', 'image_container_mapping.json'))
    model_folder = os.path.abspath(os.path.join(current_dir, '..', '..', '..', 'models', image_name))
    print(model_folder)
    dockerfile_path = os.path.join(model_folder, 'Dockerfile')
    # model_folder = shlex.quote(model_folder)
    print(dockerfile_path)
    return dockerfile_path, model_folder

def build_image(image_name, model_folder, dockerfile_path):
    command = [
            'docker', 'build',
            '-t', image_name,
            '-f', dockerfile_path, 
            model_folder
        ]
    result = subprocess.run(command, capture_output=True, text=True)
    print(result.stdout)

    if result.returncode != 0:
        print(f"Error building image: {result.stderr}")
        return False
    else:
        print(f"Image {image_name} built successfully!")
        return True

def delete_existing_container(container_name):    
    try:
        # Get the container
        container = client.containers.get(container_name)
        # Stop and remove the container
        container.stop()
        container.remove()
        print(f"Container {container_name} stopped and removed.")
        current_dir = os.path.dirname(__file__)
        json_file_path = os.path.abspath(os.path.join(current_dir, '..', '..', '..', 'models', 'model_container_names.json'))
        # Update the JSON file to delete this container from its image
        if os.path.exists(json_file_path):
            with open(json_file_path, 'r') as json_file:
                image_container_mapping = json.load(json_file)
            
            # Find and remove the container from the mapping
            for image, containers in image_container_mapping.items():
                if container_name in containers:
                    containers.remove(container_name)
                    print(f"Container {container_name} removed from image {image}.")
                    break
            # Save the updated mapping back to the JSON file
            with open(json_file_path, 'w') as json_file:
                json.dump(image_container_mapping, json_file, indent=4)
            
            print("JSON file updated.")
        else:
            print(f"JSON file {json_file_path} does not exist.")
    
    except docker.errors.NotFound:
        print(f"Container {container_name} not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

def run_command_in_container(container, command):    
    try:
        container = client.containers.get(container)
        exec_log = container.exec_run('python demo.py --image-folder /workspace/data/input --exp-cfg data/conf.yaml --show=False --output-folder /workspace/data/output --save-params True --save-vis True --save-mesh True')
        print(exec_log.output.decode())
    except docker.errors.NotFound:
        print(f"Container {container} not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

def check_image_container(image_name, command):
    #Define volumes that will be bind with the cont
    volumes = {
        os.path.abspath(current_app.config['UPLOAD_FOLDER']): {'bind': '/workspace/data/input', 'mode': 'ro'},
        os.path.abspath(current_app.config['OUTPUT_FOLDER']): {'bind': '/workspace/data/output', 'mode': 'rw'}
    }
    #Get model_container names from json file
    image_container_mapping = load_model_container_mapping()
    # Check if the container exists in the JSON mapping
    # We have to check that the existing container has been run with a volume whose directories as defined above, otherwise delete it 
    container_name = get_container_name(image_container_mapping, image_name)
    # There is no container with this name, we will create one based on the image 
    # We have to make sure that the created container has volume folders 
    if container_name == "" or container_name== None or len(container_name)==0:
        # connect to docker server 
        # If the image exists but the container doesn't, create a new container
        if image_name in image_container_mapping.keys():
            return run_container_existing_image(image_name, volumes, command)
        else:
            dockerfile_path, model_folder = get_image_docker_file(image_name.split(':')[0])
            print("this is 1")
            #Build an image and run container 
            if os.path.exists(dockerfile_path):
                # Build the image
                build_image(image_name, model_folder, dockerfile_path)
                # Create a new container from the built image
                return run_container_existing_image(image_name, volumes) #run_container_existing_image
            else:
                # If neither model nor container exists and no Dockerfile is found
                raise ValueError(f"No container or Dockerfile found for model: {image_name}")
    else:
        docker_image = image_name.split(':')[0]
        found = False
        print(container_name)
        for name in container_name:
            if docker_image == name:
                delete_existing_container(docker_image)
                run_container_existing_image(image_name, volumes, command)
                found = True
                break
        if not found:
            run_container_existing_image(image_name, volumes, command)

def access_existing_container_bash(image_name, command, client):
    print('Hello Im HERE')
    volumes = {
        os.path.abspath(current_app.config['UPLOAD_FOLDER']): {'bind': '/workspace/data/input', 'mode': 'ro'},
        os.path.abspath(current_app.config['OUTPUT_FOLDER']): {'bind': '/workspace/data/output', 'mode': 'rw'}
    }
    

    #Get model_container names from json file
    image_container_mapping = load_model_container_mapping()
    container_name = get_container_name(image_container_mapping, image_name)
    # There is no container with this name, we will create one based on the image 
    # We have to make sure that the created container has volume folders 
    if container_name == "" or container_name== None or len(container_name)==0:
        # connect to docker server 
        # If the image exists but the container doesn't, create a new container
        if image_name in image_container_mapping.keys():
            
            container = client.containers.create( 
                image_name.split(':')[0],
                name=image_name.split(':')[0],
                tty=True,
                stdin_open=True,
                volumes=volumes,
                device_requests=[
                docker.types.DeviceRequest(
                        count=-1,
                        capabilities=[['gpu']]
                    )
                ],
                environment={"NVIDIA_VISIBLE_DEVICES": "all", "DISPLAY": ":0"}, 
                 # 'nvidia' runtime for GPU access
                )
            container.start()
    else:
        container = client.containers.get(container_name[0])
        if not container.status == 'running':
            container.start()
    
    print(f"Container {container.name} ({container.id}) is created and started.")
    print(command)
    # Step 2: Access the bash shell of the container and run the given command
   # Run the command inside the container's bash shell
    exec_result = container.exec_run(f"bash -c \"{command}\"", tty=True)

    # Print the output of the command
    if exec_result.exit_code == 0:
        print(exec_result.output.decode('utf-8'))
    else:
        print(f"Error running command: {exec_result.output.decode('utf-8')}")


def run_docker_container(model, save_to_folder, file_extension, output_types, filename):
    model_name = model.split(':')[0]
    if model_name == '4dhumans':
        if file_extension in [".jpg", ".jpeg", ".png"]:
            image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            filename, file_extension= image_to_video(image_path, filename)
            filename = filename +file_extension
            print(filename)
    command = get_command(model, file_extension, filename)
    supported_extensions = ['.mp4', '.avi', '.mov']
    if model_name == 'expose' and file_extension in supported_extensions: 
        expose_preprocess()

    if model_name == '4dhumans':
        access_existing_container_bash(model, command, client)
        if file_extension in [".jpg", ".jpeg", ".png"]:
            split_video_to_frames(filename)
    else:
        check_image_container(model, command)
   
    model_process(model, save_to_folder, output_types)
    return True
