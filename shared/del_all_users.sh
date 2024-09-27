#!/bin/bash

start_imsi=999700000000001
end_imsi=999700000000304

for (( imsi=${start_imsi}; imsi<=${end_imsi}; imsi++ )); do
    sudo open5gs-dbctl remove ${imsi}
    echo "UE with IMSI: ${imsi} deleted"
done
