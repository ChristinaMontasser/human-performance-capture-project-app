import os
from werkzeug.utils import secure_filename
import json
import os
import docker
import cmd 
client = docker.from_env()

def exe_command(model_name):
    cmd.eun('docker run ')



import docker
import json
import subprocess
from flask import  current_app

def run_docker_container(image_name, container_name, volumes):
    # client = docker.from_env()

    # # Stop and remove the container if it exists
    # try:
    #     container = client.containers.get(container_name)
    #     container.stop()
    #     container.remove()
    # except docker.errors.NotFound:
    #     pass

    # # Prepare the volume bindings for the docker run command
    # volume_flags = ' '.join([f'-v {current_app.config['UPLOAD_FOLDER']}:{current_app.config['OUTPUT_FOLDER']}' for host_path, container_path in volumes.items()])

    # # Run the docker container with the specified volumes
    # command = f'docker run --name {container_name} {volume_flags} -d {image_name}'
    # subprocess.run(command, shell=True, check=True)
    pass
def run_docker_container(image_name):
    command = f'docker run {image_name}'
    subprocess.run(command, shell=True)

def set_up_docker_json_file():
    print('Imhere')
    
    # Connect to the Docker daemon
    client = docker.from_env()
    
    # Get all images
    images = client.images.list()
    
    # Prepare the dictionary to store image:container mapping
    image_container_mapping = {}

    # Initialize dictionary with all images
    for image in images:
        image_tags = image.tags if image.tags else [image.id]
        for tag in image_tags:
            image_container_mapping[tag] = []
    
    # Get all containers
    containers = client.containers.list(all=True)
    
    # Map images to their containers
    for container in containers:
        image = container.attrs['Config']['Image']
        container_name = container.name
        if ':' not in image:
            image += ':latest'
        if image in image_container_mapping:
            image_container_mapping[image].append(container_name)
    
    # Save the dictionary to a JSON file
    with open('image_container_mapping.json', 'w') as json_file:
        json.dump(image_container_mapping, json_file, indent=4)

    print("Image-container mapping saved to image_container_mapping.json")

def save_uploaded_file(file, upload_folder):
    filename = secure_filename(file.filename)
    file_path = os.path.join(upload_folder, filename)
    file.save(file_path)
    return file_path

def check_image_container(image_name):
    print('Check')
    #Get model_container names from json file
    current_dir = os.path.dirname(__file__)
    json_file = os.path.abspath(os.path.join(current_dir, '..', '..', '..', 'models', 'model_container_names.json'))
    # Load JSON data from the file
    if os.path.exists(json_file):
        with open(json_file, 'r') as f:
            image_container_mapping = json.load(f)
    else:
        raise FileNotFoundError(f"JSON file '{json_file}' does not exist.")

    # Check if the container exists in the JSON mapping
    container_name = None
    for key, value in image_container_mapping.items():
        if key == image_name:
            container_name = value
            #return container_name
    print(container_name)
    #There is no container with this name, we will create one based on the image 
    if container_name == "" or container_name== None:
        print('its not there')
        #connect to docker server 
        client =docker.from_env()
        # If the image exists but the container doesn't, create a new container
        if image_name in image_container_mapping.keys():
            print('trying to run it ')
            container = client.containers.run(image_name, name=image_name.split(':')[0]+'1', detach=True)
            print('theres a new container is running')
            print(container.id, container.name)
            return {'container_id':container.id, 
                    'container_name': container.name}
        else:
            print('theres no image snothere')
            # Check if there's a folder with the same model name containing a Dockerfile
            current_dir = os.path.dirname(__file__)
            os.path.abspath(os.path.join(current_dir, '..', '..', '..', 'models', 'model_container_names.json'))
            model_folder = os.path.join(os.getcwd(), '..', '..', '..', 'models', image_name )
            print(model_folder)
            dockerfile_path = os.path.join(model_folder, 'Dockerfile')
            #Build an image and run container 
            if os.path.exists(dockerfile_path):
                # Build the image
                image, _ = client.images.build(path=model_folder, tag=image_name)
                # Create a new container from the built image
                container = client.containers.run(image.id, name=image_name, detach=True)
                return {'container_id':container.id, 
                    'container_name': container.name}
            else:
                # If neither model nor container exists and no Dockerfile is found
                raise ValueError(f"No container or Dockerfile found for model: {image_name}")
    else:
        return container_name

   