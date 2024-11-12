#!/bin/bash

# Default to production if no argument is provided
ENV=${1:-production}

# Update the .env file with the selected environment
echo "FLASK_ENV=$ENV" > .env
echo "Updated .env file with FLASK_ENV=$ENV"

# Build the Docker image
docker build --build-arg ENV=$ENV -t profile-rewriter-tool .

# Stop and remove any existing container
docker stop profile-rewriter-container || true
docker rm profile-rewriter-container || true

# Run the Docker container
docker run -d \
  --name profile-rewriter-container \
  -p 5001:5000 \
  -e FLASK_ENV=$ENV \
  profile-rewriter-tool
