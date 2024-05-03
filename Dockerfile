FROM python:3.12.2

WORKDIR /server

COPY poetry.lock pyproject.toml ./

RUN pip install poetry
RUN poetry install --only=main
RUN poetry update

COPY . .

CMD /bin/bash -c "./commands/run-server.sh"
