# Build Docker Images

You can build your own docker image using the Dockerfile in the docker direcoty.
```
docker build -t tensorflow-serving-sidecar-client:latest .
```

# Public docker image

A public docker image in Google Cloud Container Registry is availabe if you don't want to build the image yourself. You can just pull the image and use.
```
asia.gcr.io/im-mlpipeline/tensorflow-serving-sidecar-client:latest
```





# Sending Prediction Requests
You can use the following command to send prediction requests.

```
# absolute path to the directory where label_map.pbtxt and input image files are. It must be an absolute path. Docker volume mounting doesn't work with relative path. All other paths in this scripts will work with relative path.
export VOLUME_PATH=""
export SERVER_URL="http://34.73.137.228:8501/v1/models/faster_rcnn_resnet:predict"
# relative path to the test image. i.e. config/image1.jpg. The path is relative to VOLUME_PATH
export IMAGE_PATH=""
# relative path to the output json. i.e. config/out_image1.json. The path is relative to VOLUME_PATH
export OUTPUT_JSON=""
# relative path to the label_map.pbtxt. i.e. config/label_map.pbtxt. The path is relative to VOLUME_PATH
export LABEL_MAP=""
# Specify True if you want to save the output image. 
export SAVE_OUTPUT_IMAGE=True
# You can use the publicly available docker image or use your own image
export DOCKER_IMAGE_NAME="asia.gcr.io/im-mlpipeline/tensorflow-serving-sidecar-client:latest"

docker run -it -v ${VOLUME_PATH}:/app/tensorflow-serving_sidecar/config -t ${DOCKER_IMAGE_NAME} client.py --server_url=${SERVER_URL}  --image_path=${IMAGE_PATH} --output_json=${OUTPUT_JSON} --save_output_image=${SAVE_OUTPUT_IMAGE} --label_map=${LABEL_MAP}
```