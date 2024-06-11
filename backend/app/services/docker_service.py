#This file handles interactions with Docker

import docker
import os 

client = docker.from_env()

def run_docker_container(model, image_path, output_folder):
    volumes = {
        os.path.abspath(image_path): {'bind': '/app/input_image', 'mode': 'ro'},
        os.path.abspath(output_folder): {'bind': '/app/output', 'mode': 'rw'}
    }
    container = client.containers.run(model, volumes=volumes, detach=True)
    container.wait()
    output = container.logs()
    container.remove()
    return output.decode('utf-8')
