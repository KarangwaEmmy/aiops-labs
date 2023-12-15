import datetime
import pandas as pd
import time
import json
import requests
from prophet import Prophet
from sklearn.metrics import mean_absolute_error, mean_absolute_percentage_error
from prometheus_client import start_http_server, Gauge

prometheus_url = "http://prometheus:9090/api/v1/query"
iteration = 5
prometheus_query = f"request_time_train[5m]"
prometheus_test_query = f"request_time_test[1m]"

gauge_mae = Gauge('mae_gauge', 'Guage MAE')
gauge_mape = Gauge('mape_gauge', 'Guage Mape')
gauge_anomaly_counts = Gauge('gauge_anomaly_counts', 'Anomaly Counts Gauge')

# Create an empty dataframe to store results
results_data = pd.DataFrame(columns=["Current Time", "MAE", "MAPE", "Anomalies Detected"])

# Simulate metric updates
if __name__ == '__main__':
    start_http_server(7000)  # Start Prometheus HTTP server

# Continuously fetch and train the model every 60 seconds
while True:
    # Initialize a new Prophet model inside the loop
    model = Prophet(interval_width=0.99, yearly_seasonality=False, weekly_seasonality=False, daily_seasonality=True)

    train_response = requests.get(f"{prometheus_url}", params={"query": prometheus_query})

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
        print("Failed to fetch training data")
        time.sleep(30)  # Sleep for 30 seconds and then try again
        continue

    df_train = pd.DataFrame(train_values)

    df_train.columns = ['ds', 'y']
    df_train['ds'] = df_train['ds'].apply(lambda sec: datetime.datetime.fromtimestamp(sec))
    df_train['y'] = df_train['y'].astype(float)

    time.sleep(60)

    # Fit the Prophet model with training data
    model.fit(df_train)

    # Make multiple forecasts
    for itel in range(iteration):
        test_response = requests.get(f"{prometheus_url}", params={"query": prometheus_test_query})

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

        # Make prediction
        forecast = model.predict(df_test)

        # Merge actual and predicted values
        performance = pd.merge(df_test, forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']], on='ds')

        # Check MAE value
        performance_MAE = mean_absolute_error(performance['y'], performance['yhat'])
        print(f'The MAE for the model is {performance_MAE}')
        gauge_mae.set(performance_MAE)

        # Check MAPE value
        performance_MAPE = mean_absolute_percentage_error(performance['y'], performance['yhat'])
        print(f'The MAPE for the model is {performance_MAPE}')
        gauge_mape.set(performance_MAPE)

        # Create an anomaly indicator
        performance['anomaly'] = performance.apply(lambda rows: 1 if ((float(rows.y)<rows.yhat_lower)|(float(rows.y)>rows.yhat_upper)) else 0, axis = 1)

        # Check the number of anomalies
        anomaly_counts = performance['anomaly'].value_counts()
        print("Anomaly counts:", anomaly_counts)
        gauge_anomaly_counts.set(float(anomaly_counts.get(1, 0)))

        # Current time
        current_time = datetime.datetime.now()
        results_data = pd.concat([results_data, pd.DataFrame({"Current Time": [current_time], "MAE": [performance_MAE], "MAPE": [performance_MAPE], "Anomalies Detected": [anomaly_counts[1]]})], ignore_index=True)

        # Print results after each iteration
        print(results_data)

        # Sleep for 60 seconds before fetching data and training the model again
        time.sleep(60)

    # Print the final results DataFrame
    print(results_data)


