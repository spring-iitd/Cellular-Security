TODO: Add images, add references to other related guides when completed

## Network Slicing with Basic Configuration

Network slicing is a fundamental technology in 5G networks that enables multiple logical networks to be created on top of a common physical infrastructure. This is crucial for meeting the diverse requirements of various applications, such as enhanced mobile broadband (eMBB), massive machine-type communications (mMTC), and ultra-reliable and low-latency communications (URLLC).

If you're not familiar with Network Slicing, please google and learn a bit more about what it is and why it is used. In this guide, we will try to implement Network Slicing on our 5G core network using the open5GS and UERANSIM (two VM) setup. Ensure that you have the two VM setup in place. 

### Reference
We're referring to [this video](https://youtu.be/8QDQNAAgtiQ?si=O0vUf4TeorvW1c2l), you can have a look at it if you want. However, I have tailored this article to work with the 2 VM setup that our research group at IITD is using. 

### Prerequisites

This setup assumes you have one VM for the core network (CN) using Open5GS and another VM for the User Equipment (UE)/Radio Access Network (RAN) simulation using UERANSIM.

First, ensure both Open5GS and UERANSIM are installed on their respective VMs.  

### Step 1: Configure Open5GS for Network Slicing

1. Make sure that the 5G core network is running, this is done by running the commands. 

```
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
2. **Open the WebUI to add subscribers:** From our initial configuration, we know that our `mcc: 999` and `mnc: 70` so our IMSI number will always follow the format <mcc><mnc><identifier>. So, let's add subscribers with the following information, when not mentioned, use default settings:
	1. `IMSI: 999705210000011`, `DNN/APN: internet`
	2. `IMSI: 999705210000021`, `DNN/APN: iot`
	3. `IMSI: 999705210000031`, `DNN/APN: edge`
	4. `IMSI: 999705210000041`, `DNN/APN: yourownslice`

### Step 3: Configure UERANSIM for Network Slicing

1. **UE Configuration**: Edit the UERANSIM UE configuration file to include the desired slice. This file is typically named `ue.yaml`. We can create a copy of `ue.yaml` and then edit those copies. Let's call the first copy `ue1_internet.yaml`. Create a copy using `cp open5gs-ue.yaml ue1_internet.yaml`. Now open `ue1_internet.yaml`. You need to specify the `sst` for the slice in the `sessions` section:

   ```yaml
   supi: 999705210000011
	
	# ... rest of the information remains same
	# Make sure it matches with the subscriber information on WebUI
   sessions:
   - type: 'IPv4'
      apn: 'internet'
      slice:
	      sst: 1
   ```
   
Similarly, modify `ue2_iot.yaml`, `ue3_edge.yaml` and `ue4_yourownslice.yaml` with the relevant information.

### Step 4: Run the Simulation

1. **Start Open5GS Services**: On the Open5GS VM, start all Open5GS services if not already started.

2. **Run UERANSIM**: On the UERANSIM VM, start the gNB and UE simulations. Ensure they connect to the core network and the specified slices are being used.

   - Start gNB: `./nr-gnb -c ../config/open5gs-gnb.yaml`
   - Start UE: `./nr-ue -c ../config/ue1_internet.yaml`, `./nr-ue -c ../config/ue2_iot.yaml`, `./nr-ue -c ../config/ue3_edge.yaml` and  `./nr-ue -c ../config/ue4_yourownslice.yaml`
  
 3. **Look at the Logs**: Check the logs of both Open5GS and UERANSIM, find log entries with `DNN[internet]`, `DNN[iot]`, `DNN[yourownslice]`, etc. 
 4. **Check connectivity**: Run `ip` and you'll see `uesimtun0` to `uesimtun3` because we have created a total of 4 slices. We can check if these work by `ping -I uesimtun0 google.com`. Instead of `uesimton0`, put others and check. If this works, we've been successful!

### Troubleshooting and Verification

- **Log Inspection**: Check the logs of both Open5GS and UERANSIM for any errors or warnings.
- **Open5GS Web UI**: Use the Open5GS Web UI to verify that the slices are correctly configured and that UEs are registered on the desired slices.
- **Packet Capture**: Tools like Wireshark can be used to capture packets and verify that traffic is flowing through the correct slices.


-------

***Author:** Divyanka Chaudhari (2019CS50429)*
