from prometheus_client import Gauge, Histogram, start_http_server
import random
import time

# Create Gauge Metrics
app_one_random_gauge_0_to_1 = Gauge(
    'app_one_random_gauge_0_and_1',
    'Random gauge metric between 0 and 1 for app_one'
)

app_one_random_gauge_0_to_0_6 = Gauge(
    'app_one_random_gauge_0_to_0_6',
    'Random gauge metric between 0 and 0.6 for app_one'
)

# Create Histogram Metrics
app_one_random_histogram_0_to_1 = Histogram(
    'app_one_random_histogram_0_to_1',
    'Random histogram metric between 0 and 1 for app_one'
)

app_one_random_histogram_0_to_0_6 = Histogram(
    'app_one_random_histogram_0_to_0_6',
    'Random histogram metric between 0 and 0.6 for app_one'
)

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

        # Generate random values between 0 and 0.6 for Gauge metrics
        app_one_random_gauge_0_to_1.set(random.uniform(0, 1))
        app_one_random_gauge_0_to_0_6.set(random.uniform(0, 0.6))

        # Generate random values between 0 and 1 for Histogram metrics
        app_one_random_histogram_0_to_1.observe(random.uniform(0, 1))
        app_one_random_histogram_0_to_0_6.observe(random.uniform(0, 0.6))

        # Update metrics every 5 seconds
        time.sleep(5)  
