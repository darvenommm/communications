#!/bin/bash

bash ./commands/production/compiling/ts.sh
bash ./commands/production/compiling/scss.sh
poetry run python manage.py collectstatic
