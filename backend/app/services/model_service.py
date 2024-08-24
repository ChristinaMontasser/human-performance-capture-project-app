#It's the interface to backend functions but it has to call Docker function 
#that we define to run Docker container 
import os
from services.docker_service import run_docker_container



def run_model(model, save_to_folder, file_extension, output_types, filename):
    result = run_docker_container(model, save_to_folder, file_extension, output_types, filename)
    return result


