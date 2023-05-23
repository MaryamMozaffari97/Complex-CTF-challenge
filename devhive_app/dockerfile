# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /opt/services/djangoapp/src

# Install any needed packages specified in requirements.txt
COPY requirements.txt /opt/services/djangoapp/src/
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Copy the rest of the application code
COPY . /opt/services/djangoapp/src/

# Create a non-root user and give it ownership of the work directory
RUN useradd -ms /bin/bash djangoappuser && \
    chown -R djangoappuser:djangoappuser /opt/services/djangoapp/src

# Switch to non-root user
USER djangoappuser

# Expose the required port
EXPOSE 8000
# Set the entrypoint
CMD ["sh", "./docker-entrypoint.sh"]
