# Use an official Python 3.8 slim image as the base image
FROM python:3.8-slim

# Set the working directory inside the container
WORKDIR /app

# Copy dependency file and install libraries
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire application source code into the container
COPY . /app

# Define the command to run the Snake game application
CMD ["python", "snake_game.py"]
