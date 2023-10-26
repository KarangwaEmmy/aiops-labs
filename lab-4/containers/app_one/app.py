from prometheus_client import Gauge, Histogram, start_http_server
import random
import time

# Create Gauge Metrics for request time train and test

request_time_train = Gauge(
    'request_time_train',
    'Simulated request time for training (clipped at 600 msec)',
)

request_time_test = Gauge(
    'request_time_test',
    'Random gauge metric between 0 and 1 for testing (anomaly detection)',
)

# Simulate metric updates
if __name__ == '__main__':
    start_http_server(8000)  # Start Prometheus HTTP server

    while True:

          # Generate random values between 0 and 0.6 for request_time_train
        request_time_train.set(min(random.uniform(0, 0.6), 0.6))

        # Generate random values between 0 and 1 for request_time_test
        request_time_test.set(random.random())

        # Update metrics every 5 seconds
        time.sleep(5)  
