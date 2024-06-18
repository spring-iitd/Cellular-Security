# Open5GS Metrics
The following changes were made to get the metrics using Prometheus and Grafana:
1. While writing the configuration for the NFs, make sure that the metrics are enabled and are running on interface accessible to host. In this case it was all on eth0. 
2. Make sure that the ports for each service is unique and is not being used by any other service.
3. The configuration for the Prometheus and Grafana is provided in the metrics folder. Note, the prometheus.yml file has the IP address of the host machine. Make sure to change it to the IP address of the host machine.
4. Run using `docker-compose up -d` to start the services.
5. The Grafana dashboard can be accessed at `http://<host-ip>:3000` with username `admin` and password `admin`. The Prometheus dashboard can be accessed at `http://<host-ip>:9090`.
