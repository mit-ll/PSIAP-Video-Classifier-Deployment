# Client docker container

Put python requirements in `setup/requirements.txt`

Put python source code in `app/`

Put commands to be run when docker container is run in `app/run.sh`

Build with `docker build . --tag={image_name}:{version_tag}`

Run with: 
```
docker run  --mount type=bind,source="{path/to/videos}",target=/videos,readonly\ 
--mount type=bind,source="{path/to/report_outputs}",target=/reports\
{image_name}:{version_tag}
```

In the docker container, videos will be accessible at `/videos` and all output reports should be written to `/reports`
