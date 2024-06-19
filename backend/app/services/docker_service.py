#This file handles interactions with Docker

import docker
import os, request

client = docker.from_env()

#def run_docker_container(model, image_path, output_folder)
#    if run_exist_docker_container():
#        print('A container does exist')
#    else:
#        #Run new Docker container of that image 
#        run_new_docker_container()
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

#def run_exist_docker_container(model, image_path, output_folder):
#    container_id = request['container']
#    if container_id:
#        try:
#            container = client.containers.get(container_id)
#            container.start()
#            return f"Started container: {container.name} with ID: {container.id}"
#        except docker.errors.NotFound:
#            return f"Container with ID {container_id} not found.", 404
#        except docker.errors.APIError as e:
#            return f"Error: {e.explanation}", 500
#    return 0