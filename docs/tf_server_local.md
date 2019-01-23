# Create a local tensorflow server and make your first API call

This will help you make sure you installed everything correctly.

1. Run the tensorflow server, pay attention to forward the port `8501` and bind the correct path.
Fine tune the `-v` arg if you use a different model.
```bash
# From tensorflow-serving_sidecar/
docker run -t --rm -p 8501:8501 \
   -v "$(pwd)/data/faster_rcnn_resnet101_coco_2018_01_28:/models/faster_rcnn_resnet" \
   -e MODEL_NAME=faster_rcnn_resnet \
   tensorflow/serving &
```
_What did we just do there?_ 

We simply run a docker container from the original `tensorflow-server` image. We bind the directory on the local host filesystem containing our `faster_rcnn_resnet101_coco_2018_01_28`
 model with the `models/` directory inside the container. The container can read and write data in/from this shared directory. 

This simple drawing sums it up:
 
 ![docker run -v drawing](../assets/docker_run_v.jpg) 

2. Now that we have a local server up and running we call him on port `8501`.
Call the server to perform an inference. Fine tune the `--server_url` argument if you use a different model.
The `client.py` script is a very simple script to pre-process the input image, perform the API call, and process the server's output. 
It returns detections score and build the annotated image. 

```bash
# From tensorflow-serving_sidecar/
python client.py --server_url "http://localhost:8501/v1/models/faster_rcnn_resnet:predict" \
--image_path "$(pwd)/object_detection/test_images/image1.jpg" \
--output_json "$(pwd)/object_detection/test_images/out_image1.json" \
--save_output_image "True" \
--label_map "$(pwd)/data/labels.pbtxt"
```

If everything works fine you should have an image generated under `object_detection/test_images/out_image1.jpeg`.
With the provided model and example it should look like:
![Output image based on the inference results from the model](../assets/out_image1.jpeg) 

Great, we can now dive into more elaborate setup, [return to the main Readme](../readme.md) to check different ways to serve your models.

----

This contents is basically an application of the tensorflow serving documentation with a custom model.
See https://www.tensorflow.org/serving/ for more reference