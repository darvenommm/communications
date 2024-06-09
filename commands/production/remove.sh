#!/bin/bash

docker stop communications-production-database
docker stop communications-production-redis
docker stop communications-production-server

docker rm communications-production-database
docker rm communications-production-redis
docker rm communications-production-server
