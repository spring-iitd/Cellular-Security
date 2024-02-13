import random
import time
import subprocess

if __name__ == "__main__": 
    """
    Attack Type 1 = Sends Registration and PDU session request
    Attack Type 2 = Sends Registration request only
    Attack Type 3 = Sends PDU session request only (Not implemented yet)
    """

    number_of_attacks_per_sec = 20
    period = 2 # seconds

    ranges = [ (i, i+period) for i in range(0,10**5,period)]
    # print(ranges)
    when_to_launch = []

    for each in ranges: 
        for i in range(each[0], each[1]):
            for j in range(number_of_attacks_per_sec):
                when_to_launch.append(random.uniform(0,1) + i)

    when_to_launch = sorted(when_to_launch)
    print(when_to_launch)
    print(len(when_to_launch))
    
    for i in when_to_launch:
        cmd = "nr-ue --imsi imsi-"+str(start_imsi)+ " -c UERANSIM/config/open5gs-ue.yaml -n " + str(number_of_ues) + " -t " + str(delay_bw) + " &"
