#It's the interface to backend functions but it has to call Docker function 
#that we define to run Docker container 
import os
from services.docker_service import run_model_container, run_docker_container



def run_model(model):
    print('I am in run moder')
    result = run_docker_container(model)
    return result

'''def list_containers():
    result = list_docker_containers()
    return result'''

def start_container(container_name):
    result = run_model_container(container_name)
    return result





#def run_model(model, image_path):
    #!! Check if the model container exist or not
  #  output_folder = os.path.join(os.getcwd(), 'data', 'outputs')
   # result = start_docker_container(model)
    #return result

