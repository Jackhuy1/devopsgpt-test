FROM python:3.9-slim

# Set the working directory within the container
WORKDIR /app

# Copy the entire application source code to the container
COPY . /app

# Install required Python libraries (Flask in this case)
RUN pip install --no-cache-dir flask

# Expose port 5000 for the Flask application
EXPOSE 5000

# Command to run the integrated Python application
CMD ["python", "app.py"]
