# Project setup

A few steps are required to test setup your local working environment.
I detail the installation process step by step :

1. Install docker
2. Setup a working python environment
3. Install Google Protocol Buffers libraries
4. Get tensorflow serving image

## Install docker

_Skip this step if you already have Docker installed on your machine_

`tensorflow-serving` is provided by google as a containerized application. We will use `Docker` to create and run our machine
learning applications containers.
 
#### On MacOS

With Homebrew

1. Install docker `brew install docker`
2. Install docker-machine `brew install docker-machine`
3. Start the docker-machine daemon `brew services start docker-machine`
4. Install virtualbox `brew install virtualbox`, you may need to grant the app permission for this step,
 in "System Preferences" -> "Security & Privacy": give permission for the installation. 
5. Create a default docker machine with `docker-machine create default --virtualbox-cpu-count 4 --virtualbox-memory 8192`
You can fine tune the machine settings but this one will be ok for our use case.
6. Set your environment variable with `eval $(docker-machine env default)`. This step is needed every time you open a new shell.


This last point is specific to our use case, we need to correctly forward the port `8501` of our container to the port `8501` of our localhost.
We need to do it only once. To do so:
```bash
vboxmanage controlvm default natpf1 "portforwarding,tcp,,8501,,8501"
``` 

#### On Linux

1.  Add Docker’s official GPG key
````bash
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
````
2.  Get the stable repository
````bash
sudo add-apt-repository \
   "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
   $(lsb_release -cs) \
   stable"
````

3. Update apt-get
````bash
sudo apt-get update
````

4. Install
````bash
sudo apt-get --yes install docker-ce=17.12.1~ce-0~ubuntu
````

## Create a Python virtualenv

using virtual environment is highly recommended to avoid polluting your python system distribution.

**Note** This project runs on `Python 3.6.5`. It has not been tested with `Python 3.7.z`.
Stick to `Python 3.6.5` if you want to be able to replicate all the results.

1. Create a python virtual environment with `venv`, name it as you wish, for example `tf_client`. 
Replace the path to your desired virtualenv accordingly.
```bash
`which python3.6` -m venv /PATH/TO/tf_client
```

2. Set your python source to be the `Python 3.6.5` virtualenv named `tf_serving` you just created:
```bash
source /PATH/TO/tf_client/bin/activate
```
**NB:** From now on, assume that every python command is run from this virtual env. 

3. Install the python packages required for the project. Run the following at the root of the project directory:
```bash
# in tensorflow-serving_sidecar/
pip install -r requirements.txt
``` 

### Install Protobuf
The Tensorflow Object Detection API uses Protobufs to configure model and training parameters. 
Before the framework can be used, the Protobuf libraries must be compiled. 

If you don't have protobuf installed on your machine, you can install it by following the following
procedure:

#### On MacOS
 1. Make sure you have `autoconf`, `automake` and `libtool` installed. Otherwise install them with brew:
 `brew install autoconf && brew install automake && brew install libtool`
 2. Download and unzip [protobuf-all-3.6.1.zip](https://github.com/protocolbuffers/protobuf/releases/download/v3.6.1/protobuf-all-3.6.1.zip)
 3. `cd` into `protobuf-all-3.6.1` and run `./autogen.sh && ./configure && make` _Note: This may take several minutes._
 4. Then run the install with `make check && make install`
 5. You can check your `protoc` path and version with `which protoc` and `protoc --version`

#### On Linux

 1. Get the .zip `wget https://github.com/protocolbuffers/protobuf/releases/download/v3.6.1/protobuf-all-3.6.1.zip`
 2. Unzip it `unzip protobuf-all-3.6.1.zip`
 3. Go to the protobuf folder `cd protobuf-3.6.1/`
 4. Install with `./configure  && make && make check && make install` _Note: This may take several minutes._
 
## Protobuf Compilation

Once the installation is complete you ca compile the protobufer librairies with `protoc`, 
it should be done by running the following command from the root directory of this project:
```bash
protoc object_detection/protos/*.proto --python_out=.
```

## Get `tensorflow-serving` docker image
Download the TensorFlow Serving Docker image
```bash
docker pull tensorflow/serving
```

We are now done with the setup and we can proceed with serving our first model.