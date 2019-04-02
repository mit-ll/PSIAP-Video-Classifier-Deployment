# PSIAP-Video-Classifier-Deployment
This sets up a pair of Docker container services for classifying footage with a tensorflow model

The two services are:
- tf_server: A tensorflow-serving server which hosts Convolutional Neural Networks. The example model classifies footage as in-vehicle or out-of-vehicle. The services can be accessed from localhost at `localhost:8501`, or from within the docker-compose network at `tf_server`. See [the tf_server README](https://github.com/mit-ll/PSIAP-Video-Classifier-Deployment/tree/master/tf_serving) for more details
- client: A python3 docker image which processes the videos contained within the subdirectory `videos` and generates a report in the subdirectory `reports`. It accomplishes this by using ffmpeg to extract keyframes, then submits those frames to `tf_server` for classification, and then generates a report based on the classifications. See [the client README](https://github.com/mit-ll/PSIAP-Video-Classifier-Deployment/tree/master/client) for more details

## Windows Set-Up

0. [Create a Docker Hub Account](https://hub.docker.com/signup)
1. [Install Docker Desktop for Windows](https://hub.docker.com/editions/community/docker-ce-desktop-windows)
2. Add Docker to Windows Path, should be something like C:\Program Files\Docker\Docker\resources\bin
3. [Configure Docker to use proxy, if needed (note look for config.json in \Users\USERXXX\.docker)](https://docs.docker.com/network/proxy/)
4. Copy video files to directory: \deploy\videos
5. Open Windows PowerShell
6. Navigate to deploy directory
7. [Log in to the Docker registry](https://docs.docker.com/engine/reference/commandline/login/), `docker login`
8. [Run Docker Compose to build service](https://docs.docker.com/compose/), `docker-compose build`
9. `docker-compose up`
10. `docker-compose up -d`

## *nix instructions
0. Install Docker for your platform, [e.g. ubuntu](https://docs.docker.com/install/linux/docker-ce/ubuntu/)
1. Configure [proxy](https://docs.docker.com/network/proxy/) if necessary
2. Navigate into this directory in terminal
3. Copy video files to directory `./videos`
4. `docker-compose build`
5. `docker-compose up`

## Authors
* Jeffrey Liu (MITLL)  
* Chris Budny (MITLL)
* Andrew Weinert  (MITLL)    

## Acknowledgments
* Gabriela Barrera (MITLL)
* Dieter Schuldt (MITLL)  
* Steven Talpas (NJOHSP)  
* William Drew (NJOHSP)  

## Disclaimer

This work was performed under the following financial assistance award 70NANB17Hl69 from U.S. Department of Commerce, National Institute of Standards and Technology.
