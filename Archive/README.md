# 5G-and-Beyond
This repository was made to help us decease the time it takes for us to setup a 5G core network. 
---

## Task 1: Steps to Install 
### Install Vagrant and Virtualbox  (or any other virtualisation tool of your choice)
- _On an Ubuntu machine_, you can run the following command to install virtualbox and vagrant:
  ```shell
  $ sudo apt-get install virtualbox vagrant
  ```
- _On a Windows machine,_ use the GUI to install [virtualbox](https://www.virtualbox.org/wiki/Downloads) and vagrant from [here](https://developer.hashicorp.com/vagrant/downloads).

### Clone this repository 
- Please install git and clone this repository. 
  ```shell
  $ git clone https://github.com/spg-iitd/Cellular-Security.git
  ```
> Note: If you would like to install both Open5GS and UERANSIM seperately, you can follow the instructions in the [docs](docs/) folder.

## Task 2:  Booting and Logging into the System 
Most of the tasks that we shall be doing in this repository will be done on the virtual machine and you shall be SSHing into the VM. So, in a terminal window on your host machine, cd into the repository folder, and use the following command to boot the VM:
```shell 
vagrant up # starting the VMs
vagrant ssh [name of the vm] # logging into the VM
vagrant halt # stopping the VM
vagrant destroy -f # destroying the VM
```
You can find a quickstart guide for Vagrant [here](docs/vagrant_cheatsheet.md). You will find vagrant files for open5gs and ueransim already made in the virtual-machine-installation folder. 

## Task 3: Setting up the 5G Core Network

SSH into your machine which has the Open5GS machine, you should explore the folder `open5gs/install/`. You'll find configuration settings in `etc` folder and binaries in `bin`. Make the edits to both as per requirement and start the services one after the other. 
You can run the following commands to start the services:
```shell
sudo ./open5gs-nrfd & 
sudo ./open5gs-scpd & 
sudo ./open5gs-smfd & 
sudo ./open5gs-ausfd & 
sudo ./open5gs-nssfd & 
sudo ./open5gs-pcfd & 
sudo ./open5gs-bsfd & 
sudo ./open5gs-udmd & 
sudo ./open5gs-udrd & 
sudo ./open5gs-upfd & 
sudo ./open5gs-amfd & 
```
By default the configuration file will be taken from the `open5gs/install/etc/open5gs/` folder. You can change the location of the configuration file by using the `-c` flag. 

## Task 4: Setting up the gNodeB and UE
SSH into your machine which has the UERANSIM installed, you should explore the folder `UERANSIM/`. If the installation was done correctly, you should see a `build` folder with the binaries for all the 5G core services. You can run the following commands to start the services:
```shell
./build/nr-gnb -c config/open5gs-gnb.yaml &
./build/nr-ue -c config/open5gs-ue.yaml &
``` 
> Confirm that the gNodeB and UE are connected by checking the logs and looking at the interfaces on the gNodeB. You can further explore each of the config files to understand the parameters that are being used. `nr-cli` gives you a CLI to interact with the gNodeB and UE states. 

## Task 5: Setting up the Internet Connection
If you are using the two VM setup, you can use the following commands to check if the UE is sucessfully able to connect to the internet :
```shell
ping google.com -I uesimtun0
curl --interface uesimtun0 -X GET "https://httpbin.org/get"
```

---
## References 
1. https://github.com/eatsan/open5gs-ueransim-vagrant-config
2. https://open5gs.org/open5gs/docs/guide/02-building-open5gs-from-sources/

## FAQs 
1. In case of an SCTP error, set the NatNetwork address in the Oracle VM box(/tools/network) to 192.168.56.0/24. Then for both VMs select the network attached to  'NAT network' and promiscuous mode to 'allow all '

