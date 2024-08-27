from flask import  current_app

import cv2
import os 


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


