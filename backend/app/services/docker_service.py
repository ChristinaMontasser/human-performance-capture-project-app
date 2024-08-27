#This file handles interactions with Docker
import docker, json
import os 
import subprocess
from flask import  current_app
from docker.errors import ContainerError, ImageNotFound, APIError
import cv2
from  models_preprocessing.human import image_to_video, split_video_to_frames
from utils.output_processing import model_process
from utils.get_command import get_command
from utils.helpers import load_model_container_mapping

client = docker.from_env()

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



def inspect_container_volumes(container, volumes):
        
        mounts = container.attrs['Mounts']
        print(mounts)
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


def get_container_name(image_container_mapping, image_name): 
    container_name = None
    for key in image_container_mapping.keys():
        if key == image_name:
            container_name = image_container_mapping[key]
    return container_name


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


def run_command_inside_bash(container, command):
    print(command)
    # Step 2: Access the bash shell of the container and run the given command
   # Run the command inside the container's bash shell
    exec_result = container.exec_run(f"bash -c \"{command}\"", tty=True)

    # Print the output of the command
    if exec_result.exit_code == 0:
        print(exec_result.output.decode('utf-8'))
    else:
        print(f"Error running command: {exec_result.output.decode('utf-8')}")

def run_container_existing_image(image_name, volumes, command):
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
        shm_size='1g'
        )
    container.start()
    print(f"Container {container.name} ({container.id}) is created and started.")
    run_command_inside_bash(container, command)
    container.stop()
    return True
   


def check_image_container(image_name, command):
    volumes = {
        os.path.abspath(current_app.config['UPLOAD_FOLDER']): {'bind': '/workspace/data/input', 'mode': 'ro'},
        os.path.abspath(current_app.config['OUTPUT_FOLDER']): {'bind': '/workspace/data/output', 'mode': 'rw'}
    }
    #Get model_container names from json file
    image_container_mapping = load_model_container_mapping()
    # Check if the container exists in the JSON mapping
    # We have to check that the existing container has been run with a volume whose directories as defined above, otherwise delete it 
    container_name = get_container_name(image_container_mapping, image_name)
    #There is no container with this name, we will create one based on the image 
    #We have to make sure that the created container has volume folders 
    if container_name == "" or container_name== None or len(container_name)==0:
        # connect to docker server 
        # If the image exists but the container doesn't, create a new container
        if image_name in image_container_mapping.keys():
            return run_container_existing_image(image_name, volumes, command)
        else:
            dockerfile_path, model_folder = get_image_docker_file(image_name)
            #Build an image and run container 
            if os.path.exists(dockerfile_path):
                # Build the image
                image, _ = build_image(image_name, model_folder)
                # Create a new container from the built image
                return run_container_existing_image(image_name, volumes, command)
            else:
                # If neither model nor container exists and no Dockerfile is found
                raise ValueError(f"No container or Dockerfile found for model: {image_name}")
    else:
        print('Iam Found')
        container = client.containers.get(container_name[0])
        is_matched = inspect_container_volumes(container, volumes=volumes)
        if (is_matched):
            if not container.status == 'running':
                print('its not running ')
                container.start()
                #Send command directly
            run_command_inside_bash(container, command)
            container.stop()
        else:
           #We have to delete the old one and create a new container because it doesn't bind with the data folder 
           #And docker doesn't support to update the container to bind a volume 
            delete_existing_container(container_name)
            return run_container_existing_image(image_name, volumes, command)
        

def run_docker_container(model, save_to_folder, file_extension, output_types, filename):
    model_name = model.split(':')[0]
    if model_name == '4dhumans':
        if file_extension in [".jpg", ".jpeg", ".png"]:
            image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            filename, file_extension= image_to_video(image_path, filename)
            filename = filename +file_extension
    command = get_command(model, file_extension, filename)
    supported_extensions = ['.mp4', '.avi', '.mov']
    if model_name == 'expose' and file_extension in supported_extensions: 
        expose_preprocess()

    if model_name == '4dhumans' and file_extension in [".jpg", ".jpeg", ".png"]:
        split_video_to_frames(filename)

    check_image_container(model, command)
   
    model_process(model, save_to_folder, output_types)
    return True
