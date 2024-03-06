# How to implement and run applications with docker or in a browser
With the following guide we are trying to simplify the process of running user applications further. This documentation is prepared by Tisha and Priyansh. 
This assumes that you have 
1. docker installed on the VM that is running UERANSIM
2. you have an active display and gui installed on the VM 

### 1.  Ensure Executable Permission for the binder:
```bash 
chmod +x nr-binder
```

### 2. Run the docker image of choice 
```bash
sudo ./nr-binder 10.45.0.3 docker run --name chrome  --privileged -p 3000:3000 -d tekfik/chrome
```

If you are behind a proxy and face this error :
> Unable to find image 'tekfik/chrome:latest'locally         
> docker: Error response from daemon: Get "https://registry-1.docker.io/v2/": net/http: request canceled while waiting for connection (Client.Timeout exceeded while awaiting headers).                              See 'docker run --help'.  

Use the following solution: 
> A. Open or create the Docker configuration file /etc/systemd/system/docker.service.d/http-proxy.conf 
```bash
sudo mkdir -p /etc/systemd/system/docker.service.d/
sudo nano /etc/systemd/system/docker.service.d/http-proxy.conf
```
> B. Add the following lines to the file:
```
[Service]
Environment="HTTP_PROXY=http://proxy62.iitd.ac.in:3128"
Environment="HTTPS_PROXY=http://proxy62.iitd.ac.in:3128"
(Replace with your proxy settings)
```
> C. Save the file and exit the editor and flush changes and restart Docker:
```bash
	sudo systemctl daemon-reload
	sudo systemctl restart docker

### 3. On your default browser visit the localhost:3000 to find the browser and run applications while capturing it in pcap files 
```
> D. Run the original command again
