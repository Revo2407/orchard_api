# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Create a virtual environment named 'aero_env' in the container
RUN python -m venv /opt/aero_env

# Activate the virtual environment and install dependencies
RUN /opt/aero_env/bin/pip install --no-cache-dir -r requirements.txt

# Make sure the virtualenv Python and pip are used
ENV PATH="/opt/aero_env/bin:$PATH"

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Define environment variables (example)
ENV AERO_AUTH your_actual_token

# Run the application
CMD ["python", "run.py"]
