#This file handles interactions with Docker

import docker
import os 
from flask import  current_app
from utils.helpers import check_image_container, set_up_docker_json_file
client = docker.from_env()

#def  docker():
    #!! Check if the model container exist or not 



def run_model_container(model):
    #Logic to check whether this model container exist or not and accordingly chooses one of the below functionalities 
    #  run_docker_container
    # start_docker_container

    #Result the image folder and send it back to front.
    pass 

def run_docker_container(model):
    container_name= check_image_container(model)
    #set_up_docker_json_file()
    volumes = {
        os.path.abspath(current_app.config['UPLOAD_FOLDER']): {'bind': '/app/data/input_image', 'mode': 'ro'},
        os.path.abspath(current_app.config['OUTPUT_FOLDER']): {'bind': '/app/data/output', 'mode': 'rw'}
    }
    #print(container_names)
        #if docker.errors.NotFound :
            #call run_docker_container()

    if container.status != 'running':
        container.start()

    #container = client.containers.run('4d-video-v9', volumes=volumes, detach=True)
        #if docker.errors.NotFound :
            #call run_docker_container()
    #container.wait()
    #output = container.logs()
    #container.remove()
    
    #return output.decode('utf-8')


'''def list_docker_containers():
    try:
        containers = client.containers.list(all=True)
        container_names = [container.name for container in containers]
        return container_names
    except docker.errors.DockerException as e:
        return {"error": str(e)}, 500'''


def start_docker_container(container_name):
    try:
        container = client.containers.get(container_name)
        #if docker.errors.NotFound :
            #call run_docker_container()

        if container.status != 'running':
            container.start()

        if container_name == "PARE":
            command = "env MESA_GL_VERSION_OVERRIDE=4.1 python scripts/demo.py --mode folder --image_folder /workspace/PARE/images --output_folder logs/demo"
        else:
            return {"error": f"No command defined for container: {container_name}"}, 400
        
        container.exec_run(command, stdout=True, stderr=True, tty=True)

        return {"message": f"Started container: {container_name}"}
    except docker.errors.NotFound:
        return {"error": f"Container '{container_name}' not found"}, 404
    except docker.errors.APIError as e:
        return {"error": f"Failed to start container '{container_name}': {str(e)}"}, 500
