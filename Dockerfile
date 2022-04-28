FROM python:3.8.12-slim

COPY requirements.txt /tmp
RUN pip3 install -r /tmp/requirements.txt

COPY ./app /app
WORKDIR /app
