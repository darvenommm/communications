FROM python:3.12.2

WORKDIR /server

COPY poetry.lock pyproject.toml ./

RUN pip install poetry
RUN poetry install --only=main
RUN poetry update

COPY . .

CMD /bin/bash -c "poetry run python manage.py runserver 0.0.0.0:$SERVER_PORT"
