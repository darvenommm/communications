#!/bin/bash

docker compose --file ./commands/db/docker-compose.yaml --env-file .env up --build

