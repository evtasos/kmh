FROM python:3.8-slim-buster

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install DNS utilities and OpenSSL
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    openssl && \
    rm -rf /var/lib/apt/lists/*

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Generate a self-signed certificate
RUN openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365 -nodes -subj "/C=GR/L=Local/O=Dev/CN=kmh.metaxa"

# Make port 5566 available to the world outside this container
EXPOSE 5566

# Define environment variable
ENV NAME World

# Run app.py when the container launches
CMD ["gunicorn", "-w", "1", "-b", "0.0.0.0:5566", "--certfile=cert.pem", "--keyfile=key.pem", "--error-logfile", "/app/kmh_error.log", "--access-logfile", "/app/kmh_access.log", "app:app"]
