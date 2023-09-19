# An Introduction to Open5GS

Open5GS contains software components and network functions that implement the 4G/5G NSA and 5G SA core functions. The 5G SA core is a Service Based Architecture (SBI). 
<img src="https://miro.medium.com/max/1400/1*eMg9GbQJHxMiiYJnf7x0_g.png"/>

The 5G StandAlone (SA) Core contains the following functions:

- AMF - Access and Mobility Management Function
  - The AMF handles connection and mobility management. gNBs (5G base stations) connect to the AMF.
- SMF - Session Management Function
  - Session management is all handled by the SMF.

- NRF - NF Repository Function
  - Control plane functions are configured to register with the NRF, and the NRF then helps them discover the other core functions. 
  
- AUSF - Authentication Server Function
- UDM - Unified Data Management
- UDR - Unified Data Repository
  - The UDM, AUSF and UDR carry out operations such as generating SIM authentication vectors and holding the subscriber profile. 

- PCF - Policy and Charging Function
  -  PCF is used for charging and enforcing subscriber policies.
- NSSF - Network Slice Selection Function
  -  The NSSF provides a way to select the network slice. 

- UPF - User Plane Function
  - The UPF carries user data packets between the gNB and the external WAN. It connects back to the SMF too.
- BSF - Binding Support Function

Except for the SMF and UPF, all config files for the 5G SA core functions only contain the function's IP bind addresses/ local Interface names and the IP address/ DNS name of the NRF.

# An Introduction to UERANSIM
This provides the 5G UE and gNodeB implementations to the system. There are three main interfaces here: 
- Control Interface (between RAN and AMF)
- User Interface (between RAN and UPF) 
- Radio Interface (between UE and RAN)


# Installation 
## Open5GS Installation
This part of the guide is based on installing on Intel-based machines. This installation process is fairly simple here. This process was verified on an Azure x86 VM running Ubuntu Server 20.04 

## Installation on x86 and amd64

```shell
sudo apt update
sudo apt install software-properties-common
sudo add-apt-repository ppa:open5gs/latest
sudo apt update
sudo apt install open5gs
```

## Installation on arm64
The precompiled binaries only exist for the other x86 architecture platforms. We have to build the tool here. Links for the extended guides are given in the links. A brief is explanation is also given below. 

