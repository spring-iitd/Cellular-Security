#/bin/sh

while :
do
	./build/nr-ue -c config/open5gs-ue12.yaml &
	./build/nr-ue -c config/open5gs-ue13.yaml &
	./build/nr-ue -c config/open5gs-ue14.yaml &
	./build/nr-ue -c config/open5gs-ue15.yaml &
	./build/nr-ue -c config/open5gs-ue16.yaml &
	sleep 0.5
	./build/nr-cli imsi-999700000000012 --exec 'deregister switch-off'
	./build/nr-cli imsi-999700000000013 --exec 'deregister switch-off'
	./build/nr-cli imsi-999700000000014 --exec 'deregister switch-off'
	./build/nr-cli imsi-999700000000015 --exec 'deregister switch-off'
	./build/nr-cli imsi-999700000000016 --exec 'deregister switch-off'
done		
