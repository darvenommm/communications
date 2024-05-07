#!/bin/bash

docker exec -it communications-production-server /bin/bash -c "poetry run python manage.py test apps"
