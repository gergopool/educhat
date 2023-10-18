#!/bin/bash

# Pull the images if they don't exist
docker pull gergopool/educhat

cd docker
./docker_run.sh -i -p 3000:3000 python3 run.py