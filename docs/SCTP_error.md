# SCTP error in Oracle VM
In case of an SCTP error, do the following: 
1. set the NatNetwork address in the Oracle VM box(/tools/network) to 192.168.56.0/24. 
2. Set the two VMs select the network attached to  'NAT network' and promiscuous mode to 'allow all '
