Docker Proxy Configuration on vagrant-virtualbox-boxes 

1. Change the proxy settings in the Docker configuration file for docker engine: `/etc/systemd/system/docker.service.d/http-proxy.conf`

```shell    
[Service]
Environment="HTTP_PROXY=http://proxy61.iitd.ac.in:3128"
Environment="HTTPS_PROXY=http://proxy61.iitd.ac.in:3128"
Environment="NO_PROXY=localhost,127.0.0.1,docker-registry.example.com,.corp"
```

2. Change the proxy settings in the Docker configuration file `~/.docker/config.json`

```json    
{
  "proxies":{
    "default":{
      "httpProxy": "http://10.10.78.61:3128",
      "noProxy": ""
    }
  }
}
```


mysql installtaion on vagrant
```shell
mysql -u root -p password
```
