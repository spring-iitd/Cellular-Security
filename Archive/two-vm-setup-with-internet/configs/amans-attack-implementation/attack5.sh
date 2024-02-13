#/bin/sh

while :
do
	./build/nr-ue -c config/open5gs-ue22.yaml &
	./build/nr-ue -c config/open5gs-ue23.yaml &
	./build/nr-ue -c config/open5gs-ue24.yaml &
	./build/nr-ue -c config/open5gs-ue25.yaml &
	./build/nr-ue -c config/open5gs-ue26.yaml &
	sleep 0.5
	./build/nr-cli imsi-999700000000022 --exec 'deregister switch-off'
	./build/nr-cli imsi-999700000000023 --exec 'deregister switch-off'
	./build/nr-cli imsi-999700000000024 --exec 'deregister switch-off'
	./build/nr-cli imsi-999700000000025 --exec 'deregister switch-off'
	./build/nr-cli imsi-999700000000026 --exec 'deregister switch-off'
done		
