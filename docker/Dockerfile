FROM ubuntu:16.04
USER root
LABEL maintainer="github.com/fai555"

RUN apt-get update
RUN apt-get install -y software-properties-common
RUN add-apt-repository ppa:jonathonf/python-3.6
RUN apt-get update

RUN apt-get install -y build-essential python3.6 python3.6-dev python3-pip python3.6-venv
RUN python3.6 -m pip install pip --upgrade

# Pick up some TF dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential \
        curl \
        libfreetype6-dev \
        libpng12-dev \
        libzmq3-dev \
        pkg-config \
        rsync \
        git \
        software-properties-common \
        unzip \
        wget \
        && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*


RUN pip3 --no-cache-dir install \
        tensorflow==1.13.2

RUN pip3 --no-cache-dir install \
        Cython \
        contextlib2 \
        jupyter \
        matplotlib \
        pillow \
        lxml \
        wheel \
        pandas

RUN pip3 install "git+https://github.com/philferriere/cocoapi.git#egg=pycocotools&subdirectory=PythonAPI"
WORKDIR /app
RUN git clone https://github.com/fai555/tensorflow-serving_sidecar.git
WORKDIR /app/tensorflow-serving_sidecar
RUN pip3 install -r requirements.txt
RUN wget -O protobuf.zip https://github.com/google/protobuf/releases/download/v3.9.0/protoc-3.9.0-linux-x86_64.zip && \
    unzip protobuf.zip && \
    ./bin/protoc object_detection/protos/*.proto --python_out=.

ENV PYTHONPATH "/app/models/research:/app/models/research/slim:${PYTHONPATH}"
ENTRYPOINT ["python3.6"]