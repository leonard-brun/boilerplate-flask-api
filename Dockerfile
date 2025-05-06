FROM python:3.12-slim

COPY ./app/requirements* /tmp/
RUN pip3 install -r /tmp/requirements.txt
RUN pip3 install -r /tmp/requirements.dev.txt

COPY ./app /app
WORKDIR /app
