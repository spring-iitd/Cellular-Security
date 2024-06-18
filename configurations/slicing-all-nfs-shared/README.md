

# 5GC NFs with Two Slices

## Configuration changes
This is mapping for the 5GC NFs. There are a few things to note with the slicing configuration:

`amf.yaml`:
```yaml
plmn_support:
- plmn_id:
    mcc: 999
    mnc: 70
    s_nssai:
    - sst: 1
- plmn_id:
    mcc: 999
    mnc: 70
    s_nssai:
    - sst: 2
```      

`nssf.yaml`:
```yaml
client:
    nrf:
    - uri: http://192.168.56.100:7820
    scp:
    - uri: http://192.168.56.100:7810
    nsi:
    - uri: http://192.168.56.100:7820
        s_nssai:
        sst: 1
    nsi:
    - uri: http://192.168.56.100:7820
        s_nssai:
        sst: 2
```

`smf.yaml`:
```yaml
session:
- subnet: 10.45.0.0/16
    gateway: 10.45.0.1
    dnn: internet
- subnet: 10.45.0.1/16
    gateway: 10.45.0.1 
    dnn: iotnet
```

`upf.yaml`:
```yaml
session:
- subnet: 10.45.0.0/16
    gateway: 10.45.0.1
    dnn: internet
- subnet: 10.46.0.1/16
    gateway: 10.46.0.1
    dnn: iotnet
```
## New Interface in Core VM
```bash
sudo ip tuntap add name ogstun mode tun
sudo ip addr add 10.45.0.1/16 dev ogstun
sudo ip addr add 2001:db8:cafe::1/48 dev ogstun
sudo ip link set ogstun up

sudo ip tuntap add name ogstun3 mode tun
sudo ip addr add 10.46.0.1/16 dev ogstun3
sudo ip link set ogstun3 up
```

## Ports used by the NFs
Also Note that the following ports are used for the NFs:
| Service | Protocol | New Port Number |
|---------|----------|-----------------|
| AMF     | SBI      | 7800            |
|         | NGAP     | ---             |
|         | Metrics  | 9091            |
| AUSF    | SBI      | 7801            |
| BSF     | SBI      | 7802            |
| NRF     | SBI      | 7820            |
| NSSF    | SBI      | 7803            |
| PCF     | SBI      | 7804            |
|         | Metrics  | 9092            |
| SCP     | SBI      | 7810            |
| SMF     | SBI      | 7805            |
|         | PFCP-S   | 100:----        |
|         | PFCP-C   | 101:----        |
|         | GTPC     | 100:----        |
|         | GTPU     | 100:----        |
| SMF     | Metrics  | 9093            |
| UDM     | SBI      | 7807            |
| UDR     | SBI      | 7806            |
| UPF     | PFCP-S   | 101:----        |
|         | GTPU     | 101:----        |
|         | Metrics  | 101:9094        |