# Sample Command
# python3 run_experiment.py --pdu_session 1 --ben_ues 100 --ben_delay 2 --start_imsi 999700000000500 --mal_ues 750 --attack_type 1 --repeat 0 --timeout 200 --processes 100 --delay_between 0.5  --count 1

import argparse
import os
import subprocess


def run(pdu_session, ben_ues, ben_delay, start_imsi, mal_ues, attack_type, repeat, timeout, processes, mal_delay, count):
    subprocess.run(["vagrant up"], shell=True, check=True)
    print("Vagrant Up and Running")

    str1 = "-timeout-"+str(timeout)+"-ben-"+str(ben_ues)+"-delay-"+str(ben_delay)+"-mal-"+str(mal_ues)+"-delay-"+str(mal_delay)+"-count-"+str(count) + "-repeat-"+str(repeat)

    subprocess.run(["tshark -i bridge102 -f 'port 38412' -w captured_traffic"+str1+ ".pcap &"], shell=True, check=True)
    print("Tshark Running")

    subprocess.run(["vagrant ssh open5gs -c 'sudo nohup /home/vagrant/start_all_open5gs.sh > open5gs.log & sleep 1'"], shell=True, check=True)
    print("Open5GS Running")

    subprocess.run(["vagrant ssh amf-only -c 'sudo nohup /home/vagrant/open5gs/install/bin/open5gs-amfd > amfd.log & sleep 1'"], shell=True, check=True)
    subprocess.run(["vagrant ssh amf-only -c 'sudo nohup /home/vagrant/process_mon.sh > lo.log & sleep 1'"], shell=True, check=True)
    print("AMF Running")

    subprocess.run(["vagrant ssh gnb-only -c 'sudo nohup /home/vagrant/UERANSIM/build/nr-gnb -c ~/UERANSIM/config/open5gs-gnb-1.yaml > gnb1.log & sleep 1'"], shell=True, check=True)
    subprocess.run(["vagrant ssh gnb-only -c 'sudo nohup /home/vagrant/UERANSIM/build/nr-gnb -c ~/UERANSIM/config/open5gs-gnb-2.yaml > gnb2.log & sleep 1'"], shell=True, check=True)
    print("gNodeB Running")

    cmd = "vagrant ssh benign-ue-only -c 'sudo nohup python3 /home/vagrant/cycle_through_ben_ue.py --pdu-session " + str(pdu_session) + " --number-of-ues " + str(ben_ues) + " --delay " + str(ben_delay) + " > ben_call.log & sleep 1'"
    subprocess.run([cmd], shell=True, check=True)
    print("Benign UEs Running")

    print("Malicious UEs Running")
    cmd = "vagrant ssh mal-ue-only -c 'sudo nohup python3 /home/vagrant/launch.py --start_imsi "+ str(start_imsi) +" --number_of_ues " + str(mal_ues) + " --attack_type " + str(attack_type) + " --repeat " + str(repeat) + " --timeout " + str(timeout) + " --processes " + str(processes) + " --delay_between " + str(mal_delay) + " > mal_call.log & wait'"    
    subprocess.run([cmd], shell=True, check=True)
    print("End of Experiment Saving Logs")

    # subprocess.run(["vagrant ssh open5gs -c 'sudo pkill open5gs'"], shell=True, check=True)
    # subprocess.run(["vagrant ssh amf-only -c 'sudo pkill open5gs'"], shell=True, check=True)
    # subprocess.run(["vagrant ssh gnb-only -c 'sudo pkill nr-gnb'"], shell=True, check=True)
    # subprocess.run(["vagrant ssh benign-ue-only -c 'sudo pkill nr-ue'"], shell=True, check=True)
    # subprocess.run(["vagrant ssh benign-ue-only -c 'sudo pkill python3'"], shell=True, check=True)
    # subprocess.run(["vagrant ssh mal-ue-only -c 'sudo pkill nr-ue'"], shell=True, check=True)
    # subprocess.run(["vagrant ssh mal-ue-only -c 'sudo pkill python3'"], shell=True, check=True)
    # print("Killed all processes")

    subprocess.run(["pkill tshark"], shell=True, check=True)
    print("Killed tshark")
    print("Halting vagrant")
    subprocess.run(["vagrant halt"], shell=True, check=True)


