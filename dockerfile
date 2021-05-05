FROM python:3.8-slim-buster

ADD . /APP/
WORKDIR /APP/
RUN apt-get update && apt-get -y install libpq-dev gcc
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
