# Open5gs and UERANSIM setup via Docker

This guide provides detailed instructions for setting up `Open5gs` services and `UERANSIM` services as dedicated [docker](https://www.docker.com) containers, as per this [repo](https://github.com/herlesupreeth/docker_open5gs), on machines using IITD LAN.

## Setting up Docker

> <u>**Pre-requisites:**</u>

- You are expected to setup IITD proxy, as specified [here](https://csc.iitd.ac.in/uploads/proxy_help.pdf), on your machine and it should be able to access WAN via CLI.

1. Setup the docker's apt repository on your system, using the following commands:

```sh
sudo -E apt-get update && sudo -E apt-get upgrade
sudo -E apt-get install ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo -E curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "${UBUNTU_CODENAME:-$VERSION_CODENAME}") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo -E apt-get update
```

2. Install Docker packages on your system and verify installation as:

```sh
sudo -E apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
docker --version                    # For Docker version
sudo systemctl status docker        # For Docker Daemon
sudo docker info                    # For Docker CLI
docker buildx version               # For Docker Buildx
docker compose version              # For Docker Compose
```

- <u>_Note-1:_</u> The Docker daemon binds to a Unix socket, not a TCP port. By default it's the root user that owns the `Unix` socket in linux, and other users can only access it using `sudo`. The Docker daemon always runs as the root user. So, to prevent using `sudo` with every docker command, create a Unix group called `docker` and add `users` to it as:

```sh
sudo groupadd docker
sudo usermod -aG docker $USER
newgrp docker
```

- <u>_Note-2:_</u> Also, change the ownership of `~/.docker/` directory as:

```sh
mkdir -p ~/.docker
sudo chown "$USER":"$USER" /home/"$USER"/.docker -R
sudo chmod g+rwx "$HOME/.docker" -R
```

At this point, you should be able to run basic docker commands like `docker container ls`, `docker images`, etc. (even without prefixing them with `sudo`), but you still need to configure docker to send all the `HTTP` and `HTTPS` requests via the `IITD Proxy` server.

## Configuring IITD Proxy for Docker Daemon and CLI

1. The `Docker daemon (dockerd)` will use our proxy server to access images stored on `Docker Hub` and other registries, and to reach other nodes in a `Docker swarm`. So, setup proxy configurations for docker daemon as:

```sh
sudo vi /etc/docker/daemon.json
```

2. Add the following proxy configuration information and save it:

```sh
{
  "proxies": {
    "http-proxy": "http://10.10.78.62:3128",
    "https-proxy": "http://10.10.78.62:3128",
    "no-proxy": "*.test.example.com,.example.org,127.0.0.0/8,172.*.*.*"
  }
}
```

- <u>_Note:_</u> The proxy IP address will vary depending on your degree.  
  e.g.  
  For a B.Tech student -> http://10.10.78.22:3128  
  For a Dual Degree / M.Tech student -> http://10.10.78.62:3128  
  For a PhD student -> http://10.10.78.61:3128

3. Restart the docker daemon for proxy configurations to take effect and verify them, using the following commands:

```sh
sudo systemctl daemon-reload
sudo systemctl restart docker
docker info | grep -i proxy
```

4. Similarly, set up the proxy configurations for `Docker CLI` in the `~/.docker/config.json` file as:

```sh
sudo vi ~/.docker/config.json
```

```sh
{
 "proxies": {
   "default": {
     "http-proxy": "http://10.10.78.62:3128",
     "https-proxy": "http://10.10.78.62:3128",
     "no-proxy": "*.test.example.com,.example.org,127.0.0.0/8,172.*.*.*"
   }
 }
}
```

4. Now, verify the docker installation by downloading a test image and running it as a container as:

```sh
docker run hello-world
```

Now, the docker services are successfully setup on your IITD machine. Let's set up `Open5gs` and `UERANSIM` now.

## Setting up Open5gs and UERANSIM via Docker

1. To clone the repository into the `~/Desktop/` directory, run the following commands:

```sh
cd ~/Desktop/
git clone https://github.com/spring-iitd/5G-Registration-Attack.git
```

2. Move into the appropriate folder, pull the base images, tag them with simpler image names and verify your modifications using the following commands:

```sh
cd docker_open5gs/

docker pull ghcr.io/herlesupreeth/docker_open5gs:master
docker tag ghcr.io/herlesupreeth/docker_open5gs:master docker_open5gs

docker pull ghcr.io/herlesupreeth/docker_grafana:master
docker tag ghcr.io/herlesupreeth/docker_grafana:master docker_grafana

docker pull ghcr.io/herlesupreeth/docker_metrics:master
docker tag ghcr.io/herlesupreeth/docker_metrics:master docker_metrics

docker pull ghcr.io/herlesupreeth/docker_ueransim:master
docker tag ghcr.io/herlesupreeth/docker_ueransim:master docker_ueransim

docker images
```

3. Export the environment variables, temporarily disable firewall and enable IP forwarding between network interfaces as:

```sh
set -a
source .env
set +a
sudo ufw disable
sudo sysctl -w net.ipv4.ip_forward=1
```

4. Build the docker images for the remaining additional components using the following command:

```sh
# For 5G deployment only
docker compose -f sa-deploy.yaml build \
  --build-arg HTTP_PROXY=http://10.10.78.62:3128 \
  --build-arg HTTPS_PROXY=http://10.10.78.62:3128 \
  --build-arg NO_PROXY="localhost,127.0.0.1,*.local,10.0.0.0/8,172.*.*.*"
```

## 5G SA Deployment

1. Find your machine ip using `hostname -I` or `ip a` command and then edit the following parameters in your `.env` file:

```sh
# Change this to the IP address of the host running 5GC
DOCKER_HOST_IP=10.237.27.32

# Change this to value of DOCKER_HOST_IP
UPF_ADVERTISE_IP=10.237.27.32
```

2. Under `amf` section in docker compose file (`sa-deploy.yaml`), uncomment the following part:

```sh
...
    ports:
      - "38412:38412/sctp"
...
```

3. Then, uncomment the following part under `upf` section:

```sh
...
    ports:
      - "2152:2152/udp"
...
```

4. Deploy the 5G core network services as:

```sh
source .env
docker compose -f sa-deploy.yaml up -d
```

5. Now, open a browser on your client machine (your `local` machine that you are using to `SSH` into your `Ubuntu` machine) and go to http://<DOCKER_HOST_IP>:9999 (e.g. http://10.237.27.32:9999) and access the Open5gs `webui`.

6. Login using the following credentials:

```sh
Username -> admin
Password -> 1423
```

7. Create a new subscriber using the `+` icon, with following details, and save the entry:

```sh
IMSI -> 001011234567895
Subscriber Key (K) -> 8baf473f2f8fd09487cccbd7097c6862
Authentication Management Field (AMF) -> 8000
USIM Type -> OP
Operator Key (OPc/OP) -> 11111111111111111111111111111111
```

- <u>_Note:_</u> Alternatively, you can also use `open5gs-dbctl` commands to manipulate the Open5gs database, using CLI.

8. Then, close all the existing running containers using the following command:

```sh
docker container rm -f $(docker container ls -aq)
```

9. Finally, open 3 separate terminals. SSH into your machine in all three terminals and run the following commands:

```sh
# In the first terminal, run the 5G Core Network as:
source .env
docker compose -f sa-deploy.yaml up

# In the second terminal, run the UERANSIM gNB (RF simulated) as:
docker compose -f nr-gnb.yaml up -d && docker container attach nr_gnb

# In the third terminal, run the UERANSIM NR-UE (RF simulated) as:
docker compose -f nr-ue.yaml up -d && docker container attach nr_ue
```

10. You can also manually see the console logs to verify a successful setup:

- All your core network services, in the first terminal, should be successfully running, without any `ERROR:` message.
- Your `gNB`, in the second terminal, should depict a `[ngap] [info] PDU session resource(s) setup for UE[1] count[1]` message, or a similar message.
- Your `UE`, in the third terminal, should depict a `[app] [info] Connection setup for PDU session[1] is successful, TUN interface[uesimtun0, 192.168.100.2] is up.` or, a similar message.

## Common Errors and Bug Fixes:

- <u>**Bug-1:**</u> If you recieve a **port binding conflict error** such as the one shown below:

```sh
Error response from daemon: failed to set up container networking: driver failed programming external connectivity on endpoint metrics (39937d4445bb3d14f36786d2256c5bde996118f46165f33966ca8cb67696f4b6): failed to bind host port for 0.0.0.0:9090:172.22.0.36:9090/tcp: address already in use
```

Simply remove the pre-installed `Open5gs` services that are set up to auto-start on every boot as:

```sh
sudo apt remove open5gs
sudo apt auto-remove
```

If the issue still persists, manually remove any other service that might be blocking these ports by first finding its process ID using `lsof` and kill it as:

```sh
sudo lsof -i :9090
sudo pkill -9 <process ID> <process name>
```

- <u>**Bug-2:**</u> If you recieve a **Connection timer expired error**, while running core network services, such as the one shown below:

```sh
[sbi] INFO: [6d1e3dc2-7aff-41ee-a8c6-cbfd6cf72c36] NF de-registered (../lib/sbi/nf-sm.c:241)
[sbi] ERROR: Connection timer expired (../lib/sbi/client.c:542)
```

Simply unset your environment variables using the following commands:

```sh
unset http_proxy https_proxy ftp_proxy no_proxy HTTP_PROXY HTTPS_PROXY FTP_PROXY NO_PROXY
```

Ensure that no other environment variables are set, that is forcing the docker containers of the core network to forward the HTTP requests among themselves, to IITD proxy server.

- <u>**Bug-3:**</u> If you recieve a **HTTP 302 redirection response status code**, while running core network services, such as the one shown below:

```sh
[smf] ERROR: HTTP response error : 302 (../src/smf/smf-sm.c:685)
```

Simply open the `sa-deploy.yaml` file and add the `no_proxy` variable, explicitly to each container, wherever you find the `environment` key as:

```sh
...
environment:
      - COMPONENT_NAME=nrf
      - no_proxy="172.*.*.*"
...
```

This would force the containers to not forward HTTP requests (used for internal communication) to IITD proxy server and one can also verify it by launching `/bin/bash` for every container and checking its environment variables using the following commands:

```sh
docker exec -it amf /bin/bash
env | grep -i proxy
```

## Author & Contributors

> Prateek Bhaisora _(2023JCS2564)_ <br>
> IIT Delhi SPRING Group ([spring-iitd](https://github.com/spring-iitd)) <br>
> GitHub Profile Link: [prateekbhaisora](https://github.com/prateekbhaisora)
