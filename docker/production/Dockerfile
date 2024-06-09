FROM python:3.12.2

WORKDIR /server

COPY pyproject.toml poetry.lock ./

RUN pip install poetry
RUN poetry install --only=main
RUN poetry update

COPY . .

ARG DB_HOST
ENV DB_HOST=${DB_HOST}

ARG REDIS_HOST
ENV REDIS_HOST=${REDIS_HOST}

ENV MODE='production'

CMD /bin/bash -c " \
    poetry run python manage.py migrate; \
    poetry run python manage.py createsuperuser \
    --username ${DJANGO_SUPERUSER_USERNAME} \
    --no-input || true; \
    poetry run python manage.py runserver; \
"
