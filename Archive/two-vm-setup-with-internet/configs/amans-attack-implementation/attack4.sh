#/bin/sh

while :
do
	./build/nr-ue -c config/open5gs-ue17.yaml &
	./build/nr-ue -c config/open5gs-ue18.yaml &
	./build/nr-ue -c config/open5gs-ue19.yaml &
	./build/nr-ue -c config/open5gs-ue20.yaml &
	./build/nr-ue -c config/open5gs-ue21.yaml &
	sleep 0.5
	./build/nr-cli imsi-999700000000017 --exec 'deregister switch-off'
	./build/nr-cli imsi-999700000000018 --exec 'deregister switch-off'
	./build/nr-cli imsi-999700000000019 --exec 'deregister switch-off'
	./build/nr-cli imsi-999700000000020 --exec 'deregister switch-off'
	./build/nr-cli imsi-999700000000021 --exec 'deregister switch-off'
done		
