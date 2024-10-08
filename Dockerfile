# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container
COPY . /app

# Set build-time arguments for Git info
ARG GIT_COMMIT
ARG GIT_VERSION

# Set these as environment variables inside the container
ENV COMMIT_HASH=$GIT_COMMIT
ENV VERSION_TAG=$GIT_VERSION

# Install any necessary dependencies
RUN pip install -r requirements.txt

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Define environment variable
ENV FLASK_APP=app.py

# Run the application
CMD ["flask", "run", "--host=0.0.0.0"]