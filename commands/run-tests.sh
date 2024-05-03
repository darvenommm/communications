#!/bin/bash

docker exec -it communications-server /bin/bash -c "poetry run python manage.py test apps"
