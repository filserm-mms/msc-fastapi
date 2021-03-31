# Using base image provided by nginx unit
FROM nginx/unit:1.22.0-python3.9
# Alternatively you can use different tags from https://hub.docker.com/r/nginx/unit

COPY requirements.txt /home/msc-fastapi/requirements.txt

RUN pip install -r /home/msc-fastapi/requirements.txt

COPY config.json /docker-entrypoint.d/config.json

COPY . /home/msc-fastapi