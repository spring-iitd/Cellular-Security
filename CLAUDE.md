# CLAUDE.md — Cellular-Security Repository Guide

This file provides context for AI assistants (Claude Code and others) working in this repository.

---

## Project Overview

**Cellular-Security** (also referred to as *5G-and-Beyond*) is a 5G core network research and security testing platform developed at the SPRING Lab, IIT Delhi. Its purpose is to minimize setup time for 5G network experiments, including security research, protocol testing, network slicing, QoS analysis, and packet capture/analysis.

The project uses **Vagrant + VirtualBox** to spin up pre-built VMs running **open5gs** (5G core) and **UERANSIM** (gNodeB + UE simulator), enabling a full 5G SA (Standalone) network on a single host.

---

## Repository Structure

```
Cellular-Security/
├── Vagrantfile                   # Multi-VM environment definition
├── README.md                     # Quick-start guide
├── .gitignore                    # Ignores *.log, *.pcap, proxy.sh, .vagran*, .vscode*
│
├── configurations/               # Tested, reusable deployment configs
│   ├── basic-configuration/      # Default open5gs + UERANSIM setup
│   │   ├── open5gs/              # NF config files (amf, smf, upf, nrf, etc.)
│   │   └── ueransim/             # gNB and UE config files
│   ├── slicing-all-nfs-shared/   # Network slicing (2 slices: SST1 + SST2)
│   │   └── shared/
│   │       ├── open5gs/
│   │       └── ueransim/
│   ├── metrics_using_prometheus_grafana/
│   │   ├── docker-compose.yaml   # Prometheus + Grafana stack
│   │   └── prometheus.yml        # Prometheus scrape config (update host IP)
│   └── upf-latency-measurement/  # UPF performance measurement configs
│
├── shared/                       # Synced between host and VMs at /home/vagrant/shared
│   ├── core-open5gs/             # Active open5gs NF config files (amf, smf, upf, etc.)
│   ├── gnb-ueransim/             # gNodeB configs: gnb0.yaml – gnb9.yaml
│   ├── ue-ueransim/              # UE configs: ue0.yaml – ue9.yaml
│   ├── scripts/
│   │   └── sim.sh                # Run after VM boot: sets up routing/iptables
│   └── log/                      # Log output directory
│
├── scripts/                      # Host-side utility scripts
│   ├── core-open5gs/
│   │   ├── check_status.sh       # Check which open5gs NFs are running
│   │   ├── add_user.sh           # Add UEs to open5gs MongoDB database
│   │   ├── open5gs_kill.sh       # Kill all open5gs processes
│   │   └── create_a_new_ogstun.sh # Create ogstun TUN interface
│   ├── vagrant/
│   │   ├── start_vms_parallel.sh # Start all VMs in parallel tmux windows
│   │   ├── stop_vms_parallel.sh  # Stop all VMs in parallel
│   │   ├── sim.sh                # Simulation helper
│   │   └── make_interface_netvbox0.sh # Set up vboxnet0 interface on host
│   └── ansible/
│       ├── playbook.ansible.yml  # Start all open5gs NFs via Ansible
│       └── generate_invenstory.sh # Generate Ansible inventory from Vagrant
│
├── docs/                         # Reference documentation
│   ├── intro_to_open5gs_and_ueransim.md
│   ├── two_vm_setup_sliced_core.md
│   ├── implement_network_slicing.md
│   ├── qos_parameters_for_quality.md
│   ├── vagrant_cheatsheet.md
│   ├── intro_to_pyshark.md
│   ├── running_user_applications.md
│   ├── packet_capture_using_virtualbox.md
│   ├── oai_installation.md
│   ├── SCTP_error.md
│   └── ...
│
└── pcaps/                        # Packet capture storage (gitignored: *.pcap)
```

---

## Virtual Machines

The Vagrantfile defines three VM types:

| VM Name    | Box          | IP(s)                          | vCPU | RAM  | Role                        |
|------------|--------------|-------------------------------|------|------|-----------------------------|
| `core_nw`  | `core-nw-1-0`| 192.168.56.100, .101           | 1    | 1 GB | 5G Core (open5gs + MongoDB) |
| `ran_nw`   | `ran-ue-nw`  | 192.168.56.120–.129 (10 IPs)  | 8    | 8 GB | RAN attacker / UERANSIM gNB |
| `ue_nw`    | `ran-ue-nw`  | 192.168.56.130                 | 2    | 2 GB | Benign UE simulator         |

**Shared folder**: `./shared` on host → `/home/vagrant/shared` in all VMs.

**Automatic post-boot**: `core_nw` runs `shared/scripts/sim.sh` after `vagrant up` to configure IP forwarding and NAT rules.

