#!/bin/bash

bash ./commands/production/compiling/run.sh
docker compose --project-directory ./ -f ./docker/production/docker-compose.yaml up -d --build
