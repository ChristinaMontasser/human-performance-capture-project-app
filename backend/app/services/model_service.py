#It's the interface to backend functions but it has to call Docker function 
#that we define to run Docker container 
import os
from services.docker_service import run_docker_container



def run_model(model, save_to_folder, file_extension, output_types):
    result = run_docker_container(model, save_to_folder, file_extension, output_types)
    return result



#def run_model(model, image_path):
    #!! Check if the model container exist or not
  #  output_folder = os.path.join(os.getcwd(), 'data', 'outputs')
   # result = start_docker_container(model)
    #return result

