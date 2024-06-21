#It's the interface to backend functions but it has to call Docker function 
#that we define to run Docker container 
import os
from services.docker_service import run_docker_container, list_docker_containers, start_docker_container

def run_model(model, image_path):
    output_folder = os.path.join(os.getcwd(), 'data', 'outputs')
    result = run_docker_container(model, image_path, output_folder)
    return result

'''def list_containers():
    result = list_docker_containers()
    return result'''

def start_container(container_name):
    result = start_docker_container(container_name)
    return result
