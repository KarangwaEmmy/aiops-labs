FROM python:3

WORKDIR /app

RUN wget -O /usr/local/bin/dumb-init https://github.com/Yelp/dumb-init/releases/download/v1.2.5/dumb-init_1.2.5_x86_64
RUN chmod +x /usr/local/bin/dumb-init

# Copy the necessary files to the working directory
COPY incident_detector.py /app

# Install required Python dependencies
RUN pip install prometheus_client requests pandas tabulate datetime

# Expose the Prometheus metrics endpoint
EXPOSE 8077

# Set the entry point
CMD ["python", "incident_detector.py"]
