#This file handles interactions with Docker

import docker, json
import os 
from flask import  current_app
from utils.helpers import copy_files
client = docker.from_env()
from docker.errors import ContainerError, ImageNotFound, APIError

def get_command(model):
    #!! Write a logic that returns the expected command from the model name and type of the uploaded data we will select the command 
    #We have common format:
    # model-name_datatype_command e.g. "4d-human_video_command", "4d-human_image_command"
    # So, split model name, + check sent data that's now save in the file video or image, + command word  
    return 'python demo.py --image-folder /workspace/data/input --exp-cfg data/conf.yaml --show=False --output-folder /workspace/data/output --save-params True --save-vis True --save-mesh True'
     
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
    # print("I am checking the image container mapping")
    # print(image_container_mapping)
    return image_container_mapping

def get_container_name(image_container_mapping, image_name): 
    container_name = None
    # print('I get container name')
    # print(image_container_mapping)
    for key in image_container_mapping.keys():
        # print(key)
        if key == image_name:
            container_name = image_container_mapping[key]
        #     print('They are equal and i found image there')
        # print(container_name)
    return container_name

def run_container_existing_image(image_name, volumes, command_python):
    print('I run container with existing image and heres the image name')
    print(image_name)
#    container = client.containers.run(image_name.split(':')[0], volumes=volumes, name=image_name.split(':')[0]+'1' , environment={"NVIDIA_VISIBLE_DEVICES": "all"}
#, detach=True)

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
    environment={"NVIDIA_VISIBLE_DEVICES": "all"},
    command=command_python
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

def run_container_new_image(image_name, volumes):
    container = client.containers.run(image_name, name=image_name, volumes=volumes,  runtime="gpus", environment={"gpus": "all"}, detach=True)
    # return {'container_id':container.id, 
    #                 'container_name': container.name}
    return container

def get_image_docker_file(image_name):
    current_dir = os.path.dirname(__file__)
    os.path.abspath(os.path.join(current_dir, '..', '..', '..', 'image_container_mapping.json'))
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
   # print(f'image_name {image_name}')
    volumes = {
        os.path.abspath(current_app.config['UPLOAD_FOLDER']): {'bind': '/workspace/data/input', 'mode': 'ro'},
        os.path.abspath(current_app.config['OUTPUT_FOLDER']): {'bind': '/workspace/data/output', 'mode': 'rw'}
    }
    #Get model_container names from json file
    image_container_mapping = load_model_container_mapping()
    print("I am checking the image container mapping")
    print(image_container_mapping)
    # Check if the container exists in the JSON mapping
    # We have to check that the existing container has been run with a volume whose directories as defined above, otherwise delete it 
    container_name = get_container_name(image_container_mapping, image_name)
    #There is no container with this name, we will create one based on the image 
    #We have to make sure that the created container has volume folders 
    print("what is the container name")
    print(container_name)
    if container_name == "" or container_name== None or len(container_name)==0:
        # connect to docker server 
        # If the image exists but the container doesn't, create a new container
        if image_name in image_container_mapping.keys():
            print('IM HERE')
            return run_container_existing_image(image_name, volumes, command)
            print("i am done!!!!")
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
    # else:
    #     # container = client.containers.get('expose11')
    #     print("what did I get")
    #     docker_image = image_name.split(':')[0]
    #     print("docker image is this")
    #     print(docker_image)
    #     container = client.containers.get(container_name)
    #     # print("what did I get")
    #     print(container)
    #     is_matched = inspect_container_volumes(container, volumes=volumes)
    #     if (is_matched):
    #         print('Is matched')
    #         return container
    #     else:
    #        #We have to delete the old one and create a new container because it doesn't bind with the data folder 
    #        #And docker doesn't support to update the container to bind a volume 
    #         delete_existing_container(container_name)
    #         return run_container_existing_image(image_name, volumes)
    else:
        # container = client.containers.get('expose11')
        print("what did I get")
        docker_image = image_name.split(':')[0]
        print("docker image is this")
        print(docker_image)

        found = False
        for name in container_name:
            if docker_image == name:
                delete_existing_container(docker_image)
                run_container_existing_image(image_name, volumes, command)
                found = True
                break
        if not found:
            run_container_existing_image(image_name, volumes, command)


def run_docker_container(model, save_to_folder, extensions=['.npz', '.png']):
    #print(docker.__version__)
    #print('Hi')
    # #!! match  both the model name sent by frontend and the one that's in json file 
    command = get_command(model)
    container = check_image_container(model, command)


    # print('I checked the image')
    # print(container.top())
    # #instead of zero, it should be specified using the data type 
    # if container.status != 'running':
    #     print('I will start a container')
    #     container.start()
    # print('I have already get a command')
    # run_command_in_container(container, command)
    # print('I have already ran the model')



    #run_command_in_container('4d-video-v9', "python track.py video.source='example_data/videos/gymnasts.mp4'")
    
    #Now we have to send the output that's in output folder to the 'Save To' folder
    #copy from one data/outputs to the save_to_folder
    #copy based on preference result, npz. overlayed image or both, create filter function that filters the copied files based on its extention 
    #copy_files(current_app.config['OUTPUT_FOLDER'], save_to_folder, extensions)
    return True
