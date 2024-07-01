# 5G Core Network Setup Guide Open Air Interface

## June 29, 2024

## Important Links

- OpenAirInterface 5G Core Deployment with UERANSIM
- OAI 5G Core Deployment Documentation
- Docker Installation Guide
- Configure Docker Proxy

## Step 1: Installing Dependencies

1. Install Docker and Python:

```
$ sudo apt install docker.io
$ sudo apt install python
```
2. Login to Docker Hub and pull necessary images:

```
$ docker login
$ docker pull ubuntu:bionic
$ docker pull mysql:8.
$ docker logout
$ docker pull rohankharade/ueransim
$ docker image tag rohankharade/ueransim:latest ueransim:latest
$ While installing docker if getting following error.
```
```
{docker: Error response from daemon: Get
"https :// registry -1. docker.io/v2/":
net/http: request canceled bluewhile waiting bluefor
connection (Client.Timeout exceeded bluewhile awaiting
headers ). See ’docker run --help’.}
```

```
$ Setup proxy for docker to pull images
(https://docs.docker.com/config/daemon/systemd/#httphttps-proxy)
```
3. Clone the OAI official repository:

```
$ git clone https://gitlab.eurecom.fr/oai/cn5g/oai-cn5g-fed.git
$ git config --global http.proxy http://proxyuser:proxypwd@proxy62.iitd.ac.in:
```
4. Install Docker Compose:

```
$ cd /oai-cn5g-fed
$ sudo apt-get install docker-compose
```
5. Pulling the core docker images

```
$ docker login
#!/bin/bash
docker pull oaisoftwarealliance/oai-amf:v1.5.
docker pull oaisoftwarealliance/oai-nrf:v1.5.
docker pull oaisoftwarealliance/oai-spgwu-tiny:v1.5.
docker pull oaisoftwarealliance/oai-smf:v1.5.
docker pull oaisoftwarealliance/oai-udr:v1.5.
docker pull oaisoftwarealliance/oai-udm:v1.5.
docker pull oaisoftwarealliance/oai-ausf:v1.5.
docker pull oaisoftwarealliance/oai-upf-vpp:v1.5.
docker pull oaisoftwarealliance/oai-nssf:v1.5.
docker pull oaisoftwarealliance/oai-pcf:v1.5.
docker pull oaisoftwarealliance/oai-nef:v1.5.
docker pull oaisoftwarealliance/trf-gen-cn5g:latest
```
## Step 2: Configuration Update

Update the following in/conf/basicvppnrf.conf:

- supported_integrity_algorithms:
    - "NIA1"
    - "NIA2"
    - "NIA0"
- supported_encryption_algorithms:
    - "NEA1"
    - "NEA2"
    - "NEA0"


## Step 3: Running the OAI Simulator

For detailed instructions, refer here

1. Command for running 5G core services

```
$ cd oai-cng5g-fed/docker-compose
$ docker-compose -f docker-compose-basic-vpp-nrf.yaml up -d
```
2. Running the UERANSIM

```
$ cd oai-cng5g-fed/docker-compose
$ docker-compose -f docker-compose-ueransim-vpp.yaml up -d
```
3. Shutting down the UERANSIM and 5G core services

```
$ docker-compose -f docker-compose-basic-vpp-nrf.yaml down
$ docker-compose -f docker-compose-ueransim-vpp.yaml down
```