if __name__ == "__main__": 
    
    # parser = argparse.ArgumentParser(description='Run experiment')

    # parser.add_argument("--pdu_session" ,   help="BEN: pdu session",type=int, default=1, required=True)
    # parser.add_argument("--ben_ues"     ,   help="BEN: number of ues",type=int, default=1, required=True)
    # parser.add_argument("--ben_delay"   ,   help="BEN:delay between each ue",type=int, default=2, required=True)

 
    # parser.add_argument('--start_imsi', type=int, default=999700000000302, help='MAL: This is the starting point for for ues-imsi' , required=True)
    # parser.add_argument('--mal_ues', type=int, help='This variable takes in the number of UEs to be started' , required=True)
    # parser.add_argument('--attack_type', required=True,type=int, default=1, help='This variable can take 3 values.\n 1 for Registration + PDU session \n, 2 for Registration only')
    # parser.add_argument('--repeat', type=int,default=0, help='This variable takes 1 or 0 based on if we want the UEs to be started and stopped in a loop or not', required=True)
    # parser.add_argument('--timeout', type=int,default=10, help='This variable takes in the timeout value for the attack', required=True)
    # parser.add_argument('--processes', type=int,default=0, help='This variable takes in the number of processes to be run in parallel (MAX 500)', required=True)
    # parser.add_argument('--delay_between', type=float,default=0.5, help='This variable takes in the delay between each UE', required=True)

    # # parser.add_argument('--count', type=int, help='no of times this code runs' , required=True)

    # args = parser.parse_args()

    # pdu_session = args.pdu_session
    # ben_ues = args.ben_ues
    # ben_delay = args.ben_delay

    # start_imsi = args.start_imsi
    # mal_ues = args.mal_ues
    # attack_type = args.attack_type
    # repeat = args.repeat
    # timeout = args.timeout
    # processes = args.processes
    # mal_delay = args.delay_between

    # count = args.count
    

    pdu_session = 1
    start_imsi = 999700000000501
    count = i = 1
    processes = 100
    attack_type = 1

#--------------------------------------------------------------1--------------------------------------------------------------#
    mal_ues = 25
    mal_delay = .5
    timeout = 700
    ben_ues = 300
    ben_delay = 1
    repeat = 1 

    run(pdu_session, ben_ues, ben_delay, start_imsi, mal_ues, attack_type, repeat, timeout, processes, mal_delay, i)
    print("1 Done")
#--------------------------------------------------------------!--------------------------------------------------------------#

#--------------------------------------------------------------1--------------------------------------------------------------#
    mal_ues = 20
    mal_delay = .5
    timeout = 700
    ben_ues = 300
    ben_delay = 1
    repeat = 1 

    run(pdu_session, ben_ues, ben_delay, start_imsi, mal_ues, attack_type, repeat, timeout, processes, mal_delay, i)
    print("2 Done")
#--------------------------------------------------------------!--------------------------------------------------------------#

#--------------------------------------------------------------1--------------------------------------------------------------#
    mal_ues = 15
    mal_delay = .5
    timeout = 700
    ben_ues = 300
    ben_delay = 1
    repeat = 1 

    run(pdu_session, ben_ues, ben_delay, start_imsi, mal_ues, attack_type, repeat, timeout, processes, mal_delay, i)
    print("3 Done")
#--------------------------------------------------------------!--------------------------------------------------------------#

#--------------------------------------------------------------1--------------------------------------------------------------#
    mal_ues = 10
    mal_delay = .5
    timeout = 700
    ben_ues = 300
    ben_delay = 1
    repeat = 1 

    run(pdu_session, ben_ues, ben_delay, start_imsi, mal_ues, attack_type, repeat, timeout, processes, mal_delay, i)
    print("4 Done")
#--------------------------------------------------------------!--------------------------------------------------------------#

#--------------------------------------------------------------1--------------------------------------------------------------#
    mal_ues = 5
    mal_delay = .5
    timeout = 700
    ben_ues = 300
    ben_delay = 1
    repeat = 1 

    run(pdu_session, ben_ues, ben_delay, start_imsi, mal_ues, attack_type, repeat, timeout, processes, mal_delay, i)
    print("5 Done")
#--------------------------------------------------------------!--------------------------------------------------------------#

#--------------------------------------------------------------1--------------------------------------------------------------#
    mal_ues = 0
    mal_delay = .5
    timeout = 700
    ben_ues = 300
    ben_delay = 1
    repeat = 1 

    run(pdu_session, ben_ues, ben_delay, start_imsi, mal_ues, attack_type, repeat, timeout, processes, mal_delay, i)
    print("6 Done")
#--------------------------------------------------------------!--------------------------------------------------------------#


    print("Done")