## Project installation

A few steps are required to test your `tf-serving` API call.

### Create a Python virtualenv

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

### Protobuf Compilation
The Tensorflow Object Detection API uses Protobufs to configure model and training parameters. 
Before the framework can be used, the Protobuf libraries must be compiled. 
This should be done by running the following command from the root directory of this project:
```bash
protoc object_detection/protos/*.proto --python_out=.
```

#### Installing Protobuf
If you don't have protobuf installed on your machine, you can install it by following the following
procedure:

##### On MacOS
 1. Make sure you have `autoconf`, `automake` and `libtool` installed. Otherwise install them with brew:
 `brew install autoconf && brew install automake && brew install libtool`
 2. Download and unzip [protobuf-all-3.6.1.zip](https://github.com/protocolbuffers/protobuf/releases/download/v3.6.1/protobuf-all-3.6.1.zip)
 3. `cd` into `protobuf-all-3.6.1` and run `./autogen.sh && ./configure && make` _Note: This may take several minutes._
 4. Then run the install with `make check && make install`
 5. You can check your `protoc` path and version with `which protoc` and `protoc --version`

##### On Linux

 1. Get the .zip wget https://github.com/protocolbuffers/protobuf/releases/download/v3.6.1/protobuf-all-3.6.1.zip` 
 2. Unzip it `unzip protobuf-all-3.6.1.zip`
 3. Go to the protobuf folder `cd protobuf-3.6.1/`
 4. Install with `./configure  && make && make check && make install` _Note: This may take several minutes._
   
## Credits

The `object_detection` directory comes from the
[tensorflow-model](https://github.com/tensorflow/models) repository. 
I use it because it offers useful utils to mark tage the image sent to the model.

Feel free to investigate the models on the `tensorflow-model` repo since they are well documented and often provide tutorials to fit your needs.


----
 ### Cheatsheet
useful commands:

(on macOS)

1. Docker machine related
```bash
docker-machine start default
eval "$(docker-machine env default)"
```

Open port of your docker machine
```bash
vboxmanage controlvm default natpf1 "nameformapping,tcp,,8501,,8501"
```

```bash
python client.py --server_url "http://localhost:8501/v1/models/fasterrcnn:predict" \
--image_path "$(pwd)/object_detection/test_images/image1.jpg" \
--output_json "/Users/fpaupier/Desktop/out_horse.json" \
--save_output_image "True" \
--label_map "$(pwd)/data/labels.pbtxt"
```
