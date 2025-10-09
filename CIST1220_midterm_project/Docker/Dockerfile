# Use the latest Python base image
FROM python:latest

# Set working directory
WORKDIR /app

# Install Flask (and SQLite for your app)
RUN pip install flask

# Set the Flask app name (for the flask CLI)
ENV FLASK_APP=web_server.py

# Enable auto-reload by setting development mode
ENV FLASK_ENV=development

# Expose Flask’s default port
EXPOSE 5000

# Default command runs Flask with reloader enabled
CMD ["flask", "run", "--host=0.0.0.0", "--reload"]
