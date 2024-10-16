#!/bin/bash

open5gs-nrfd  -c  /home/vagrant/shared/core-open5gs/nrf.yaml   &
open5gs-scpd  -c  /home/vagrant/shared/core-open5gs/scp.yaml   &
open5gs-udmd  -c  /home/vagrant/shared/core-open5gs/udm.yaml   &
open5gs-udrd  -c  /home/vagrant/shared/core-open5gs/udr.yaml   &
open5gs-nssfd -c  /home/vagrant/shared/core-open5gs/nssf.yaml  &
open5gs-pcfd  -c  /home/vagrant/shared/core-open5gs/pcf.yaml   &
open5gs-bsfd  -c  /home/vagrant/shared/core-open5gs/bsf.yaml   &
open5gs-ausfd -c  /home/vagrant/shared/core-open5gs/ausf.yaml  &
open5gs-amfd  -c  /home/vagrant/shared/core-open5gs/amf.yaml   &
open5gs-upfd  -c  /home/vagrant/shared/core-open5gs/upf.yaml   &
open5gs-smfd  -c  /home/vagrant/shared/core-open5gs/smf.yaml   &