# import os 
from flask import  current_app

import cv2
import os 
# from services.docker_service import get_container_name, load_model_container_mapping
# import docker

# def download_phalp_lib():
#     #pip install phalp[all]@git+https://github.com/brjathu/PHALP.git
#     pass

# def access_existing_container_bash(image_name, command, client):
#     print('Hello Im HERE')
#     volumes = {
#         os.path.abspath(current_app.config['UPLOAD_FOLDER']): {'bind': '/workspace/data/input', 'mode': 'ro'},
#         os.path.abspath(current_app.config['OUTPUT_FOLDER']): {'bind': '/workspace/data/output', 'mode': 'rw'}
#     }
    

#     #Get model_container names from json file
#     image_container_mapping = load_model_container_mapping()
#     container_name = get_container_name(image_container_mapping, image_name)
#     # There is no container with this name, we will create one based on the image 
#     # We have to make sure that the created container has volume folders 
#     if container_name == "" or container_name== None or len(container_name)==0:
#         # connect to docker server 
#         # If the image exists but the container doesn't, create a new container
#         if image_name in image_container_mapping.keys():
            
#             container = client.containers.create( 
#                 image_name.split(':')[0],
#                 name=image_name.split(':')[0],
#                 tty=True,
#                 stdin_open=True,
#                 volumes=volumes,
#                 device_requests=[
#                 docker.types.DeviceRequest(
#                         count=-1,
#                         capabilities=[['gpu']]
#                     )
#                 ],
#                 environment={"NVIDIA_VISIBLE_DEVICES": "all", "DISPLAY": ":0"}, 
#                 runtime="nvidia",   # 'nvidia' runtime for GPU access
#                 )
#             container.start()
#     else:   
#         container = client.containers.get(image_name.split(':')[0])
    
    
#     print(f"Container {container.name} ({container.id}) is created and started.")

#     # Step 2: Access the bash shell of the container
#     exec_result = container.exec_run('/bin/bash', tty=True, stdin=True)

#     # Print the output (if any) from starting bash
#     print(exec_result.output.decode('utf-8'))

#     # Example: Run a command inside the container
#     exec_result = container.exec_run(command)
#     print(exec_result.output.decode('utf-8'))
#     # else:
#     #     docker_image = image_name.split(':')[0]
#     #     found = False
#     #     print(container_name)
#     #     for name in container_name:
#     #         if docker_image == name:
#     #             delete_existing_container(docker_image)
#     #             run_container_existing_image(image_name, volumes, command)
#     #             found = True
#     #             break
#     #     if not found:
#     #         run_container_existing_image(image_name, volumes, command)

from moviepy.editor import ImageClip
import os 
def image_to_video(image_path, filename):
# Load your image
    
    output_video_path= os.path.join(current_app.config['UPLOAD_FOLDER'], os.path.splitext(filename)[0]+'.mp4')
   
    # Create an ImageClip instance with your image
    clip = ImageClip(image_path, duration=2)  # duration in seconds

    # Set the video resolution if needed
    clip = clip.set_duration(25)  # 2 seconds duration for example

    # Write the video file
    clip.write_videofile(output_video_path, fps=1)  # fps can be 1 since it's a single frame
    os.remove(image_path)
    return os.path.splitext(filename)[0], '.mp4'



def split_video_to_frames(filename):
    """
    Splits a video into frames and saves them to the specified output folder.

    Parameters:
    - video_path (str): Path to the input video file.
    - output_folder (str): Path to the output folder where frames will be saved.

    Returns:
    - None
    """
    print('I am spliting the vdeo noe')
    print(filename)
    video_path= os.path.join(current_app.config['OUTPUT_FOLDER'], 'PHALP_'+ filename)
    print(video_path)
    output_folder = current_app.config['OUTPUT_FOLDER']
    print(output_folder)
    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        print('Output Folder')

    # Open the video file
    video_capture = cv2.VideoCapture(video_path)

    # # Check if the video was opened successfully
    if not video_capture.isOpened():
        print("Error: Could not open video.")
        return

    frame_count = 0

    while True:
        # Read the next frame from the video
        success, frame = video_capture.read()

        # If reading a frame was not successful, break the loop
        if not success:
            break

        # Save the current frame as a JPEG file
        frame_filename = os.path.join(output_folder, f"frame_{frame_count:04d}.png")
        cv2.imwrite(frame_filename, frame)

        # Increment the frame count
        frame_count += 1
        break

    # Release the video capture object
    video_capture.release()

    print(f"Finished splitting video into frames. {frame_count} frames saved to '{output_folder}'.")


