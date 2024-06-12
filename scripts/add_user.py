import sys
import os


if __name__ == "__main__": 

    no_of_ues_to_add = int(sys.argv[1])
    base_supi = 999700000000001
    key ="465B5CE8B199B49FAA5F0A2EE238A6BC"
    op = "E8ED289DEBA952E4283B54E88E6183CA"

    for i in range(0, no_of_ues_to_add + 1):
        supi = str(base_supi + i)
        command = "sudo open5gs-dbctl add " + supi + " " + str(key) + " " + str(op)
        output = os.system(command)
        print("UE with IMSI: " + str(base_supi + i) + " added")
