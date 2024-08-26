# Start from the base image
FROM pytorch/pytorch:1.7.0-cuda11.0-cudnn8-devel

# Set the timezone
ENV TZ=Europe/Berlin
ENV MESA_GL_VERSION_OVERRIDE=4.1

# Set the working directory
WORKDIR /workspace/PARE

# Copy the contents of the current directory to the working directory in the container
COPY . /workspace/PARE

# Add the NVIDIA repository GPG key
RUN apt-key adv --keyserver keyserver.ubuntu.com --recv-keys A4B469963BF863CC

# Update package lists and install necessary packages, including Python 3.8
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3.8 \
    python3.8-dev \
    python3-pip \
    libturbojpeg \
    libegl1 \
    libsm6 \
    libxrender1 \
    libgl1-mesa-glx \
    libglfw3-dev \
    libgles2-mesa-dev \
    sudo \
    libglib2.0-0 \
    wget \
    unzip \
    git \
	ffmpeg \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Ensure Python 3.8 is the default python and pip
RUN update-alternatives --install /usr/bin/python python /usr/bin/python3.8 1 \
    && update-alternatives --install /usr/bin/pip pip /usr/bin/pip3 1

RUN mkdir -p /workspace/data/input /workspace/data/output

# Install Python dependencies using pip
RUN pip install --no-cache-dir -r requirements.txt

# Convert line endings in prepare_data.sh from Windows to Unix style
RUN sed -i 's/\r$//' scripts/prepare_data.sh

# Set execute permissions for prepare_data.sh
RUN chmod +x scripts/prepare_data.sh

# Run a script to prepare data
RUN ./scripts/prepare_data.sh

# Copy the new renderer.py to the Docker image
COPY renderer.py /opt/conda/lib/python3.8/site-packages/pyrender/renderer.py

# Set the default command to start a Bash shell
CMD ["/bin/bash"]
