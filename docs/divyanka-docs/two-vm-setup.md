# Two VM Setup - Open5GS and UERANSIM

## 1. Installation and Configuration of the Cellular-Security Repository
Make sure you have access to Whitepaper (IITD Lab Machine) before doing this. You need to be on the IITD network. SSH into the lab machine:
```bash
ssh <your_username>@<whitepaperIP>
```

Before this, make sure you have internet access in the machine, using [IITD Proxy](https://csc.iitd.ac.in/uploads/proxy_help.pdf).
Test it out using `wget google.com` or `ping google.com`.

Clone the existing IITD Cellular Security Repo:
```bash
git clone https://github.com/spg-iitd/Cellular-Security/tree/main
~/Cellular-Security/virtual-machine-installation/ueransim
vagrant up
```
Open a new terminal window
```bash
~/Cellular-Security/virtual-machine-installation/open5gs
```
Open `Vagrantfile` in the `open5gs` folder and note the port speicified in your open5GS vagrant file infront of `host` in the following line (if the line doesn't exist, add it at the appropirate location):

```yaml
open5gs.vm.network "forwarded_port", guest: 9999, host: 9999
```
Now, exit the SSH, open a new terminal and use the following command to ssh into your IITD Lab machine, or Whitepaper:
```
ssh -L 9999:localhost:9999 divyanka@10.237.27.48
```
or replace `9999` with any port specified in your open5GS vagrant file infront of `host` in the line above. Replace `divyanka` with your username.


3. Now, on both the seperate terminals (with open5gs and ueransim folders), do `vagrant ssh` and each. You'll ssh into the machines.

```bash
vagrant@ubuntu2204:~$ ls
index.html  open5gs  scripts  shared
```
```bash
vagrant@ubuntu2204:~$ ls
scripts  shared  UERANSIM
```

## 2. Setup Open5GS Configuration


```bash
vagrant@ubuntu2204:~/open5gs/install/etc/open5gs$ ls
amf.yaml  ausf.yaml  bsf.yaml  hnet  hss.yaml  mme.yaml  nrf.yaml  nssf.yaml  pcf.yaml  pcrf.yaml  scp.yaml  sepp1.yaml  sepp2.yaml  sgwc.yaml  sgwu.yaml  smf.yaml  tls  udm.yaml  udr.yaml  upf.yaml
```
Modify `amf.yaml` and `upf.yaml` files.

```yaml
# amf config file locates in /etc/open5gs/amf.yaml
amf:
  sbi:
    server:
      - address: 127.0.0.5
        port: 7777
    client:
      nrf:
        - uri: http://127.0.0.10:7777
      scp:
        - uri: http://127.0.0.200:7777
  ngap:
    server:
      - address: 192.168.56.100 # open5gs VM address, can be found in open5gs Vagrantfile
  metrics:
    server:
      - address: 127.0.0.5
        port: 9090
```

```yaml
# upf config file locates in /etc/open5gs/upf.yaml
upf:
  pfcp:
    server:
      - address: 127.0.0.7
    client:
#      smf:     #  UPF PFCP Client try to associate SMF PFCP Server
#        - address: 127.0.0.4
  gtpu:
    server:
      - address: 192.168.56.100 # open5gs VM address, can be found in open5gs Vagrantfile
  session:
    - subnet: 10.45.0.1/16
    - subnet: 2001:230:cafe::1/48
  metrics:
    server:
      - address: 127.0.0.7
        port: 9090

```
Let everything else remain the default configuration.

## 3. NAT Port Forwarding

In order to bridge between the 5G Core UPF and WAN(Internet), I need enable IP forwarding and add a NAT rule to the IP Tables. Following are the NAT port forwarding I have done. Without this port forwarding the connectivity from 5G Core to internet would not work.

```bash
# nat port forwarding
sudo sysctl -w net.ipv4.ip_forward=1
sudo iptables -t nat -A POSTROUTING -o enp0s3 -j MASQUERADE
sudo systemctl stop ufw
sudo iptables -I FORWARD 1 -j ACCEPT

# if above setup not works try to manually create tun interface and do nat forwarding
sudo ip tuntap add name ogstun mode tun
sudo ip addr add 10.45.0.1/16 dev ogstun
sudo ip addr add 2001:230:cafe::1/48 dev ogstun
sudo ip link set ogstun up
```

## 4. Install dependencies and disable proxy

Before this, make sure you have internet access in the VM, using [IITD Proxy](https://csc.iitd.ac.in/uploads/proxy_help.pdf).
Test it out using `wget google.com` or `ping google.com`.

Install NodeJS:
```bash
# install nodejs
sudo apt update
sudo apt upgrade
sudo apt install curl
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt install nodejs
```
Now `cd` into the following folder and
``` bash
vagrant@ubuntu2204:~/open5gs/webui$
```
and run these commands

```
cd webui
npm install
npm audit fix

```
We're done with internet use in the Open5GS VM. *Disable* firewall:

```bash
sudo ufw disable
```

Now, after this, *DISABLE* IITD proxy. Comment out anything you added in `.bashrc` (if you did) and login again. Logout of your open5GS VM, and `vagrant reload` and `vagrant ssh`. Make sure `ping google.com` *doesn't* run.

## 5. Start the Open5GS services one-by-one
Start the following commands one by one (line by line) and see if you get error at any point.

```bash
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
At any point, if you get any error, kill all of them by using `sudo pkill -9 open5gs`, resolve the error and try one-by-one again. Once you run all of them successfully, you can use all the commands at once the next time.

### Error Example: 
Now, I got an error while running `sudo ./open5gs-pcfd & ` 
```bash
<p><b>Connection to 127.0.0.4 failed.</b></p>
</blockquote>

<p id="sysmsg">The system returned: <i>(111) Connection refused</i></p>

<p>The remote host or network may be down. Please try the request again.</p>

<p>Your cache administrator is <a href="mailto:webmaster?subject=CacheErrorInfo%20-%20ERR_CONNECT_FAIL&amp;body=CacheHost%3A%20localhost%0D%0AErrPage%3A%20ERR_CONNECT_FAIL%0D%0AErr%3A%20(111)%20Connection%20refused%0D%0ATimeStamp%3A%20Wed,%2010%20Apr%202024%2005%3A58%3A41%20GMT%0D%0A%0D%0AClientIP%3A%2010.237.27.48%0D%0AServerIP%3A%20127.0.0.4%0D%0A%0D%0AHTTP%20Request%3A%0D%0APOST%20%2Fnnrf-nfm%2Fv1%2Fnf-status-notify%20HTTP%2F1.1%0AProxy-Connection%3A%20Keep-Alive%0D%0AAccept%3A%20application%2Fproblem+json%0D%0A3gpp-sbi-sender-timestamp%3A%20Wed,%2010%20Apr%202024%2005%3A57%3A50.418%20GMT%0D%0A3gpp-sbi-max-rsp-time%3A%2010000%0D%0AContent-Type%3A%20application%2Fjson%0D%0AContent-Length%3A%20816%0D%0AUser-Agent%3A%20NRF%0D%0AHost%3A%20127.0.0.4%3A7777%0D%0A%0D%0A%0D%0A">webmaster</a>.</p>

<br>
</div>

<hr>
<div id="footer">
<p>Generated Wed, 10 Apr 2024 05:58:41 GMT by localhost (squid/3.1.19)</p>
<!-- ERR_CONNECT_FAIL -->
</div>
</body></html>
] (../lib/sbi/message.c:1373)
04/10 05:57:50.422: [sbi] ERROR: parse_content() failed (../lib/sbi/message.c:1006)
04/10 05:57:50.422: [nrf] ERROR: cannot parse HTTP response (../src/nrf/sbi-path.c:148)c:148)
```
**Source of error:** Proxy blocking connection
**Resolve the error:** Disable proxy as mentioned earlier.


## 6. Register UE Device on Open5GS WebUI

### Understanding Port Fowarding between Whitepaper and Your machine
**Here's the tricky part:** since we're are ssh-ing twice (one into the whitepaper and then into vagrant), it becomes difficult for us to forward ports. We have to do it twice. 

```
A (your machine) --ssh--> B (whitepaper machine) --vagrant ssh--> C (open5gs vagrant on whitepaper)

```
Now, to forward port from `C` to `B` we use vagrant configuration `open5gs.vm.network "forwarded_port", guest: 9999, host: 9999`. Now, to forward from `B` to `A` we use `ssh -L 9999:localhost:9999 divyanka@10.237.27.48`. 

### Starting the WebUI

``` bash
vagrant@ubuntu2204:~/open5gs/webui$
```
Now, in that folder,

```bash
# clone webui
# git clone https://github.com/open5gs/open5gs.git

# run webui with npm
cd webui


npm run dev --host 0.0.0.0
# the web interface will start on
# You need to check where it starts because of the multiple port forwarding we did
http://localhost:9999/

# webui login credentials
username - admin
password - 1423

# add new subscriber
# the default device information can be found in open5gs config on UERANSIM in Step 5
# IMSI = [MCC|MNC|MSISDN], for us mcc=999 and mnc=70
IMSI: 999700000000001
Subscriber Key: 465B5CE8B199B49FAA5F0A2EE238A6BC
USIM Type: OPc
Operator Key: E8ED289DEBA952E4283B54E88E6183CA

```

## 7. Setup gNB and UE

Now, go to your other terminal with UERANSIM VM:
```bash
vagrant@ubuntu2204:~/UERANSIM/config$ ls
custom-gnb.yaml  custom-ue.yaml  free5gc-gnb.yaml  free5gc-ue.yaml  open5gs-gnb.yaml  open5gs-ue.yaml
```
Modify the following files:

```yaml
# open5gs-gnb.yaml

mcc: '999'          # Mobile Country Code value
mnc: '70'           # Mobile Network Code value (2 or 3 digits)

nci: '0x000000010'  # NR Cell Identity (36-bit)
idLength: 32        # NR gNB ID length in bits [22...32]
tac: 1              # Tracking Area Code

# IP address of the UERANSIM VM, found in ueransim vagrantfile
linkIp: 192.168.56.120   # gNB's local IP address for Radio Link Simulation (Usually same with local IP)
ngapIp: 192.168.56.120   # gNB's local IP address for N2 Interface (Usually same with local IP)
gtpIp: 192.168.56.120    # gNB's local IP address for N3 Interface (Usually same with local IP)

# List of AMF address information
amfConfigs:
  - address: 192.168.56.100 # open5gs VM address, can be found in open5gs Vagrantfile
    port: 38412
```
```yaml
# open5gs-ue.yaml

# IMSI number of the UE. IMSI = [MCC|MNC|MSISDN] (In total 15 digits)
supi: 'imsi-999700000000001'
# Mobile Country Code value of HPLMN
mcc: '999'
# Mobile Network Code value of HPLMN (2 or 3 digits)
mnc: '70'
# SUCI Protection Scheme : 0 for Null-scheme, 1 for Profile A and 2 for Profile B
protectionScheme: 0
# Home Network Public Key for protecting with SUCI Profile A
homeNetworkPublicKey: '5a8d38864820197c3394b92613b20b91633cbd897119273bf8e4a6f4eec0a650'
# Home Network Public Key ID for protecting with SUCI Profile A
homeNetworkPublicKeyId: 1
# Routing Indicator
routingIndicator: '0000'

# Permanent subscription key
key: '465B5CE8B199B49FAA5F0A2EE238A6BC'
# Operator code (OP or OPC) of the UE
op: 'E8ED289DEBA952E4283B54E88E6183CA'
# This value specifies the OP type and it can be either 'OP' or 'OPC'
opType: 'OPC'
# Authentication Management Field (AMF) value
amf: '8000'
# IMEI number of the device. It is used if no SUPI is provided
imei: '356938035643803'
# IMEISV number of the device. It is used if no SUPI and IMEI is provided
imeiSv: '4370816125816151'

# List of gNB IP addresses for Radio Link Simulation
gnbSearchList:
  - 192.168.56.120 # ueransim VM address, can be found in ueransim Vagrantfile
```

Let all the other configuration be the default configuration.

## 8. Test 5G Network

1. **Internet Access**: Now, use proxy configuation again and add internet access to the UERANSIM VM:  [IITD Proxy](https://csc.iitd.ac.in/uploads/proxy_help.pdf). Test it out using `wget google.com` or `ping google.com`.
2. **Run UERANSIM**: On the UERANSIM VM, start the gNB and UE simulations. Ensure they connect to the core network.

   - Start gNB: `./nr-gnb -c ../config/open5gs-gnb.yaml`
   - Start UE: `./nr-ue -c ../config/open5gs-ue.yaml`
3.  **Check Connection**: you can use the following commands to check if the UE is sucessfully able to connect to the internet :
```bash
ping google.com -I uesimtun0
curl --interface uesimtun0 -X GET "https://httpbin.org/get"
```
If it runs, we have been successful!

-------
***Author**: Divyanka Chaudhari (2019CS50429)*
Please let me know if there can be any modification/addition or just create a pull request.