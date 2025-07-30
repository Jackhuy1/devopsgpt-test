FROM python:3.9

# Install necessary system dependencies for pygame and SDL2 libraries
RUN apt-get update && \
    apt-get install -y \
        libsdl2-dev \
        libsdl2-image-dev \
        libsdl2-mixer-dev \
        libsdl2-ttf-dev \
        libsmpeg-dev && \
    rm -rf /var/lib/apt/lists/*

# Set working directory in the container
WORKDIR /app

# Copy game source code into the container
COPY . /app

# Install python dependencies (pygame)
RUN pip install --no-cache-dir pygame

# Set environment variables required for runtime configuration
ENV GAME_MODE=default
ENV DISPLAY=:0

# Specify default command to run the Snake game
CMD ["python", "game.py"]
