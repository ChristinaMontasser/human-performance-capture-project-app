FROM nvidia/cuda:12.4.1-cudnn-runtime-ubuntu20.04

WORKDIR /workspace

RUN apt-get update && \
    apt-get install -y apt-transport-https ca-certificates curl gnupg && \
    curl -fsSL https://developer.download.nvidia.com/compute/cuda/repos/ubuntu1804/x86_64/3bf863cc.pub | apt-key add - && \
    curl -fsSL https://developer.download.nvidia.com/compute/machine-learning/repos/ubuntu1804/x86_64/7fa2af80.pub | apt-key add - && \
    apt-get update && \
    apt-get install -y tzdata

ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=Europe/Berlin    

RUN apt install -y python3.8 python3.8-dev python3.8-venv python3-pip pip git libgl1-mesa-glx libglib2.0-0 libegl1-mesa libegl1

RUN ln -s /usr/bin/python3.8 /usr/bin/python

COPY expose /workspace/expose

WORKDIR /workspace/expose

RUN pip install -r requirements.txt

RUN pip install torchvision==0.9.1

RUN mkdir -p /workspace/data/input /workspace/data/output
