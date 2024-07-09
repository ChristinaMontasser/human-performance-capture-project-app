#This file handles interactions with Docker

import docker, json
import os 
from flask import  current_app
from utils.helpers import copy_files
client = docker.from_env()

def get_command(model):
    #!! Write a logic that returns the expected command from the model name and type of the uploaded data we will select the command 
    #We have common format:
    # model-name_datatype_command e.g. "4d-human_video_command", "4d-human_image_command"
    # So, split model name, + check sent data that's now save in the file video or image, + command word  
    return 'python track.py video.source="example_data/videos/gymnasts.mp4"'
     
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
    json_file = os.path.abspath(os.path.join(current_dir, '..', '..', '..', 'models', 'model_container_names.json'))
    # Load JSON data from the file
    if os.path.exists(json_file):
        with open(json_file, 'r') as f:
            image_container_mapping = json.load(f)
    else:
        raise FileNotFoundError(f"JSON file '{json_file}' does not exist.")
    return image_container_mapping

def get_container_name(image_container_mapping, image_name): 
    container_name = None
    for key, value in image_container_mapping.items():
        if key == image_name:
            container_name = value
    return container_name

def run_container_existing_image(image_name, volumes):
    container = client.containers.run(image_name, name=image_name.split(':')[0]+'1', detach=True)
    
    # return {'container_id':container.id, 
    #         'container_name': container.name}
    return container

def run_container_new_image(image_name, volumes):
    container = client.containers.run(image_name, name=image_name, detach=True)
    # return {'container_id':container.id, 
    #                 'container_name': container.name}
    return container

def get_image_docker_file(image_name):
    current_dir = os.path.dirname(__file__)
    os.path.abspath(os.path.join(current_dir, '..', '..', '..', 'models', 'model_container_names.json'))
    model_folder = os.path.join(os.getcwd(), '..', '..', '..', 'models', image_name )
   # print(model_folder)
    dockerfile_path = os.path.join(model_folder, 'Dockerfile')
    return dockerfile_path, model_folder

def build_image(image_name, model_folder):
    image, _ = client.images.build(path=model_folder, tag=image_name)
    return image

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

def run_command_in_container(container_name, command):    
    try:
        container = client.containers.get(container_name)
        container.exec_run("apt-get install libgl1-mesa-dev")
        exec_log = container.exec_run(command)
        print(exec_log.output.decode())
    except docker.errors.NotFound:
        print(f"Container {container_name} not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

def check_image_container(image_name):
    volumes = {
        os.path.abspath(current_app.config['UPLOAD_FOLDER']): {'bind': '/app/data/input_image', 'mode': 'ro'},
        os.path.abspath(current_app.config['OUTPUT_FOLDER']): {'bind': '/app/data/output', 'mode': 'rw'}
    }
    #Get model_container names from json file
    image_container_mapping = load_model_container_mapping()
    # Check if the container exists in the JSON mapping
    # We have to check that the existing container has been run with a volume whose directories as defined above, otherwise delete it 
    container_name = get_container_name(image_container_mapping, image_name)
    #There is no container with this name, we will create one based on the image 
    #We have to make sure that the created container has volume folders 
    if container_name == "" or container_name== None:
        # connect to docker server 
        # If the image exists but the container doesn't, create a new container
        if image_name in image_container_mapping.keys():
            return run_container_existing_image(image_name, volumes)
        else:
            dockerfile_path, model_folder = get_image_docker_file(image_name)
            #Build an image and run container 
            if os.path.exists(dockerfile_path):
                # Build the image
                image, _ = build_image(image_name, model_folder)
                # Create a new container from the built image
                return run_container_new_image(image.name, volumes)
            else:
                # If neither model nor container exists and no Dockerfile is found
                raise ValueError(f"No container or Dockerfile found for model: {image_name}")
    else:
        container = client.containers.get(container_name)
        is_matched = inspect_container_volumes(container, volumes=volumes)
        if (is_matched):
            return container
        else:
           #We have to delete the old one and create a new container because it doesn't bind with the data folder 
           #And docker doesn't support to update the container to bind a volume 
            delete_existing_container(container_name)
            return run_container_existing_image(image_name, volumes)


def run_docker_container(model, save_to_folder, extensions=['.npz', '.png']):
   
    #!! match  both the model name sent by frontend and the one that's in json file 
    container = check_image_container(model)

    if container.status != 'running':
        container.start()
    command = get_command(model)
    run_command_in_container('4d-video-v9', command)
    #Now we have to send the output that's in output folder to the 'Save To' folder
    #copy from one data/outputs to the save_to_folder
    #copy based on preference result, npz. overlayed image or both, create filter function that filters the copied files based on its extention 
    copy_files(current_app.config['OUTPUT_FOLDER'], save_to_folder, extensions)
    return True
