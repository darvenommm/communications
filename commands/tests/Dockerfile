FROM python:3.12.3

WORKDIR /django_server

RUN pip install poetry

COPY pyproject.toml .

RUN poertyr install

COPY . .

CMD [ "python", "manage.py", "runserver", "$SERVER_PORT_FOR_TESTS" ]
