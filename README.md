# Human Performance Capture Project

This project implemented three different machine learning methods for generating 3D human bodies in Docker container, and the application is designed for running each of them via utilizing Tkinter for the frontend and Flask for the backend

## Contents
  * [Installation of the application](#Installation-of-the-application)
    * [Set up the Docker](#set-up-the-docker)
    * [Clone the repo](#clone-the-repo)
    * [Installation of ExPose](#installation-of-expose)
    * [Installation of 4DHumans](#installation-of-4DHumans)
    * [Installation of Pare](#installation-of-Pare)
    * [Usage of the application](#usage-of-the-application)
  * [Acknowledgments](#acknowledgments)


## Installation of the application
### Set up the Docker
Download the Docker Desktop from its official website: https://www.docker.com/


1. Download Docker Desktop from its official website: https://www.docker.com/
2. Install WSL (Windows Subsystem for Linux), which allows you to run a Linux distribution
directly on Windows:
    - Open PowerShell as Administrator and run the following command:
    ```shell
        wsl --install
    ```
    - Set WSL 2 as the default version by running:
    ```shell
        wsl --set-default-version 2
    ```
3. Install a Linux distribution (e.g., Ubuntu) from the Microsoft Store. When you install
WSL, you will need to choose a Linux distribution to run.
4. Activate several Windows features, including Windows Subsystem for Linux (WSL),
Hyper-V, and optionally, Windows Sandbox.
    - Press Win + R to open the Run dialog.
    - Type optionalfeatures and press
    - Select the mentioned above features.
5. Ensure Nvidia GPU availability on your local machine:
    - Nvidia GPU Driver Installation: Verify the installation by running:
    ```shell
        nvidia-smi
    ```
    - CUDA Toolkit Installation : Check the CUDA installation by running:
    ```shell
        nvcc --version
    ```
6. Enable GPU support in Docker Desktop settings: Go to Docker Desktop settings, select
“Resources,” then “WSL Integration,” and ensure your WSL2 distributions are enabled.
7. Verify Nvidia GPU availability in your WSL environment: Open the WSL terminal and
run:
```shell
nvidia-smi
```

### Clone the repo
First, clone this repo from Github if you have been invited and have access to it because it's a private repo.
```shell
git clone https://github.com/ChristinaMontasser/human-performance-capture-project-app.git
```
Then, create a virtual environment, activate it, and install the requirements file.
```shell
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```

### Installation of ExPose
1. Clone the ExPose repository from https://github.com/vchoutas/expose and put the
whole folder into the models/expose folder that contains Dockerfile.
2. Follow the instructions of ’Preparing the data’ on the ExPose GitHub web page to get
the ’data’ folder.
3. Put the ’data’ folder in models/expose folder.
4. Finally, put all the .py files (in ’required files’) into expose folder.
5. The installation of ExPose has been done therefore it can be used via the frame.

the structure looks like this: 
```bash
models/expose
├── Dockerfile
├── data
├── expose
│   ├── other files inside the repo of ExPose
│   ├── detect_single_human.py
│   ├── frames_to_video.py
│   ├── npz_transform.py
│   ├── ... (all the files inside required_files folder)
```

### Installation of 4DHumans
1. Clone the forked repository for 4D Humans from https://github.com/ChristinaMontasser/
4D-Humans into a folder named models/4d-humans.
2. Register on the SMPLify website and navigate to the download section. After registration,
download the Code and Model zip file. Once downloaded, create a directory named
data inside your models/4d-humans folder, and place the basicModel_neutral_lbs_10_207_0_v1.0.0.
file into the models/4d-humans/data directory.
3. Clone the this repository https://github.com/ChristinaMontasser/dockerfile_script,
place the docker file and postprocessing.py in the same directory as the model,
models/4d-humans.

### Installation of Pare
1. Clone the repository: https://github.com/mkocabas/PARE.git
2. Remove the version numbers for opencv-python and setuptools in the requirements.
txt file to ensure that the latest versions of these packages are installed, promoting
access to new features.
3. To optimize rendering performance, modify the renderer.py file as follows. Change
the sample count parameter in the glRenderbufferStorageMultisample function
from 4 to 1. This adjustment is found within the OpenGL settings for the render buffer,
specifically controlling the number of samples used for multisampling, which affects
the rendering quality and performance.
4. Execute the Dockerfile.

### Usage of the application
First, activate the backend on your local host so you can send requests to the server. 
```shell
python backend/app/main.py
```
Then, run the frontend 
```shell
python frontend/main.py
```

## Acknowledgments
This frame may also provide function that can be fitted to more methods related to 3D Expressive Human Body. 
Please follow the following instructions to include your chosen model in the program:
1. Write a proper Dockerfile that works successfully with the chosen model. Note: set the
work directory as /workspace WORKDIR /workspace
2. Create a directory for the model with the model name DIR, place the Dockerfile and
the model source code there, and any post-processing scripts.
3. Include the model commands, for image or video, or both if any. While following the
mentioned database.
4. Include the model name in the JSON file.
5. Restrict the type of data, image or video, it can handle by including it in the JSON file. 