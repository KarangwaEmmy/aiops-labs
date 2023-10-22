# AIOps Lab 2

## Description

A sandbox Docker Environment to experiment with Prometheus and Grafana

## How to get started

Clone the Repo: `git clone https://github.com/KarangwaEmmy/lab-2.git`

Start the demo cluster: `./bin/start`

Stop the demo cluster: `./bin/stop`

## Accessing Exposed Services

- Grafana `http://localhost:3000`
- Prometheus `http://localhost:9090`
- Prometheus Node Exporter `http://localhost:9100`
- Prometheus Postgres Exporter `http://localhost:9187`
- Prometheus Push Gateway `http://localhost:9091`
- Dummy Application Metrics `http://localhost:8000`

## Defaults

- Grafana credentials: `admin:admin`

# Lab Task – Basic Prometheus and Grafana

#### Start the sandbox by executing the bin/start
!['Start the sandbox'](./screenshots/start_bin.png)

#### Images in the docker desktop container
!['Docker Container Images'](./screenshots/docker.png)

#### Grafana Login
!['Grafana Login'](./screenshots/grafana%20login.png)

#### Prometheus 
!['Prometheus'](./screenshots/prometheus.png)

#### App One Metrics
!['App One metrics'](./screenshots/app_one%20Metrics.png)

#### Prometheus Node Exporter (Metrics)
!['Node Exporter Metrics'](./screenshots/Node_exporter_metrics.png)

#### Postgres exporter
!['Postgres exporter'](./screenshots/postgres_exporter_metrics.png)

#### Push Gateway
!['Push gateway'](./screenshots/push_gateway.png)



#### 4. Prometheus Demo Gauge graph (30 mins)
    demo_gauge
!['Demo Gauge'](./screenshots/prometheus_demo_gauge.png)

#### Prometheus Demo Gauge graph (15 mins)
    demo_gauge
![](./screenshots/prometheus_demo_gauge_15.png)

    db_backup_last_completion_timestamp_seconds
!['db_backup'](./screenshots/prom_db_backup.png)

    go_gc_duration_seconds
![Alt text](./screenshots/go_gc_duration_seconds.png)

    go_goroutines
![Alt text](./screenshots/prom_go_routine.png)

    go_memstats_heap_alloc_bytes
![Alt text](./screenshots/go_memstats_heap_alloc_bytes.png)

    process_cpu_seconds_total
![Alt text](./screenshots/prom_cpu.png)

    process_resident_memory_bytes
![Alt text](./screenshots/prom_memory.png)

#### 5. Grafana Dashboard
!['grafana Dashboard'](./screenshots/grafana_dashboard.png)
!['grafan Python'](./screenshots/Grafana_Python.png)

- Grafana Demo gauge app one Histogram
![Alt text](./screenshots/grafana_demo_gauge.png)

- Grafana Demo gauge app one Time Series
![Alt text](./screenshots/Grafana_demo_time_series.png)

- Grafana Process CPU
![Alt text](./screenshots/Grafana_process_cpu.png)
   scrape_duration_seconds
![Alt text](./screenshots/grafana_push_gateway.png)
`up`
![Alt text](./screenshots/grafana_up.png)

# Lab Task – Adding new metrics
1. Define two new metrics, for app1 updated code
![Alt text](./screenshots/updated_code.png)

2. Implement the metrics by running docker compose
![Alt text](./screenshots/docker_compose.png)
![Alt text](./screenshots/new_metrics.png)
![Alt text](./screenshots/histogram_bucket.png)
![Alt text](./screenshots/app_one_random_histogram_0_to_1_sum.png)
![Alt text](./screenshots/app_one_random_histogram_0_to_0_6_bucket.png)

3. Add custom panels in the Grafana dashboard to visualize
![Alt text](./screenshots/dashboard_1.png)
![Alt text](./screenshots/app_one_gauge_0_to_1.png)
![Alt text](./screenshots/app_one_gauge_0_to_0_6.png)



# Lab Task – Answer the following question
-  `Describe in writing the images created by docker compose and the running containers using Docker desktop or docker ps. Explain the contents of the dockercompose.yml file. Explain what network the containers are attached to`
## Images Created by Docker compose
- Images created after running docker compose
![Alt text](./screenshots/image.png)

## Explaination the contents of the dockercompose.yml file

1.  `version: "3.6":
`specifies the version of the Docker Compose file format being used
2. `services:` defines the various services (containers) that will be created and run as part of the application
3.     `app_one:`
- This service will be named "app_one" when it's running.
- It's built from the Dockerfile located in the "./containers/app_one" directory.
- It maps port 8000 on the host to port 8000 in the container.

4. `app_two:`
- This service will be named "app_two" when it's running.
- It's built from the Dockerfile located in the "./containers/app_two" directory.
- It maps port 8001 on the host to port 8001 in the container.
- It sets an environment variable DOCKER_NETWORK with the value "push_gateway:9091."

5. `prometheus:`
- This service will be named "prometheus" when it's running.
- It's built from the Dockerfile located in the "./containers/prometheus" directory.
- It maps port 9090 on the host to port 9090 in the container.

6. `grafana:`
- This service will be named "grafana" when it's running.
- It's built from the Dockerfile located in the "./containers/grafana" directory.
- It maps port 3000 on the host to port 3000 in the container.

7. `node_exporter:`
- This service will be named "prometheus_node_exporter" when it's running.
- It uses the pre-built/base-image image "quay.io/prometheus/node-exporter."
- It maps port 9100 on the host to port 9100 in the container.

8. `push_gateway:`
- This service will be named "prometheus_push_gateway" when it's running.
- It uses the pre-built image "prom/pushgateway."
- It maps port 9091 on the host to port 9091 in the container.

9.  `postgres:`
- This service will be named "postgres" when it's running.
- It uses the pre-built image "postgres:13.3."
- It maps port 5432 on the host to port 5432 in the container.
- It sets an environment variable POSTGRES_PASSWORD with the value "example."

10. `postgres_exporter:`
- This service will be named "postgres_exporter" when it's running.
- It uses the pre-built image "wrouesnel/postgres_exporter."
- It maps port 9187 on the host to port 9187 in the container.
- It sets an environment variable DATA_SOURCE_NAME to postgresql://postgres:example@postgres:5432/postgres?sslmode=disable` connect to the PostgreSQL database.