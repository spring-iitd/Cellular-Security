# Docker Rootless for Whitepaper 

## Install Process
Run the following commands to install docker-rootless. 
```shell
dockerd-rootless-setuptool.sh install
```
Usage
The systemd unit file is installed as ~/.config/systemd/user/docker.service.

```shell
systemctl --user start docker
systemctl --user enable docker
```
Note: Add the following in your .bashrc file, to set the context, path, and host. 
```bash
docker context use rootless

#[INFO] Make sure the following environment variable(s) are set (or add them to ~/.bashrc):
export PATH=/usr/bin:$PATH

#[INFO] Some applications may require the following environment variable too:
export DOCKER_HOST=unix:///run/user/1001/docker.sock
```

## Setting-up Proxy

1. Create a systemd drop-in directory for the docker service:
```shell
mkdir -p ~/.config/systemd/user/docker.service.d
```
2. Create a file named ~/.config/systemd/user/docker.service.d/http-proxy.conf that adds the HTTP_PROXY environment variable:
```shell
[Service]
Environment="HTTP_PROXY=http://10.10.78.61:3128"
Environment="HTTPS_PROXY=http://10.10.78.61:3128"
```
3. Flush changes and restart Docker
```shell
systemctl --user daemon-reload
systemctl --user restart docker
```
4. Verify that the configuration has been loaded and matches the changes you made, for example:
```shell
systemctl --user show --property=Environment docker
```


---
References:
1. https://docs.docker.com/config/daemon/systemd/#httphttps-proxy
2. https://docs.docker.com/engine/security/rootless/
