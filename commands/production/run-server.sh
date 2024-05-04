#!/bin/bash

docker compose --project-directory ./ -f ./docker/production-docker-compose.yaml up -d
