FROM python:3.10-slim

# Create a non-root user
RUN adduser --disabled-password --gecos '' appuser

WORKDIR /app

# Copy only requirements first for better caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Set environment variables for Flask
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=8080
ENV PYTHONUNBUFFERED=1

# Expose port 8080
EXPOSE 8080

# Change to non-root user
USER appuser

# Use Gunicorn for production
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "app:app"]
