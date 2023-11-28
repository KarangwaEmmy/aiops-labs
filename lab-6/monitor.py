import requests
from prometheus_client import start_http_server, Gauge
from tabulate import tabulate
import sys, getopt
from sklearn.metrics import mean_absolute_error, mean_absolute_percentage_error
# Prophet model for time series forecast
from prophet import Prophet
# Data processing
import numpy as np
import pandas as pd
from datetime import datetime
import time
from urllib.parse import urlencode
import json
import math

gauge_mae = Gauge('mae_gauge', 'Guage MAE')
gauge_mape = Gauge('mape_gauge', 'Guage Mape')
gauge_anomaly_counts = Gauge('gauge_anomaly_counts', 'Anomaly Counts Gauge')
y_max = Gauge('y_max', 'y maximum')
y_min = Gauge('y_min', 'y minimum')
y = Gauge('y', 'y values')

# Create an empty dataframe to store results
results_data = []

def extract_first_y( test_json ):
    # print(test_json, flush=True)
    result =  test_json['data']['result']
    val = result[0]['value'][1]
    # print(val, flush=True)
    return float(val)


def test_data():
    url_test_data_50 = {
        "query": "histogram_quantile( 0.5, sum by (le) (rate(istio_request_duration_milliseconds_bucket{app='frontend', destination_app='shippingservice', reporter='source'}[1m])))"
    }
    test_url = 'prometheus.istio-system'
    # "http://35.232.124.193:9090/api/v1/query"


    r = requests.get(test_url, params=url_test_data_50)
    # req_time_50 = extract_first_y(r.json() )

    return r.json()


def main(waiting_time):

    f = open("boutique_training.json")
    prom = json.load(f)
    df_train = pd.DataFrame( prom['data']['result'][0]['values'] )
    df_train.columns = ['ds', 'y']
    df_train

    test_offset = time.time() - df_train['ds'].iloc[0]

    df_train['ds'] = df_train['ds'] - df_train['ds'].iloc[0]

    df_train['ds'] = df_train['ds'].apply(lambda sec: datetime.fromtimestamp(sec))
    df_train

    df_train['y']=df_train['y'].astype(float)

    
    df_train.info()

    # Add seasonality
    model = Prophet(interval_width=0.99, yearly_seasonality=False, weekly_seasonality=False, daily_seasonality=False, growth='flat')
    model.add_seasonality(name='hourly', period=1/24, fourier_order=5)

    # Fit the model on the training dataset
    model.fit(df_train)



    while True:

        df_test = test_data()
        y_value = extract_first_y(test_data())

        print('Y_value', y_value, flush=True)

        if not math.isnan(y_value):
            df_test = pd.DataFrame([df_test['data']['result'][0]['value']], columns = ['ds', 'y'])

            df_test['ds'] = df_test['ds'] - test_offset

            df_test['ds'] = df_test['ds'].apply(lambda sec: datetime.fromtimestamp(sec))
        
            df_test['y']=df_test['y'].astype(float)
            df_test.info()

           
                                    
            # Make prediction
            forecast = model.predict(df_test)

            # Merge actual and predicted values
            performance = pd.merge(df_test, forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']], on='ds')

            # Check MAE value
            performance_MAE = mean_absolute_error(performance['y'], performance['yhat'])
            print(f'MAE:  {performance_MAE}', flush=True)
            gauge_mae.set(performance_MAE)

            # Check MAPE value
            performance_MAPE = mean_absolute_percentage_error(performance['y'], performance['yhat'])
            print(f'MAPE: {performance_MAPE}', flush=True)
            gauge_mape.set(performance_MAPE)

            # Create an anomaly indicator
            performance['anomaly'] = performance.apply(lambda rows: 1 if ((float(rows.y)<rows.yhat_lower)|(float(rows.y)>rows.yhat_upper)) else 0, axis = 1)

            # Check the number of anomalies
            anomaly_counts = performance['anomaly'].sum()
            print("Anomaly:", anomaly_counts, flush=True)
            gauge_anomaly_counts.set(float(anomaly_counts))

            y.set(performance['y'])
            y_min.set(performance['yhat_lower'])
            y_max.set(performance['yhat_upper'])

            # Print the y_max, y_min, y
            print('y_max', y_max, flush=True)
            print('y_min', y_min, flush=True)
            print('y', flush=True)
            # List of dictionaries containing data to be appended
            results_data.append(
                {"Current Time": datetime.now(), "Anomalies Detected": anomaly_counts, "MAE": performance_MAE,
                 "MAPE": performance_MAPE})

            # Print ongoing anomaly counts
            print(f'The number of anomalies is', anomaly_counts, flush=True)

            # Convert the list of dictionaries to a DataFrame
            results_df = pd.DataFrame(results_data)
            results_dict_list = results_df.to_dict('records')

            # Create an empty list to store rows of data
            table_rows  = []

            headers = ['Current Time', 'MAE', 'MAPE', 'Anomalies Detected']

            # Populate the table_data list with rows
            for result in results_dict_list:
                row = [
                    result['Current Time'],
                    result['Anomalies Detected'],
                    result['MAE'],
                    result['MAPE']
                ]
                table_rows .append(row)

            table_data_df = pd.DataFrame(table_rows )

            # Print the table using tabulate
            print(tabulate(table_data_df, headers=headers, tablefmt='grid'), flush=True)

            time.sleep(waiting_time)

if __name__ == '__main__':
    waiting_time = int(sys.argv[1])
    start_http_server(8099)
    main(waiting_time)
