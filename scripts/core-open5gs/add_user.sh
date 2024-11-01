#!/bin/bash

  if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <number_of_ues_to_add>"
    exit 1
  fi

  no_of_ues_to_add=$1
  base_supi=999700000000001
  key="465B5CE8B199B49FAA5F0A2EE238A6BC"
  op="E8ED289DEBA952E4283B54E88E6183CA"

  for ((i=0; i<=no_of_ues_to_add; i++)); do
    supi=$((base_supi + i))
    command="sudo open5gs-dbctl add $supi $key $op"
    eval $command
    echo "UE with IMSI: $supi added"
  done