from collections import Counter
import datetime
import pandas as pd
import time
import json
import requests
from prophet import Prophet
from sklearn.metrics import mean_absolute_error, mean_absolute_percentage_error
from prometheus_client import start_http_server, Gauge
from tabulate import tabulate

prometheus_url = "http://localhost:9090"
num_forecast_steps = 5
train_duration_minutes = 5  # Number of minutes of training data to extract from Prometheus (5 minutes)
test_duration_minutes = 1
prometheus_query = f"request_time_train[{train_duration_minutes}m]"
prometheus_test_query = f"request_time_test[{test_duration_minutes}m]"

# Anomaly threshold
anomaly_threshold = 0.2

# Start the Prometheus HTTP server to expose metrics
start_http_server(7000)  # Use a port of your choice
MAPE_Gauge = Gauge("MAPE_Gauge", "Performance Mean Absolute Percentage Error")
MAE_Gauge = Gauge("MAE_Gauge", "Performance Mean Absolute Error")
Anomaly_Counts_Gauge = Gauge("Anomaly_Count", "Anomaly count for each Iteration")

# Create an empty dataframe to store results
results_data = []
# Continuously fetch and train the model every 60 seconds
while True:
    # Initialize a new Prophet model inside the loop
    model = Prophet(interval_width=0.99, yearly_seasonality=False, weekly_seasonality=True, daily_seasonality=False)
    ### daily seasonality 

    train_response = requests.get(f"{prometheus_url}/api/v1/query", params={"query": prometheus_query})

    # Check the HTTP status code of the response
    if train_response.status_code == 200:
        try:
            train_data = train_response.json()

            # Extract values from the response if 'result' exists and is not empty
            if 'result' in train_data['data'] and train_data['data']['result']:
                train_values = train_data['data']['result'][0]['values']
            else:
                print("No training data available.")
                time.sleep(30)  # Sleep for 30 seconds and then try again
                continue

        except json.JSONDecodeError as e:
            print("Failed to parse training data JSON:", e)
            time.sleep(30)  # Sleep for 30 seconds and then try again
            continue
    else:
        print("Failed to fetch training data:", train_response)
        time.sleep(30)  # Sleep for 30 seconds and then try again
        continue

    df_train = pd.DataFrame(train_values)

    df_train.columns = ['ds', 'y']
    df_train['ds'] = df_train['ds'].apply(lambda sec: datetime.datetime.fromtimestamp(sec))
    df_train['y'] = df_train['y'].astype(float)

    print("train data")
    print(df_train)
    time.sleep(60)

    # Fit the Prophet model with training data
    model.fit(df_train)

    # Make multiple forecasts
    for step in range(num_forecast_steps):


        # # Fetch test data for the previous minute 
        # end_time_test = start_time_train
        # start_time_test = end_time_test - datetime.timedelta(minutes=1)

        test_response = requests.get(f"{prometheus_url}/api/v1/query", params={"query": prometheus_test_query})

        # Check the HTTP status code of the response
        if test_response.status_code == 200:
            try:
                test_data = test_response.json()

                # Extract values from the response if 'result' exists and is not empty
                if 'result' in test_data['data'] and test_data['data']['result']:
                    test_values = test_data['data']['result'][0]['values']
                else:
                    print("No test data available.")
                    time.sleep(30)  # Sleep for 30 seconds and then try again
                    continue

            except json.JSONDecodeError as e:
                print("Failed to parse test data JSON:", e)
                time.sleep(30)  # Sleep for 30 seconds and then try again
                continue
        else:
            print("Failed to fetch test data:", test_response)
            time.sleep(30)  # Sleep for 30 seconds and then try again
            continue

        df_test = pd.DataFrame(test_values)
        df_test.columns = ['ds', 'y']
        df_test['y'] = df_test['y'].astype(float)
        df_test['ds'] = df_test['ds'].apply(lambda sec: datetime.datetime.fromtimestamp(sec))
        print("test data")
        print(df_test)

        # Make prediction
        forecast = model.predict(df_test)


        # Merge actual and predicted values
        performance = pd.merge(df_test, forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']], on='ds')

        # Check MAE value
        performance_MAE = mean_absolute_error(performance['y'], performance['yhat'])
        print(f'The MAE for the model is {performance_MAE}')

        MAE_Gauge.set(performance_MAE)

        # Check MAPE value
        performance_MAPE = mean_absolute_percentage_error(performance['y'], performance['yhat'])
        print(f'The MAPE for the model is {performance_MAPE}')

        MAPE_Gauge.set(performance_MAPE)

        # Create an anomaly indicator
        # performance['anomaly'] = performance.apply(lambda row: 1 if row['y'] > anomaly_threshold else 0, axis=1)
        performance['anomaly'] = performance.apply(lambda rows: 1 if ((float(rows.y)<rows.yhat_lower)|(float(rows.y)>rows.yhat_upper)) else 0, axis = 1)
        # print("performance")
        # print(performance)

        # Check the number of anomalies
        anomaly_counts = performance['anomaly'].value_counts()
        print("Anomaly counts:", anomaly_counts)

        Anomaly_Counts_Gauge.set(float(anomaly_counts.get(1, 0)))
        current_time = datetime.datetime.now()
        # Take a look at the anomalies
        anomalies = performance[performance['anomaly'] == 1].sort_values(by='ds')
        # print("Anomalies detected:")
        # print(anomalies)
        
        results_data.append({"Current Time": current_time, "Anomalies Detected": anomaly_counts, "MAE": performance_MAE, "MAPE": performance_MAPE})
        print(results_data)


    # Print results
    results_data.append({"Current Time": current_time, "Anomalies Detected": anomaly_counts, "MAE": performance_MAE, "MAPE": performance_MAPE})
    print(results_data)