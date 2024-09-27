#!/bin/bash

nfs=("open5gs-amfd" "open5gs-ausfd" "open5gs-bsfd" "open5gs-nrfd" "open5gs-nssfd" "open5gs-pcfd" "open5gs-scpd" "open5gs-smfd" "open5gs-upfd" "open5gs-udmd" "open5gs-udrd")

running_count=0

GREEN="\e[32m"
RED="\e[31m"
NC="\e[0m"

echo "Status of Open5GS daemons..."
echo ""

for nf in "${nfs[@]}"; do
    if ps -e | grep -q "$nf"; then
        echo -e "${nf#open5gs-}: ${GREEN}running${NC}"
        ((running_count++))
    else
        echo -e "${nf#open5gs-}: ${RED}not running${NC}"
    fi
done

echo ""
echo -e "$running_count unique NFs are running!"
