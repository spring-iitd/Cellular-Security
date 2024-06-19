# 5G-and-Beyond

This repository was made to help us decrease the time it takes for us to set up a 5G core network. 
- `./configurations/` has files specific to a deployment that has been tested and runs. There can be some path dependencies that you might need to change. 
- `./shared/` is shared between the VMs and the host machine.
- `./docs/` has some documentation that might be useful.
- `./scripts/` has some scripts that might be useful.
---

## Setting up the environment
### Setting up the internet connection
- Ask Priyansh or Neha for access to `whitepaper`.
- `ssh` into the server. You will find `proxy.sh` in your home folder. 
- Make changes to the `proxy.sh` file. 
  - Change the proxy_add variable to match your Kerberos.
  - change the username and password per Kerberos.
  > Note: This is saved in plaintext; you can use alternate scripts such as [https://github.com/SkullTech/iitd-proxylogin](https://github.com/SkullTech/iitd-proxylogin). 
- Make changes to the `.bashrc` file.
  - Uncomment the export commands to your `.bashrc` file.
  - either log out and log in again or do `source ~/.bashrc`.
- Run the `proxy.sh` script as a background process.
  - Vagrant, Docker, Virtualbox, etc., should now be able to access the internet. If you need something installed, please contact Priyansh or Neha.
### Making virtual machine images 
We are using Vagrant to simplify the process of setting up the 5G core network. You need to add these images to your user to use them.

You can use the local images rather than downloading the images from the internet. 

```bash
$ vagrant box add /boxes/core.box --name core-nw --provider virtualbox --force --clean
$ vagrant box add /boxes/ran-ue.box --name ran-ue-nw --provider virtualbox --force --clean
$ vagrant plugin install vagrant-proxyconf
```

## Deploying the 5G Network
### Cloning the Repository
Clone the repository and follow the instructions in the README.md file.
```bash
$ git clone https://github.com/spg-iitd/Cellular-Security.git
$ cd Cellular-Security
```
### Booting and Logging into the System 
Most of the tasks that we shall be doing in this repository will be done on the virtual machine and you shall be ssh-ing into the VM. You can find a quick start guide for Vagrant [here](docs/vagrant_cheatsheet.md). Use the following command to boot the VM:
```shell 
$ vagrant up # starting the VMs
$ vagrant ssh [ran_ue_nw/core_nw] # logging into the VM
$ vagrant halt # stopping the VM
$ vagrant destroy -f # destroying the VM
```
- **core-nw**: This VM has the open5gs and free5gc installed. 
- The open5gs core network has 300 users, and it is already configured. 
- **ran-ue-nw**: This VM has the UERANSIM and PacketRusher installed.
### Setting up the 5G Core Network
You can ssh into the VM using `vagrant ssh core_nw`. Locate the configurations you would like to run. You can use the following commands to start the services:
```shell
$ open5gs-nrfd -c nrf.yaml 
$ open5gs-scpd -c scp.yaml 
$ open5gs-smfd -c smf.yaml 
$ open5gs-ausfd -c ausf.yaml 
$ open5gs-nssfd -c nssf.yaml 
$ open5gs-pcfd -c pcf.yaml 
$ open5gs-bsfd -c bsf.yaml 
$ open5gs-udmd -c udm.yaml 
$ open5gs-udrd -c udr.yaml 
$ open5gs-upfd -c upf.yaml 
$ open5gs-amfd -c amf.yaml 
```
> If you are getting errors while starting the services, like services aren't connecting to each other, or the services are not starting, check if there is a proxy set in the VM. You can check this by running `env | grep -i proxy` and unset the proxy by running `unset http_proxy https_proxy HTTP_PROXY HTTPS_PROXY`.
You may need to change the path of the configuration files. You can also run these processes in the background by adding `&` at the end of the command.
### Setting up the gNodeB and UE
You can ssh into the VM using `vagrant ssh ran_ue_nw`. Locate the configurations you would like to run. Locate the configurations you would like to run. You can use the following commands to start the services:
```shell
$ nr-gnb -c gnb.yaml 
$ sudo nr-ue -c ue.yaml 
```
> Confirm that the gNodeB and UE are connected by checking the logs and looking at the interfaces on the gNodeB. 
> You can further explore each of the config files to understand the parameters that are being used. `nr-cli` gives you a CLI to interact with the gNodeB and UE states. 

### Setting up the Internet Connection
You can use the following commands to check if the UE is successfully able to connect to the internet:
```shell
ping google.com -I uesimtun0
curl --interface uesimtun0 -X GET "https://httpbin.org/get"
```
> You may need to export proxy settings in the VM to access the internet.
```shell
export http_proxy=http:<proxy>:<port>
export https_proxy=http:<proxy>:<port>
# example: http://proxy61.iitd.ac.in:3128
```

