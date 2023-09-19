#/bin/sh

while :
do
	./build/nr-ue -c config/open5gs-ue7.yaml &
	./build/nr-ue -c config/open5gs-ue8.yaml &
	./build/nr-ue -c config/open5gs-ue9.yaml &
	./build/nr-ue -c config/open5gs-ue10.yaml &
	./build/nr-ue -c config/open5gs-ue11.yaml &
 	sleep 0.5
	./build/nr-cli imsi-999700000000011 --exec 'deregister switch-off'
	./build/nr-cli imsi-999700000000010 --exec 'deregister switch-off'
	./build/nr-cli imsi-999700000000009 --exec 'deregister switch-off'
	./build/nr-cli imsi-999700000000008 --exec 'deregister switch-off'
	./build/nr-cli imsi-999700000000007 --exec 'deregister switch-off'
done		
