# Use NVIDIA's CUDA base image as a starting point
FROM nvidia/cuda:11.3.1-cudnn8-devel-ubuntu20.04


# Set environment variables
ENV PATH /opt/conda/bin:$PATH
ENV CUDA_HOME /usr/local/cuda
ENV LD_LIBRARY_PATH /usr/local/cuda/lib64:$LD_LIBRARY_PATH

# Prevent prompts from tzdata package
ENV DEBIAN_FRONTEND=noninteractive

# Set the timezone environment variable (replace with your desired timezone)
ENV TZ=Europe/Berlin

# Install required packages and Miniconda
RUN apt-get update && apt-get install -y \
 libgl1 \
git \
libglfw3-dev \ 
libgles2-mesa-dev \
freeglut3-dev \
    wget \
    bzip2 \
    ca-certificates \
    curl \
    build-essential \
    ninja-build \
    tzdata &&\
    ln -fs /usr/share/zoneinfo/$TZ /etc/localtime \
    && rm -rf /var/lib/apt/lists/*

# Download and install Miniconda
RUN wget --quiet https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O /tmp/miniconda.sh && \
    /bin/bash /tmp/miniconda.sh -b -p /opt/conda && \
    rm /tmp/miniconda.sh

# Copy the environment.yml file into the Docker image
COPY environment.yml /tmp/environment.yml


# Create the Conda environment with increased timeout and retry mechanism
RUN /opt/conda/bin/conda update -n base conda && \
    for i in {1..5}; do /opt/conda/bin/conda env create -f /tmp/environment.yml && break || sleep 15; done && \
    /opt/conda/bin/conda clean -a

# Activate the environment and set it as default
RUN echo "source activate 4D-humans" >> ~/.bashrc
ENV PATH /opt/conda/envs/4D-humans/bin:$PATH
RUN /opt/conda/envs/4D-humans/bin/pip install hydra-core joblib




# Set the working directory
WORKDIR /workspace

# Copy all the necessary files into the Docker image
COPY . /workspace

