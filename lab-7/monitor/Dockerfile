FROM python:3

WORKDIR /app

RUN wget -O /usr/local/bin/dumb-init https://github.com/Yelp/dumb-init/releases/download/v1.2.5/dumb-init_1.2.5_x86_64
RUN chmod +x /usr/local/bin/dumb-init

# Copy the repo content to the working directory
COPY checkoutservice_2_shippingservice.json /app
COPY frontend_2_shippingservice.json /app
COPY monitor.py /app

# Install Prometheus client library
RUN pip install prometheus_client Prophet scikit-learn requests datetime pandas tabulate matplotlib 

# Entry Port
EXPOSE 8089

#Run application
CMD ["python","monitor.py"]