**Packet capture**: VirtualBox NIC tracing is enabled by default on `core_nw` to `pcaps/nictrace1.pcap` and `pcaps/nictrace2.pcap`.

---

## Network Configuration

| Component        | Value                  |
|------------------|------------------------|
| PLMN MCC         | 999                    |
| PLMN MNC         | 70                     |
| UE tunnel subnet | 10.45.0.0/16           |
| IoT slice subnet | 10.46.0.0/16           |
| IPv6 UE subnet   | 2001:db8:cafe::/48     |
| Core private net | 192.168.56.0/24        |

**NF SBI ports** (non-default, used in slicing configuration):

| NF   | SBI Port | Metrics Port |
|------|----------|--------------|
| AMF  | 7800     | 9091         |
| AUSF | 7801     | —            |
| BSF  | 7802     | —            |
| NRF  | 7820     | —            |
| NSSF | 7803     | —            |
| PCF  | 7804     | 9092         |
| SCP  | 7810     | —            |
| SMF  | 7805     | 9093         |
| UDM  | 7807     | —            |
| UDR  | 7806     | —            |
| UPF  | —        | 9094         |

**Forwarded ports** (host → `core_nw`): 9091, 9092, 9093, 9094 (NF metrics), 9999 (open5gs web UI).

---

## Common Workflows

### 1. First-Time Environment Setup

```bash
# Add pre-built Vagrant box images (from local server)
vagrant box add /boxes/core.box --name core-nw-1-0 --provider virtualbox --force --clean
vagrant box add /boxes/ran-ue.box --name ran-ue-nw --provider virtualbox --force --clean
vagrant plugin install vagrant-proxyconf
```

> The boxes are stored locally on the IITD server. Do not attempt to download them from the internet.

### 2. Starting/Stopping VMs

```bash
vagrant up core_nw          # Start core network VM
vagrant up ran_nw            # Start RAN/attack VM
vagrant up ue_nw             # Start benign UE VM
vagrant ssh core_nw          # SSH into core VM
vagrant halt                 # Stop all VMs
vagrant destroy -f           # Destroy all VMs
```

To start multiple VMs in parallel using tmux:
```bash
bash scripts/vagrant/start_vms_parallel.sh
bash scripts/vagrant/stop_vms_parallel.sh
```

### 3. Starting the 5G Core Network (inside `core_nw`)

Run NFs using config files from `/home/vagrant/shared/core-open5gs/`:
```bash
open5gs-nrfd  -c /home/vagrant/shared/core-open5gs/nrf.yaml  &
open5gs-scpd  -c /home/vagrant/shared/core-open5gs/scp.yaml  &
open5gs-udmd  -c /home/vagrant/shared/core-open5gs/udm.yaml  &
open5gs-udrd  -c /home/vagrant/shared/core-open5gs/udr.yaml  &
open5gs-nssfd -c /home/vagrant/shared/core-open5gs/nssf.yaml &
open5gs-pcfd  -c /home/vagrant/shared/core-open5gs/pcf.yaml  &
open5gs-bsfd  -c /home/vagrant/shared/core-open5gs/bsf.yaml  &
open5gs-ausfd -c /home/vagrant/shared/core-open5gs/ausf.yaml &
open5gs-amfd  -c /home/vagrant/shared/core-open5gs/amf.yaml  &
open5gs-upfd  -c /home/vagrant/shared/core-open5gs/upf.yaml  &
open5gs-smfd  -c /home/vagrant/shared/core-open5gs/smf.yaml  &
```

Or use the Ansible playbook from the host (after generating inventory):
```bash
bash scripts/ansible/generate_invenstory.sh
ansible-playbook scripts/ansible/playbook.ansible.yml -i inventory
```

### 4. Starting gNodeB and UE (inside `ran_nw` or `ue_nw`)

```bash
nr-gnb -c /home/vagrant/shared/gnb-ueransim/gnb0.yaml &
sudo nr-ue -c /home/vagrant/shared/ue-ueransim/ue0.yaml &
```

### 5. Verifying Connectivity

```bash
# Check NF status (run inside core_nw or from host via shared)
bash scripts/core-open5gs/check_status.sh

# Test UE internet access (inside ran_nw)
ping google.com -I uesimtun0
curl --interface uesimtun0 -X GET "https://httpbin.org/get"

# Interact with gNB/UE via CLI (inside ran_nw)
nr-cli --help
```

### 6. Managing UE Subscriptions

```bash
# Add N UEs to open5gs MongoDB (run inside core_nw)
bash scripts/core-open5gs/add_user.sh <N>

# Kill all open5gs NFs
bash scripts/core-open5gs/open5gs_kill.sh
```

Default UE credentials used by `add_user.sh`:
- SUPI base: `999700000000001`
- Key: `465B5CE8B199B49FAA5F0A2EE238A6BC`
- OP: `E8ED289DEBA952E4283B54E88E6183CA`

