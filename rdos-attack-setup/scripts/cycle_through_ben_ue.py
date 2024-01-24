# until killed run the following:
#   1. start a UE
#   2. wait for 1 second
#   3. stop the UE
import argparse
import time
import subprocess
from copy import deepcopy
import yaml
import os
import socket

def create_config(number_of_ues, pdu_session):
    """ This function creates the individual config files for each UE.
    """
    base_supi = 999700000000001
    key = int("465B5CE8B199B49FAA5F0A2EE238A6BC",16)

    ## changes the config on the one UE based on the pdu session value.

    path = "/home/vagrant/UERANSIM/config/"

    with open(path + 'open5gs-ue.yaml', 'r') as file:
        original_ue = yaml.safe_load(file)

    new_ue = deepcopy(original_ue)

    if pdu_session != 1:
        del new_ue['sessions']

    for i in range(0, number_of_ues):
        new_ue['supi'] = "imsi-"+ str(base_supi + i)
        new_ue['key'] = str(hex(key + i)).split('0x')[-1].upper()
        with open(path + 'open5gs-ue-'+ str(i+1) +'.yaml', 'w') as file:
            yaml.dump(new_ue, file)

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='''This scripts starts a number of UEs and then deregisters them.''')
    parser.add_argument("-p","--pdu-session" ,  help="pdu session",type=int, default=1)
    parser.add_argument("-n","--number-of-ues" ,  help="number of ues",type=int, default=1)
    parser.add_argument("-d","--delay" ,  help="delay between each ue",type=int, default=2)
    args = parser.parse_args()

    pdu_session = args.pdu_session
    number_of_ues = args.number_of_ues
    delay = args.delay

    create_config(number_of_ues, pdu_session)

    s = socket.socket()

    # Define the port on which you want to connect
    addr = "192.168.56.130"
    port = 12345

    # Bind the socket to the port
    s.bind((addr, port))

    # Put the socket into listening mode
    s.listen(1)

    # Establish connection with client.
    c, addr = s.accept()
    print('Got connection from', addr)

    for i in range(number_of_ues):
        print("starting ue",i)
        c.send(b'1')
        time.sleep(0.05)
        subprocess.run(["nr-ue -c /home/vagrant/UERANSIM/config/open5gs-ue-"+str(i+1)+".yaml > "+str(i+1)+".log &"],shell=True)
        time.sleep(delay)

    c.close()
