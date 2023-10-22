# Lab 3 Anomaly Detection

## Lab Task – Building the Prophet model
1. Revisit the app_one Python code
![app_one_code](./screenshots/app_one_code.png)

2. Prometheus Metrics
![metrics](./screenshots/metric_8000.png)

![request_time_train](./screenshots//prometheus_request_time_train.png)
![request_time_test](./screenshots/prometheus_request_time_test.png)

3. Two metrics in Grafana dashboard
![Alt text](./screenshots/grafana_request_train_and_test.png)

4. Anomalies detected to the
console log
![Alt text](./screenshots/anomaly_detection.png)
![Alt text](./screenshots/anomaly_detection1.png)

## Lab Task – Package model as Docker container/image

- Model quality metrics
![Alt text](./screenshots/mae_and_mape.png)
![Alt text](./screenshots/mape_mae_metrics.png)
- Dataframe
![Alt text](./screenshots/dataframe.png)

- Prometheus metrics


## Lab Task – Explore model quality vs training time series and forecast durations
### 1. Seasonality in the Model:
 - The code specifically disables seasonality when creating the Prophet model by setting yearly_seasonality, weekly_seasonality, and daily_seasonality to False. This means that the model does not consider annual, weekly, or daily seasonality when making forecasts.
 - The absence of seasonality may be a deliberate choice based on the nature of the metric data. If the metric data doesn't exhibit strong seasonality patterns, it's reasonable to exclude seasonality components from the model to avoid overfitting. Including seasonality when it doesn't exist can lead to poorer forecasts.

### 2. Forecast Horizon and Training Data:
- The code in the notebook doesn't explicitly mention the forecast horizon for predictions. It generates forecasts for the test data, but the length of the forecast is not clearly defined.
- The effect of adding a longer baseline of training data can be twofold:
        - Better Model Understanding: With more historical data, the model can better understand long-term trends and patterns, potentially leading to more accurate forecasts.
        - Delayed Model Updates: However, if the model continuously reuses a long baseline for training, it might not adapt quickly to short-term changes or anomalies in the data.

### 3. Reasonable Baseline of Data for Production:
- The choice of a reasonable baseline of data for a Prophet model in a production system depends on several factors, including the nature of the metric data, the desired forecasting horizon, and the acceptable trade-off between responsiveness and accuracy.
- A longer baseline of data (historical data) is generally helpful for understanding long-term trends and improving forecast accuracy. However, the ideal baseline depends on the specific use case.
- Operational challenges might arise if the length of training data becomes too large. Longer training times may require more computational resources and storage space. Additionally, if the data distribution significantly changes over time, using very old data might not be useful.

### 4. Retraining in a Production Setting:
- Whether a Prophet model should be allowed to retrain continuously in a production setting or require manual review/approval depends on the specific use case and the importance of real-time responsiveness.
- Advantages of Continuous Retraining:
        1. `Real-time adaptability:` Continuous retraining allows the model to adapt quickly to changing data patterns.
        2. `Improved accuracy:` It helps in capturing short-term fluctuations and anomalies.
        Pitfalls of Fully Automatic Operation:
        3. `Overfitting:` If not carefully managed, continuous retraining may lead to overfitting, especially if there are data quality issues or noise.




