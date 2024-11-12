FROM python:3.9-slim

# Set build arguments
ARG ENV=development
ENV FLASK_ENV=$ENV

# Set the working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt /app/
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && pip install -r requirements.txt \
    && if [ "$ENV" = "production" ]; then pip install gunicorn; fi \
    && if [ "$ENV" = "development" ]; then pip install flask-debugtoolbar; fi \
    && apt-get remove -y build-essential \
    && apt-get autoremove -y \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* ~/.cache/pip

# Copy the application files
COPY . /app

# Expose Render's dynamic port
EXPOSE ${PORT:-5000}

# Default environment variables
ENV FLASK_APP=app.py

# Command for Flask or Gunicorn based on environment
CMD ["sh", "-c", "if [ \"$FLASK_ENV\" = \"development\" ]; then flask run --host=0.0.0.0 --port=$PORT; else gunicorn -b 0.0.0.0:$PORT app:app; fi"]
