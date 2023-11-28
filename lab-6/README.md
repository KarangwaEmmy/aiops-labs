# Lab 6: Anomaly detection in GKE with Prophet and Istio

### Lab Task 2 – Train a Prophet model with seasonality for normal operation
![Alt text](./screenshots/Total_request_bound.png)
![Alt text](./screenshots/response_time.png)
![Alt text](./screenshots/number_of_users.png)

- Scrap data
![Alt text](./screenshots/scrapping_data.png)
![Alt text](./screenshots/get_mapped_ip.png)

2. Set the Load environment variables
![Alt text](./screenshots/environment_variables.png)

3. Generate  training data from Prometheus
![Alt text](./screenshots/Change_Ip_address.png)
![Alt text](./screenshots/Edit_load_balancer.png)

5. Save the training data pulled by the curl command to a local file
![Alt text](./screenshots/save_training_data.png)

6. Training Metric
![Alt text](./screenshots/Train_metric.png)

- Forecast
![Alt text](./screenshots/forecast.png)


### Lab Task 3 – Verify no/minimal anomaly detection under normal operation
- Trend and Hourly
![Alt text](./screenshots/trend_and_hour.png)

- Run monitor file
![Alt text](./screenshots/monitor_file.png)

2. read input argument
![Alt text](./screenshots/read_input.png)

3. code should contain just one loop following the initial model training
![Alt text](./screenshots/loop_code.png)

 ![Alt text](./screenshots/pre_anomalies.png)


### Lab Task 4 – Inject faults with Istio to detect anomalies
1. ![Alt text](./screenshots/add_delays.png)




### Lab Task 5 – Deploy your monitor into the Boutique cluster and publish to Grafana
1. ![Alt text](./screenshots/dockerhub_image.png)
2. ![Alt text](./screenshots/copy_training_data.png)
3. ![Alt text](./screenshots/deployment_file.png)
![Alt text](./screenshots/deployment.png)
![Alt text](./screenshots/get_deployment.png)
![Alt text](./screenshots/scalling_up.png)
4.  console output as the monitor `kubectl logs <pod_id>`
![Alt text](./screenshots/get_logs_1.png)
![Alt text](./screenshots/get_logs_2.png)

5. 

6. 

7. publish  anomaly metric and prediction quality metrics back to Grafana the monitor deployment
![Alt text](./screenshots/publish_metrics.png)
8.







