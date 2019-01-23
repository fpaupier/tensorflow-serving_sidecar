# Serve your machine learning model with `tensorflow-serving`

This project provides material to serve your tensorflow models with `tensorflow-serving`.
It can be followed as a step-by-step tutorial to serve your machine learning model fro people familiar with the stack but 
who don't really know the detail and in which order the stuff should be done to serve a model.


I describe installation steps to quickly get up and running. You will learn how to serve an object detection model with tensorflow serving,
first on local and then on cloud instances. In this tutorial I rely on a pre-trained object detection model freely available on tensorflow's official GitHub.

I enumerate the various possibilities of serving a tensorflow model and compare the pros and cons of each method.

## 0. Install the project

The installation process is thoroughly described in the [docs/setup.md](docs/setup.md). It covers everything you need to do
prior being able to serve a model with tensorflow-serving.

## 1. Serve your first model and perform inference with tensorflow-serving

_Time to test!_

To make sure the installation went smoothly, get your first inference result from the object detection model and tensorflow serving.
Follow the basic tutorial to serve a tensorflow model on your machine [docs/tf_server_local.md](docs/tf_server_local.md).

----

## Credits

The `object_detection` directory comes from the
[tensorflow-model](https://github.com/tensorflow/models) repository. 
It offers useful `utils` functions to tag the image returned from the model.

Feel free to investigate the models on the `tensorflow-model` repo since they are well documented and often provide tutorials to fit your needs.

