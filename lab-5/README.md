## Lab 5: Capturing application metrics with Istio service mesh

#### Lab Task 1 – Install and configure the Boutique application
![Alt text](./screenshots/creating_new_cluster.png)
![Alt text](./screenshots/deployment.png)

![Alt text](./screenshots/get_deployed_services.png)
![Alt text](./screenshots/get_pods.png)
![Alt text](./screenshots/get_deployments.png)
![Alt text](./screenshots/compute_firewall_rules_list.png)

#### Lab Task 2
- 1 Install the addons
![Alt text](./screenshots/deploy_istio_addons.png)

- 2 Start the Prometheus, Kiali and Grafana dashboards
![Alt text](./screenshots/run_prometheus_dashboard.png)
![Alt text](./screenshots/run_grafana_dashboard.png)
![Alt text](./screenshots/Run_Kiali_Dashboard.png)

- Create a simple Prometheus query
    productcatalogservice query
![Alt text](./screenshots/productcatalogueservice_query.png)

![Alt text](./screenshots/destination_canonical_service_checkout_service.png)

![Alt text](./screenshots/destination_canonical_service_frontend.png)

![Alt text](./screenshots/destination_canonical_service_recommendation_service.png)

#####  Grafana dashboard
![Alt text](./screenshots/grafana_visualization.png)

## 7
![Alt text](./screenshots/histogrm_quantile_prometheus.png)

### 8
![Alt text](./screenshots/grafana_gaue.png)

![Alt text](./screenshots/grafana_time_series.png)

### 9
![Alt text](./screenshots/scaling_loadgenerator.png)
![Alt text](./screenshots/2_replicas_scalling.png)
![Alt text](./screenshots/scaling_to_2_replicas.png)
![Alt text](./screenshots/scalling_down.png)

## Lab Task 3 (From Kiali exploration)
![Alt text](./screenshots/Kiali_dashboard_graphs.png)

- addservice
![Alt text](./screenshots/adservice_details.png)
![Alt text](./screenshots/addservice_trace.png)

- cartservice
![Alt text](./screenshots/cartservice_details.png)
![Alt text](./screenshots/cartservice_trace.png)


## Lab Task 4
- Deploying Delay 0.2 seconds
![Alt text](./screenshots/delay_2s.png)
![Alt text](./screenshots/2_delay.png)


- Deploying Delay 0.4 seconds
![Alt text](./screenshots/delay_4s.png)
![Alt text](./screenshots/4_delay.png)

- screen shot from Kiali showing shipping service response times to the Source.
![Alt text](./screenshots/shipping_service_kiali.png)
![Alt text](./screenshots/time_bound.png)
![Alt text](./screenshots/traces.png)
![Alt text](./screenshots/traffic.png)
![Alt text](./screenshots/Request_duration.png)
![Alt text](./screenshots/source.png)
### Shut down the cluster
    kubectl delete -k .
![Alt text](./screenshots/delete_cluster.png)

    kubectl delete -f /sample/addons
![Alt text](./screenshots/delete_istio.png)

- Delete cluster
    gcloud container clusters delete lab5    --project=aiops-400918     --zone=us-central1-a

