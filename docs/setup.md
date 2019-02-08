# Project setup

A few setup steps are required.
I detail the installation process step by step :

1. Install docker
2. Setup a working python environment
3. Install Google Protocol Buffers libraries
4. Get `tensorflow-serving` docker image
5. Download a sample object detection model for serving (_All the tutorial will use this model_)

## 1. Install docker

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
Here I use 5 CPUs because my machine has 4, adapt accordingly. Also note that `8192` Mb is enough for our model but may be insufficient for more demanding ones.  
6. Set your environment variable with `eval $(docker-machine env default)`. This step is needed every time you open a new shell.


We need to forward the port `8501` of our container to the port `8501` of our localhost to be able to make call to our prediction server on local.
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

## 2. Create a Python virtualenv

Using virtual environment is highly recommended to avoid polluting your python system distribution.

**Note** This project runs on `Python 3.6.5`. It has not been tested with `Python 3.7.z`.
Stick to `Python 3.6.5` if you want to be able to replicate all the results.

1. Create a python virtual environment with `venv`, name it as you wish, for example `tf_client`. 
Replace the path `/PATH/TO/` to your desired virtualenv accordingly.
```bash
`which python3.6` -m venv /PATH/TO/tf_client
```

2. Set your python source to be the `Python 3.6.5` virtualenv named `tf_serving` you just created:
```bash
source /PATH/TO/tf_client/bin/activate
```
**NB:** From now on, assume that every python command used in this project should be run from this virtual env. 
- Especially call to the client code `client.py`.


3. Install the python packages required for the project. Run the following at the root of the project directory:
```bash
# From tensorflow-serving_sidecar/
pip install -r requirements.txt
``` 

## 3. Install Protobuf
The Tensorflow Object Detection API uses Protobufs to configure model and training parameters. 
Before the framework can be used, the Protobuf libraries must be compiled. 

If you don't have protobuf installed on your machine, you can install it with the following
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
 
### Protobuf Compilation

Once the installation is complete you can compile the protobufer libraries of the project with `protoc`, 
it should be done by running the following command from the root directory of this project:
```bash
# From tensorflow-serving_sidecar
protoc object_detection/protos/*.proto --python_out=.
```

## 4. Get `tensorflow-serving` docker image
Download the TensorFlow Serving Docker image
```bash
docker pull tensorflow/serving
```
We will use this image to serve our model.

## 5. Download a sample model for serving

If you don't have a `savedModel.pb` ready to be served you can download several models from
[the tensorflow model zoo](https://github.com/tensorflow/models/blob/master/research/object_detection/g3doc/detection_model_zoo.md
)
In this tuto I will work with the the faster_rcnn_resnet101_coco model.

1. Download the saved model [faster_rcnn_resnet101_coco model](http://download.tensorflow.org/models/object_detection/faster_rcnn_resnet101_coco_2018_01_28.tar.gz)
2. Decompress the archive
3. Move the model folder (_e.g._ `faster_rcnn_resnet101_coco_2018_01_28`) under `tensorflow-serving_sidecar/data/`.
The interesting file for serving a model is the `saved_model.pb` file. (The checkpoint and model files are useful if you 
want to resume training from a pre-trained model). Your path should look like :
```
tensorflow-serving_sidecar/
 |
 |--data/
 |     |
 |     |--labels.pbtxt
 |     |
 |     |--faster_rcnn_resnet101_coco_2018_01_28/
 |             |
 |             |--saved_model/
 |             |   |
 |             |   |-saved_model.pb     <-- Here 
 |             |   |
 |             |   |-variables/
 |             |
 |             |--checkpoint
 |             |
 |            ...
 |
 |--docs/
 |
...

```
4. Tensorflow serving will search for a model to serve in this directory. Tensorflow serving expects to find model with a directory name being version number.
Rename the folder `saved_model` into a folder named `00001` and discard the rest of the directory. The project path should now look like:
```
tensorflow-serving_sidecar/
 |
 |--data/
 |     |
 |     |--labels.pbtxt
 |     |
 |     |--faster_rcnn_resnet101_coco_2018_01_28/
 |             |
 |             |--00001/
 |                |
 |                |-saved_model.pb 
 |                |
 |                |-variables/
 |             
 |     
 |
 |--docs/
 |
...

```

We are done with the setup!
We can proceed with serving our first model.
 
---- 
## What's next?

Deploy an object detection prediction server on local with tensorflow-serving --> [tf-serving local](tf_server_local.md).