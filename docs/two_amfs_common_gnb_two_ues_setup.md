## Two AMFs, Common gNB and Two UEs Setup - Open5GS and UERANSIM

<u>**Pre-requisites:**</u> This guide assumes that you have already went through and understood the [two_vm_setup_sliced_core.md](https://github.com/spring-iitd/Cellular-Security/blob/main/docs/two_vm_setup_sliced_core.md) doc. Hence, this guide might skip through some basic steps (e.g. proxy setup, debugging issues related to running 5G Core services, etc.)

<u>**Overview:**</u> The goal of this guide is to help you set up a connection between two UEs and two AMFs using a common intelligent gNB. The UEs requests for two disctint slices, i.e., `ue1` requests for slice with sst `1` and `ue2` requests for slice with sst `2`. `amf1` supports only slice `1` and `amf2` only supports slice `2`. Hence, the gNB must "intelligently" route the registeration requests to the appropriate AMF, depending on the slice type requested by the UE.



### Part A) Initializing open5gs and UERANSIM VMs:

1. SSH into to your Ubuntu VM via forwarded ports, clone the repo and, navigate into it using the following commands:

```sh
ssh -L 9999:localhost:8888 <username>@<private_ip>
https://github.com/spring-iitd/Cellular-Security.git
cd Cellular-Security
```

2. Boot up your vagrant machine. The Vagrantfile is configured to automatically provide you the correct static IPs, according to the IPs mentioned in the corresponding YAML configuration files.

```sh
vagrant up
```

### <u>Possible Errors:</u> 

* <u>Error 1:</u> If you encounter an error during `vagrant up` such as:

<span style="color: red;"> The VirtualBox VM was created with a user that doesn't match the current user running Vagrant. VirtualBox requires that the same user be used to manage the VM that was created. Please re-run Vagrant with that user. This is not a Vagrant issue. </span>

<span style="color: red;"> The UID used to create the VM was: 1001
Your UID is: 1002 </span>

=> Simply remove the temporary vagrant metadata and state information as:

```sh
rm -rf .vagrant/
```

* <u>Error 2:</u> If you encounter an error during `vagrant up` such as:

<span style="color: red;"> A VirtualBox machine with the name 'core_nw' already exists.
Please use another name or delete the machine with the existing
name, and try again. </span>

=> List all your VMs and delete the unwanted VMs using their VM-ID as:

```sh
vboxmanage list vms
vboxmanage controlvm <VM-ID> poweroff
vboxmanage unregistervm <VM-ID> --delete
```

### Part B) Modifying open5gs database and running core services:

1) SSH into the open5gs VM as:

```sh
vagrant ssh core_nw
```

2) The open5gs VM automatically creates approx. 300 users. We will first delete them all and then, set up only two users, for the sake of simplicity. So, run:

```sh
cd shared/
./del_all_users.sh
```
* Note that this might take a while. It is recommended to run the above script twice, until you see no users in the database using  the `open5gs-dbctl showall` command.

3) Now, we will add two users as:

```sh
sudo open5gs-dbctl add 999700000000001 465B5CE8B199B49FAA5F0A2EE238A6BC E8ED289DEBA952E4283B54E88E6183CA
sudo open5gs-dbctl add 999700000000002 465B5CE8B199B49FAA5F0A2EE238A6BC E8ED289DEBA952E4283B54E88E6183CA
```

4) Now, open the index.js file as:

```sh
cd ~/open5gs/webui/server/
vi index.js
```

5) Ensure that you have the `_hostname` and `port` variables set as:

```sh
const _hostname = process.env.HOSTNAME || '0.0.0.0';
const port = process.env.PORT || 9999;
```

6) Now, launch the webui as:

```sh
cd ~/open5gs/webui/
npm ci
npm run dev
```

7) Now, run a browser on your parent system <i>(the system on which you are running the terminal)</i> and launch webui by going to `http://localhost:9999`. Type `admin` as username and `1423` as password. 
 
8) Now, you should see the two UEs you created in the GUI. Click on `999700000000002` UE and edit it. Scroll down and set the sst option to `2`, by clicking on the corresponding radio button. Save your subscriber changes and move back to the open5gs terminal.

9) Kill the webui using `CTRL+C` and naviagte to the folder containing the YAML configurations as:

```sh
cd ~/configurations/basic-configuration/open5gs/
```

10) Unset the environment variables for proxy, using the following command:

```sh
unset http_proxy https_proxy ftp_proxy no_proxy HTTP_PROXY HTTPS_PROXY FTP_PROXY NO_PROXY
```

11) Run all the 5G core services on this terminal. Thereafter, you can also check the status, i.e., if all the unique 11 Network functions are up and running, or not, using the following commands:

```sh
./run_all_srv.sh
./check_srv_status.sh
```

### Part C) Setting up gNB and registering the two UEs:

1) Now, start another parallel terminal <i>(preferrably using tmux/terminator on Ubuntu or, using iTerm on OSX, etc.)</i>. We used the first terminal to simulate the 5G Core Network (CN). We will use the second terminal to simulate the Radio Access Network (RAN).

2) SSH into to your Ubuntu VM via forwarded ports and, navigate into the repo using the following commands:

```sh
ssh -L 9999:localhost:8888 <username>@<private_ip>
cd Cellular-Security
```

3) SSH into the UERANSIM VM as:

```sh
vagrant ssh ran_ue_nw
```

4) Naviagte to the folder containing the YAML configurations as:

```sh
cd ~/configurations/basic-configuration/ueransim/
```

5) Setup the gNB and the connect the UEs with the following command:

```sh
./setup_gnb_and_two_ues.sh
```

* Congratulations! You have successfully connected two UEs, requesting for two different slices, to two AMFs serving two distinct slices, via a common intelligent gNB. Feel free to verify the connections using the `nr-cli` tool.