- [Building Open5GS from Sources on Linux](https://open5gs.org/open5gs/docs/guide/02-building-open5gs-from-sources/)
  - These instructions were tested and Parallels VM on Ubuntu systems.
- [Building Open5GS from Sources on MacOS](https://open5gs.org/open5gs/docs/platform/05-macosx-apple-silicon/)
  - These instructions were tested macOS Monterey 12.5 on a Macbook Air (Apple M1 Chipset).

### Installing on MacOS 
  1.  Prerequisites
      - Install Xcode Command-Line Tools
        - Homebrew requires the Xcode command-line tools from Apple’s Xcode.
          ```shell
          xcode-select --install
          ```
      - Installing Homebrew
        - Install brew using the official Homebrew installation instructions.
          ```shell
          /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
          ```
        - Configure Homebrew PATH
          ```shell
          $ export PATH="/opt/homebrew/opt/bison/bin:/opt/homebrew/bin:$PATH"
          $ export LIBRARY_PATH=/opt/homebrew/lib
          $ export C_INCLUDE_PATH=/opt/homebrew/include
          $ export CPLUS_INCLUDE_PATH=/opt/homebrew/include
          ```
      - MongoDB
        - Install MongoDB with Package Manager.
          ```shell
          brew tap mongodb/brew
          brew install mongodb-community
          ```
        - Run MongoDB persistent server.
          ```shell
          brew services start mongodb-community
          ```
        - Other Dependencies 
          ```shell
          brew install mongo-c-driver gnutls libgcrypt libidn libyaml libmicrohttpd nghttp2 pkg-config bison libusrsctp libtins talloc meson node
          ```

  2. Setting up the Network 
        ```shell
        git clone https://github.com/open5gs/open5gs
        cd open5gs
        sudo ./misc/netconf.sh
        ```
        > Note that Open5GS uses built-in “utun” device driver. So, You don’t have to install external TUN/TAP driver.
  3. Building Open5GS
      - Compile with meson
        ```shell
        meson build --prefix=`pwd`/install
        ninja -C build
        ```
      - Check whether the compilation is correct.
        ```shell
        cd build
        sudo meson test -v
        cd ../
        ```

      - You need to perform the installation process.
        ```shell
        $ cd build
        $ ninja install
        $ cd ../
        ```
    
  4.  Building WebUI of Open5GS
      - Install the dependencies to run WebUI
        ```shell
        cd webui
        npm ci --no-optional
        ```
      
      - The WebUI runs as an npm script.
        ```shell
        npm run dev
        ```
### Installing on Ubuntu 
1. Installing MongoDB 

    Import the public key used by the package management system.

    ```shell
    sudo apt update
    sudo apt install gnupg
    curl -fsSL https://pgp.mongodb.com/server-6.0.asc | sudo gpg -o /usr/share/keyrings/mongodb-server-6.0.gpg --dearmor
    ```

    Create the list file /etc/apt/sources.list.d/mongodb-org-6.0.list for your version of Ubuntu.

2. On ubuntu 22.04 (Focal)

    ```shell
    $ echo "deb [ arch=amd64,arm64 signed-by=/usr/share/keyrings/mongodb-server-6.0.gpg] https://repo.mongodb.org/apt/ubuntu focal/mongodb-org/6.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-6.0.list
    ```

    Install the MongoDB packages.

    ```shell
    sudo apt update
    sudo apt install -y mongodb-org
    sudo systemctl start mongod (if '/usr/bin/mongod' is not running)
    sudo systemctl enable mongod (ensure to automatically start it on system boot)
    ```

3. Git Clone

    ```shell
    git clone https://github.com/open5gs/open5gs
    ```

4. Network Setup 

    ```shell
    sudo ./open5gs/misc/netconf.sh
    ```

5. Install the dependencies for building the source code.

    ```shell
    sudo apt install python3-pip python3-setuptools python3-wheel ninja-build build-essential flex bison git libsctp-dev libgnutls28-dev libgcrypt-dev libssl-dev libidn11-dev libmongoc-dev libbson-dev libyaml-dev libnghttp2-dev libmicrohttpd-dev libcurl4-gnutls-dev libnghttp2-dev libtins-dev libtalloc-dev meson
    ```

6. Compile 
    ```shell
    cd open5gs
    meson build --prefix=`pwd`/install
    ninja -C build 
    ```

7. Run all test programs as below.
    ```shell
    cd build
    meson test -v
    cd ../
    ```

8. Installation process
    ```shell
    cd build
    ninja install
    cd ../
    ```

## Building the WebUI 
Open5GS gives us a webUI for registering and managing the UEs. This UI works on Nodejs. In this section, we will build and execute the web interface. 

1. Install Node
   ```shell 
    sudo apt update
    sudo apt install curl
    curl -fsSL https://deb.nodesource.com/setup_14.x | sudo -E bash -
    sudo apt install nodejs
    curl -fsSL https://open5gs.org/open5gs/assets/webui/install | sudo -E bash -
    cd webui
    npm ci --no-optional
   ```
2. Running the WebUI 
    ```shell
    npm run dev
    ```



## Open5GS Configuration and Services

The configuration for the 5G functions and interfaces can be found in `~/open5gs/install/etc/open5gs`. Here is a list of configurations available to us. 

| Configuration|  Files | |
| --- | --- | ---|
| pcrf.yaml | amf.yaml | ausf.yaml 
| bsf.yaml| hss.yaml| mme.yaml| 
| nrf.yaml| nssf.yaml|  pcf.yaml|
| scp.yaml| sgwc.yaml| sgwu.yaml| 
| smf.yaml| udm.yaml| udr.yaml| 
| upf.yaml| 

We need to restart that particular service after changing any of these files. This can be done using the command: 
```shell
sudo systemctl restart open5gs-amfd
```

> Note: These scripts, by default, configure the service with `/etc/open5gs/upf.yaml`. 
> ```shell
> sudo ./open5gs/install/bin/open5gs-upfd -c ./install/etc/open5gs/upf.yaml & 
> ```
> You can restart the service with a specific configuration with the above statement. 


### Registering a UI using WebUI 
Part of configuring the simulator is registering the UE with the core network. We need to go to the URL `http://localhost:3000` and log in with the default credentials: `admin/1423`. 

<img src="https://miro.medium.com/max/700/1*TaUIUONqzsGzXUKcq3OyKg.png"/>

```
> Defaults:
IMSI: 901700000000001
Subscriber Key: 465B5CE8B199B49FAA5F0A2EE238A6BC
USIM Type: OPC
Operator Key: E8ED289DEBA952E4283B54E88E6183CA
```
## UERANSIM Installation 
The simulator is only functional on Ubuntu 16.04 or later. This cannot be installed on host Windows or Mac machines. This was tested on Ubuntu VM running over ARM MacBook Air.

1. Install the dependencies
   ```shell
   sudo apt update
   sudo apt upgrade
   sudo apt install make gcc g++ libsctp-dev lksctp-tools iproute2
   sudo apt install cmake --classic 
   ```
2. Clone
   ```shell
   cd ~
   git clone https://github.com/aligungr/UERANSIM
   ```
3. Make
   ```shell
   cd ~/UERANSIM
   make
   ```
The compiled binaries are in the /ueransim/build/ folder. 
- nr-gnb | Main executable for 5G gNB (RAN)
- nr-ue | Main executable for 5G UE
- nr-cli | CLI tool for 5G gNB and UE

## UERANSIM Configuration and Services
  By changing the respective configuration files within  `~/UERANSIM/config/`, the UE and gNodeB can be customised. Within our limited experiment, we need just to add the registered UE configuration. 

  ### Register UE and gNodeB
  In the process of configuring a subscriber to our simulated network, we had put in an IMSI number, Subscriber Key, USIM Type & Operator Key in `UERANSIM/config/open5gs-ue.yaml` 

We can also modify the configuration of `UERANSIM/config/open5gs-gnb.yaml` if needed. 


--- 
References:
1. https://medium.com/rahasak/5g-core-network-setup-with-open5gs-and-ueransim-cd0e77025fd7
2. https://open5gs.org/open5gs/docs/guide/02-getting-started/
 