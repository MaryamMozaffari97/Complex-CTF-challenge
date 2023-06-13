# pull official base image
FROM python:3.11.3-slim-buster

# set work directory
# WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install system dependencies
RUN apt-get update && apt-get install -y netcat

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt /opt/services/flaskapp/src/requirements.txt
RUN pip install -r /opt/services/flaskapp/src/requirements.txt

# copy project
COPY . /opt/services/flaskapp/src/

# Create a non-root user and give it ownership of the work directory
RUN useradd -ms /bin/bash flaskappuser && \
    chown -R flaskappuser:flaskappuser /opt/services/flaskapp/src

# Switch to non-root user
USER flaskappuser

# Expose the required port
EXPOSE 5000

# Set the entrypoint
ENTRYPOINT ["/opt/services/flaskapp/src/docker-entrypoint.sh"]