#!/bin/bash

docker compose --file ./commands/server/docker-compose.yaml --project-directory . up --build
