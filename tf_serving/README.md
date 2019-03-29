# TF Server Docker image for hosting in-vehicle-analytic model
The docker image sets up an instance of a [tf-serving server](https://llcad-github.llan.ll.mit.edu/HADR/tensorflow_server) to host the in-vehicle-analytic classifier.

To build the docker image, run `./build.sh`. To give the image a specific name and tag, use `./build.sh -n=image_name -t=version_tag` (or equivalently `--name=` and `--tag=`)

To add a new model to the build, add a tensorflow saved_model to the `models/` directory and update the `models/models.config` file accordingly. Then run `./build.sh` (and update tag accordingly)

After building, run with `docker run {name}:{tag}`; default is `docker run iva:latest`

Server is accessible at `localhost:8500` over grpc and `localhost:8501` over http
