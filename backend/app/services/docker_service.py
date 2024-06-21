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

def list_docker_containers():
    try:
        containers = client.containers.list(all=True)
        container_names = [container.name for container in containers]
        return container_names
    except docker.errors.DockerException as e:
        return {"error": str(e)}, 500
    
def start_docker_container(container_name):
    try:
        print("")
        container = client.containers.get(container_name)
        container.start()
        return {"message": f"Started container: {container_name}"}
    except docker.errors.NotFound:
        return {"error": f"Container '{container_name}' not found"}, 404
    except docker.errors.APIError as e:
        return {"error": f"Failed to start container '{container_name}': {str(e)}"}, 500
