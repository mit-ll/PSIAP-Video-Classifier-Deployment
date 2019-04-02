# TF Server Docker image for hosting trained model
The docker image sets up an instance of a [tf-serving server](https://www.tensorflow.org/tfx/guide/serving) to host the in-vehicle-analytic classifier.

## Build an image
To build the docker image, run `./build.sh`. To give the image a specific name and tag, use `./build.sh -n=image_name -t=version_tag` (or equivalently `--name=` and `--tag=`)

Run `./build.sh` (and update tag accordingly) to build the container image. After building, run this container with `docker run {name}:{tag}`; default is `docker run iva:latest`

## Add a new model
To add a new model to the build, add a [tensorflow saved_model](https://www.tensorflow.org/guide/saved_model#load_and_serve_a_savedmodel_in_tensorflow_serving) to the `models/` directory and update the `models/models.config` file accordingly:
```
model_config_list {
  config {
    name: 'model1_name'
    base_path: '/models/model1_path'
    model_platform: 'tensorflow'
  }
  config {
    name: 'model2_name'
    base_path: '/models/model2_path'
    model_platform: 'tensorflow'
  }
}
```
For details on how to create a saved_model:
- [from tensorflow](https://www.tensorflow.org/guide/saved_model)
- [from keras](https://www.tensorflow.org/tutorials/keras/save_and_restore_models#as_a_saved_model)

## Communicate with the server
Server is accessible at `localhost:8500` over [gRPC API](https://github.com/tensorflow/serving/tree/master/tensorflow_serving/apis) and `localhost:8501` over [REST http API](https://www.tensorflow.org/tfx/serving/api_rest). 
