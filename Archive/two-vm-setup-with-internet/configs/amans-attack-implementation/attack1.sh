#/bin/sh

while :
do
	./build/nr-ue -c config/open5gs-ue2.yaml &
	./build/nr-ue -c config/open5gs-ue3.yaml &
	./build/nr-ue -c config/open5gs-ue4.yaml &
	./build/nr-ue -c config/open5gs-ue5.yaml &
	./build/nr-ue -c config/open5gs-ue6.yaml &
	sleep 0.5
	# remove -c from the commands below
	./build/nr-cli imsi-999700000000002 --exec 'deregister switch-off'
	./build/nr-cli imsi-999700000000003 --exec 'deregister switch-off'
	./build/nr-cli imsi-999700000000004 --exec 'deregister switch-off'
	./build/nr-cli imsi-999700000000005 --exec 'deregister switch-off'
	./build/nr-cli imsi-999700000000006 --exec 'deregister switch-off'
done
