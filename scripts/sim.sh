sudo sh /home/vagrant/open5gs/misc/netconf.sh
sudo sysctl -w net.ipv4.ip_forward=1
sudo sysctl -w net.ipv6.conf.all.forwarding=1
sudo iptables -t nat -A POSTROUTING -s 10.45.0.0/16 ! -o ogstun -j MASQUERADE
sudo ip6tables -t nat -A POSTROUTING -s 2001:db8:cafe::/48 ! -o ogstun -j MASQUERADE
# Use this for start capturing within the core network.
# nohup tshark -i any -w /home/vagrant/shared/internal_ogs_capture.pcap -Q &