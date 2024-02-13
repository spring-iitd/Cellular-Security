# This script will run everytime that the system bootsup 

echo "--- Adding a route for the UE to have WAN connectivity over SGi/N6 -------"
sudo sh /home/vagrant/open5gs/misc/netconf.sh
sudo sysctl -w net.ipv4.ip_forward=1
sudo sysctl -w net.ipv6.conf.all.forwarding=1
sudo iptables -t nat -A POSTROUTING -s 10.45.0.0/16 ! -o ogstun -j MASQUERADE
sudo ip6tables -t nat -A POSTROUTING -s 2001:db8:cafe::/48 ! -o ogstun -j MASQUERADE