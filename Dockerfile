# Use a lightweight Python base image with a specific version
FROM python:3.9.16-slim

# Set environment variables for better behavior in containers
ENV PYTHONUNBUFFERED=1

# Set the working directory inside the container
WORKDIR /app

# Copy the dependency file first to leverage Docker's caching mechanism
COPY requirements.txt /app/requirements.txt

# Install required Python dependencies
RUN pip install -r requirements.txt

# Copy the application code into the container
COPY snake_game.py /app/snake_game.py

# Command to run the application
CMD ["python", "snake_game.py"]
