import time
import requests
import pandas as pd
from datetime import datetime
import time
from tabulate import tabulate
from prometheus_client import start_http_server, Gauge

# Define threshold and initial accumulators for each service
threshold = 10
accumulator_1 = 0
accumulator_2 = 0

# Prometheus gauge metrics for accumulators and incident severiies
temperature_gauge = Gauge('temperature', 'Current sum of accumulators')
sev1_gauge = Gauge('sev1_incident', 'Sev 1 Incident Gauge')
sev2_gauge = Gauge('sev2_incident', 'Sev 2 Incident Gauge')
anomaly_count_1_gauge = Gauge('anomaly_count_1', 'Anomaly Count for Accumulator 1')
anomaly_count_2_gauge = Gauge('anomaly_count_2', 'Anomaly Count for Accumulator 2')

def fetch_result_count(url):
    response = requests.get(url)
    data = response.json()
    return int(data['data']['result'][0]['value'][1])

def process_requests():
    global accumulator_1, accumulator_2

    url_1 = 'http://34.68.4.178:9090/api/v1/query?query=lab7_frontend_2_shippingservice_anomaly_count'
    url_2 = 'http://34.68.4.178:9090/api/v1/query?query=lab7_checkoutservice_2_shippingservice_anomaly_count'

    result_count_1 = fetch_result_count(url_1)
    result_count_2 = fetch_result_count(url_2)

    # Set anomaly counts for accumulator 1 and accumulator 2 in Prometheus gauges
    anomaly_count_1_gauge.set(result_count_1)
    anomaly_count_2_gauge.set(result_count_2)

    accumulator_1 = update_accumulator(accumulator_1, result_count_1)
    accumulator_2 = update_accumulator(accumulator_2, result_count_2)

    # Summing the accumulators and categorizing incidents based on thresholds
    total_accumulator = accumulator_1 + accumulator_2

    temperature_gauge.set(total_accumulator)

    process_incidents(accumulator_1, accumulator_2, total_accumulator)

def update_accumulator(accumulator, result_count):
    if result_count > 0:
        accumulator += 1
    else:
        accumulator = max(0, accumulator - 2)  # Subtract 2 if no anomaly detected
    return accumulator

def process_incidents(accumulator_1, accumulator_2, total_accumulator):
    if total_accumulator >= threshold:
        if accumulator_1 > 0 and accumulator_2 > 0:
            sev1_gauge.set(1)
            print("Sev 1 Incident detected! Triggering an alert.")
        else:
            sev2_gauge.set(1)
            print("Sev 2 Incident detected! Triggering an alert.")

results_data = []

def print_metrics_table():
    temperature = temperature_gauge._value.get()
    sev1 = sev1_gauge._value.get()
    sev2 = sev2_gauge._value.get()
    anomaly_count_1 = anomaly_count_1_gauge._value.get()
    anomaly_count_2 = anomaly_count_2_gauge._value.get()

    results_data.append({
        "Current Time": datetime.now(),
        "Anomaly Count 1": anomaly_count_1,
        "Anomaly Count 2": anomaly_count_2,
        "Temperature": temperature,
        "Sev 1": sev1,
        "Sev 2": sev2
    })

    # Convert the list of dictionaries to a DataFrame
    results_df = pd.DataFrame(results_data)
    results_dict_list = results_df.to_dict('records')

    # Create an empty list to store rows of data
    table_rows = []

    headers = ['Current Time', 'Anomaly Count 1', 'Anomaly Count 2', 'Temperature', 'Sev 1', 'Sev 2']

    # Populate the table_rows list with rows
    for result in results_dict_list:
        row = [
            result['Current Time'],
            result['Anomaly Count 1'],
            result['Anomaly Count 2'],
            result['Temperature'],
            result['Sev 1'],
            result['Sev 2'],
        ]
        table_rows.append(row)

    table_data_df = pd.DataFrame(table_rows)

    # Print the table using tabulate
    print(tabulate(table_data_df, headers=headers, tablefmt='grid'), flush=True)
def main():
    start_http_server(8077)

    while True:
        process_requests()
        print_metrics_table()
        time.sleep(15) 

if __name__ == "__main__":
    main()
