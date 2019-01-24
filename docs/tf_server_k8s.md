# Deploy a tensorflow-server on the cloud

At the end of this step you will have a kubernetes cluster exposing your model for inference.
To reach this goal, the steps are:
1. Create a docker image with with your `saved_model.pb` file embedded.
2. Deploy in kubernetes.

## 1. Create a docker image with with your `saved_model.pb` file embedded.

You remember the docker image we used to run tensorflow-serving and perform inference with our object detection model in our [local example](tf_server_local.md)
shared the model data with the host filesystem. We will now build a self-sufficient image that contains the model.
   
We take the tensorflow-serving base image and add our model in order to deploy on Kubernetes.

### 1.1 Create a custom tensorflow-server image

1. Run a serving image as a daemon:
```bash
docker run -d --name serving_base tensorflow/serving
```

2. Copy the `faster_rcnn_resnet101_coco` model data to the container's `models/` folder:
```bash
# From tensorflow-serving_sidecar/
docker cp $(pwd)/data/faster_rcnn_resnet101_coco_2018_01_28 serving_base:/models/faster_rcnn_resnet
```
3. Commit the container to serving the `faster_rcnn_resnet` model:
```bash
docker commit --change "ENV MODEL_NAME faster_rcnn_resnet" serving_base faster_rcnn_resnet_serving
```
_Note:_ if you use a different model, change `faster_rcnn_resnet` in the `--change` argument accordingly.

`faster_rcnn_resnet_serving` will be our new serving image.
You can check this by running `docker images`, you should see a new docker image:

![faster_rcnn_resnet_serving new docker image](../assets/docker_images_tf.png)


4. Stop the serving base container
```bash
docker kill serving_base
docker rm serving_base
```

Great, next step is to test the server.

### 1.2 Test the custom server

Before deploying our app on kubernetes, let's make sure it works correctly.

1. Start the server:
```bash
docker run -p 8501:8501 -t faster_rcnn_resnet_serving &
```
_Note:_ Make sure you have killed the previous running servers otherwise the port `8501` may be locked.
You can also use another port _e.g._ `8500`.

2. We can use the same client code to call the server.
```bash
# From tensorflow-serving_sidecar/
python client.py --server_url "http://localhost:8501/v1/models/faster_rcnn_resnet:predict" \
--image_path "$(pwd)/object_detection/test_images/image1.jpg" \
--output_json "$(pwd)/object_detection/test_images/out_image2.json" \
--save_output_image "True" \
--label_map "$(pwd)/data/labels.pbtxt"
``` 

## 2. Deploy our app on kubernetes


TODO






________
### Resources


- More resources on Docker `bind` mount is available on [Docker bind official docs](https://docs.docker.com/storage/bind-mounts/).
- To understand how the docker `commit` command works, refer to the [Docker commit official doc](https://docs.docker.com/engine/reference/commandline/commit/).

---------

_Note:_ This tutorial comes from the [tensorflow-serving official documentation](https://www.tensorflow.org/serving/serving_kubernetes),
I adapted it to fit our use case (different model used).