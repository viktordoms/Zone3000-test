FROM python:3.10

ENV PYTHONUNBUFFERED 1

WORKDIR /api

COPY Pipfile Pipfile.lock /api/

RUN pip install pipenv

RUN pipenv install --system --deploy --ignore-pipfile

COPY . /api/
