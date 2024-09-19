# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install necessary dependencies including ffmpeg
RUN apt-get update && apt-get install -y \
    wget \
    curl \
    unzip \
    git \
    chromium \
    chromium-driver \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Install pip and the required Python packages
RUN pip install --upgrade pip \
    && pip install selenium requests gradio \
    && pip install git+https://github.com/openai/whisper.git

# Set environment variables for Selenium
ENV CHROME_BIN=/usr/bin/chromium
ENV CHROMEDRIVER_BIN=/usr/bin/chromedriver

# Expose the port the app will run on
EXPOSE 7860

# Command to run the Gradio app
CMD ["python", "app.py"]