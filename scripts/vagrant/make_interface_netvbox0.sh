sudo modprobe dummy
sudo ip link add netvbox0 type dummy
sudo ifconfig netvbox0 hw ether C8:D7:4A:4E:47:50
sudo ip addr add 192.168.1.100/24 brd + dev netvbox0
sudo ip link set dev netvbox0 up

# 
# sudo ip addr del 192.168.1.100/24 brd + dev eth0
# sudo ip link delete eth0 type dummy
# sudo rmmod dummy
#