### 7. Metrics (Prometheus + Grafana)

```bash
# Start from configurations/metrics_using_prometheus_grafana/
# First update prometheus.yml with actual core_nw IP
docker-compose up -d

# Access dashboards
# Grafana:    http://<host-ip>:3000  (admin/admin)
# Prometheus: http://<host-ip>:9090
```

### 8. Proxy Configuration (IITD network)

```bash
# In VMs, unset proxy if NFs fail to connect
unset http_proxy https_proxy HTTP_PROXY HTTPS_PROXY

# Verify no proxy is set
env | grep -i proxy
```

---

## Configuration Files Guide

### `shared/` vs `configurations/`

- `shared/` contains **active working configs** that are synced to VMs. Modify these for experiments.
- `configurations/` contains **reference snapshots** of tested setups. Copy from here when starting a new experiment variant.

### Key config areas to customize

| File | What to change |
|------|----------------|
| `shared/core-open5gs/amf.yaml` | PLMN ID, slices (S-NSSAI), NGAP bind address |
| `shared/core-open5gs/smf.yaml` | Session subnets, UPF address, DNN names |
| `shared/core-open5gs/upf.yaml` | Session subnets, DNN names, UPF interface |
| `shared/core-open5gs/nrf.yaml` | SBI bind address and port |
| `shared/gnb-ueransim/gnb0.yaml` | AMF address, PLMN ID, TAC, slices |
| `shared/ue-ueransim/ue0.yaml` | IMSI, key, OP, DNN, slice |
| `Vagrantfile` | VM IPs, RAM, CPU, proxy settings |

---

## Troubleshooting

| Symptom | Likely Cause | Fix |
|---------|-------------|-----|
| NFs not connecting to each other | HTTP proxy set in VM | `unset http_proxy https_proxy HTTP_PROXY HTTPS_PROXY` |
| SCTP errors on AMF startup | Port conflict or missing interface | See `docs/SCTP_error.md` |
| UE cannot register | IMSI/key mismatch in DB | Re-run `add_user.sh` with correct credentials |
| `vagrant up` hangs | VirtualBox network issue | Run `make_interface_netvbox0.sh` to recreate vboxnet0 |
| Pcap file grows too large | NIC trace always on | Disable `nictrace` lines in `Vagrantfile` |

---

## Technology Stack

| Component    | Technology       | Notes |
|-------------|------------------|-------|
| Virtualization | Vagrant + VirtualBox | VM lifecycle management |
| 5G Core      | open5gs          | NRF, SCP, AMF, SMF, UPF, UDM, UDR, AUSF, NSSF, PCF, BSF |
| 5G Core (alt) | free5gc         | Installed in `core_nw` box but not primary |
| RAN + UE     | UERANSIM         | nr-gnb, nr-ue, nr-cli |
| UE (alt)     | PacketRusher     | Installed in `ran-ue-nw` box |
| Database     | MongoDB          | Used by open5gs for subscriber data |
| Automation   | Ansible          | Playbook for starting NFs remotely |
| Monitoring   | Prometheus + Grafana | Via docker-compose |
| Packet Capture | tshark / Wireshark | Both VirtualBox NIC trace and in-VM tshark |

---

## Git Conventions

- **Branch naming**: Feature/experiment branches follow `<name>-dev-env` or descriptive names
- **Commit messages**: Short imperative phrases; multi-line changes listed with `-`
- **Gitignore**: Never commit `*.pcap`, `*.log`, `proxy.sh`, `.vagran*`, or `.vscode*`
- **No CI/CD**: This repo has no automated test pipeline; all validation is manual

---

## Important Notes for AI Assistants

1. **No build system**: This is an infrastructure/configuration repo. There is no `make`, `npm`, `pip install`, or compilation step.
2. **No automated tests**: There is no test suite. Validation is done by running VMs and checking network connectivity.
3. **Config files are YAML**: All open5gs and UERANSIM configs are YAML. Be careful with indentation.
4. **Path dependencies**: Configs in `configurations/` reference absolute paths inside VMs (`/home/vagrant/shared/...`). Do not change these paths without updating VM provisioning.
5. **Sensitive data**: `proxy.sh` contains credentials and is gitignored. Never create or commit this file.
6. **Security research context**: This repo is used for 5G network security research. Scripts like `open5gs_kill.sh` and `add_user.sh` are legitimate research tools, not malware.
7. **Multiple gNB/UE support**: The setup supports up to 10 gNodeBs (gnb0–gnb9) and 10 UEs (ue0–ue9), each with their own YAML config and IP.
8. **Shared directory is the source of truth**: Changes to NF configs should go in `shared/core-open5gs/` and `shared/gnb-ueransim/` (not directly into `configurations/`).
