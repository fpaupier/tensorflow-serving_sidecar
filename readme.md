## Project installation

### COCO API installation
(Not Necessary) #FIXME

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
   

### Add Libraries to PYTHONPATH
When running locally, the tensorflow/models/research/ and slim directories should be appended to PYTHONPATH. 
This can be done by running the following root directory of this project:
```bash
# From tensorflow/models/research/
export PYTHONPATH=$PYTHONPATH:`pwd`:`pwd`/slim
```
Note: This command needs to run from every new terminal you start. 
If you wish to avoid running this manually, you can add it as a new line to the end of your ~/.bashrc file,
replacing `pwd` with the absolute path of tensorflow/models/research on your system.


## Notes

The `object_detection` and `slim` directory come from the
[tensorflow-model](https://github.com/tensorflow/models) repository.


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
python client.py --server_url="http://localhost:8501/v1/models/fasterrcnn:predict" \
--image_path="/Users/fpaupier/Desktop/horse.jpg" \
--output_json="/Users/fpaupier/Desktop/out_horse.json" \
--save_output_image="True" \
--label_map="/Users/fpaupier/projects/tensorflow-serving_sidecar/labels.pbtxt"
```
