import json
import time
import pandas as pd
from datetime import datetime
import requests
from prophet import Prophet
from prometheus_client import Gauge, Histogram, start_http_server
from sklearn.metrics import mean_absolute_error, mean_absolute_percentage_error


gauge_request_time_train = Gauge('request_time__gauge_train','Gauge request time train')
gauge_request_time_test = Gauge('request_time_gauge_test','Gauge request tima test')

# Define the Prometheus queries for training and test data
query_train = f"request_time_train[5m]"
query_test = "request_time_test[1m]"

# Define Prometheus URL
prometheus_url = "http://localhost:9090/api/v1/query"

# train_response = requests.get(prometheus_url, params={'query': 'request_time_train[5m]'}) 
test_response = requests.get(prometheus_url, params={'query': 'request_time_test[1m]'}) 
train_response = requests.get(f"{prometheus_url}", params={"query": query_train })

fetch_interval_seconds = 60  # Fetch data every minute



while True:
    # Initialize Prophet model (with your desired settings)
    model = Prophet(interval_width=0.99, yearly_seasonality=False, weekly_seasonality=False, daily_seasonality=False)

    # Fetch training data from Prometheus
    current_time = int(time.time())
    start_time_train = current_time - 60  # Fetch data for the last 1 minute
    end_time_train = current_time

    start_time_test = current_time - 60  # Fetch data for the last 1 minute
    end_time_test = current_time


    params_train = {
        "query": query_train,
        "start": start_time_train,
        "end": end_time_train
    }
    params_test = {
        "query": query_test,
        "start": start_time_test,
        "end": end_time_test
    }

    # response_train = requests.get(prometheus_url, params=params_train)
    response_test = requests.get(prometheus_url, params=params_test)

    response_train = requests.get(f"{prometheus_url}", params={"query": query_train })
    print("start fetching data", train_response.json())
    
    # Process Prometheus query results
    if response_train.status_code == 200:
        try:
            prom_data_train = response_train.json()
            if 'result' in  prom_data_train['data'] and prom_data_train['data']['result']:
                # print(prom_data_train['data']['result'][0]['values'])
                df_train = pd.DataFrame(prom_data_train['data']['result'][0]['values'])
            else:
                print('Error getting train data')
                time.sleep(30)
                continue

        except json.JSONDecodeError as error:
            print('Failed to fetch data', error)
            time.sleep(30)
            continue

    else:
        print("Error fetching data from Prometheus")
        time.sleep(30)
        continue

    df_train.columns = ['ds', 'y']
    df_train['ds'] = df_train['ds'].apply(lambda sec: datetime.fromtimestamp(sec))
    df_train['y'] = df_train['y'].astype(float)

    print('Train Data:', df_train)


     # Process Prometheus query results for the test
    if response_test.status_code == 200:
        try:
            prom_data_test = response_test.json()
            if 'result' in  prom_data_test['data'] and prom_data_test['data']['result']:
                df_test = pd.DataFrame(prom_data_test['data']['result'][0]['values'])
            else:
                print('Error getting test data')
                time.sleep(30)
                continue

        except json.JSONDecodeError as error:
            print('Failed to fetch data', error)
            time.sleep(30)
            continue

    else:
        print("Error fetching data from Prometheus")
        time.sleep(30)
        continue

    df_test.columns = ['ds', 'y']
    df_test['ds'] = df_test['ds'].apply(lambda sec: datetime.fromtimestamp(sec))
    df_test['y'] = df_test['y'].astype(float)

    print('Test Data: ', df_test)

     # Fit the model on the training data
    model.fit(df_test)



    # Make prediction
    forecast = model.predict(df_test)

    print('forecast:', forecast)

    # Merge actual and predicted values
    performance = pd.merge(df_test, forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']], on='ds')

    print('performance:', performance)

    # Check MAE value
    performance_MAE = mean_absolute_error(performance['y'], performance['yhat'])
    print(f'The MAE for the model is {performance_MAE}')

    # Check MAPE value
    performance_MAPE = mean_absolute_percentage_error(performance['y'], performance['yhat'])
    print(f'The MAPE for the model is {performance_MAPE}')

    # Create an anomaly indicator
    performance['anomaly'] = performance.apply(lambda rows: 1 if ((float(rows.y)<rows.yhat_lower)|(float(rows.y)>rows.yhat_upper)) else 0, axis = 1)

    performance.info()

    # Check the number of anomalies
    anomalies_numer = performance['anomaly'].value_counts()
    print('anomalies_number', anomalies_numer)

    # Take a look at the anomalies
    anomalies = performance[performance['anomaly']==1].sort_values(by='ds')
    print('anomalies:' ,anomalies)

    # Sleep for the specified interval before fetching data again
    time.sleep(fetch_interval_seconds)