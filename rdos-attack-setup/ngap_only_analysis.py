import pyshark
import os 
import csv
import argparse
import multiprocessing
import time
import sys

import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import numpy as np

"""

"""
def extract_info_from_pcapng (display_filter, pcapng_file): 
    """ 
    This function extracts the information from a pcapng file and returns a csv file and a pcap file
    """
    filename = pcapng_file.split('.')[0]
    print(filename, display_filter)
    os.system("mkdir _extraction")
    os.system('tshark -r '+ pcapng_file + ' -Y "' + display_filter + '" -w _extraction/' + filename +'.pcap')
    
    return '_extraction/'+filename+".pcap"

def save_to_csv(type_of_data,filename, data):
    """ 
    This function saves the data to a csv file
    """    
    with open(type_of_data+filename+".csv", "w") as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=',')
        csv_writer.writerow(["count","timestamp","timestamp2","diff1"]) 
        for key in data:
            csv_writer.writerow(key)

def process_pcap_regitsration(extracted_file, attack_type, ngap_id):
    display_filter = "ngap.RAN_UE_NGAP_ID == " + str(ngap_id)
    os.system('tshark -r '+ extracted_file + ' -Y "' + display_filter + '" -w ' + extracted_file.split('.')[0] + str(ngap_id) +'.pcap')
    
    extracted_files = extracted_file.split('.')[0] + str(ngap_id) +'.pcap'

    time_start = 0
    time_end = 0
    time_diff = 0
    order = 0 

    pcap = pyshark.FileCapture(extracted_files, keep_packets=True)

    for pkt in pcap: 
        for ngap in [i for i in pcap[int(pkt.number)-1].layers if ('ngap' == i._layer_name  and i.ran_ue_ngap_id == str(ngap_id))] :
            if ngap.has_field('initialuemessage_element') and order == 0 :
                time_start = pkt.sniff_time
                order = 1
            elif order == 1 and ngap.has_field('nas_5gs_mm_message_type') and str(ngap.nas_5gs_mm_message_type) == '0x44': 
                order = 8
            elif order == 8 and ngap.has_field('uecontextreleasecomplete_element'):
                time_end = pkt.sniff_time
                time_diff = round((time_end - time_start).total_seconds() * 1000, 3)
                continue
            elif order == 1 and ngap.has_field('successfuloutcome_element') and ngap.has_field('initialcontextsetupresponse_element') : 
                order = 2
            elif order == 2 and ngap.has_field('uplinknastransport_element'):
                order = 3
            elif attack_type == 2 and order == 3 and ngap.has_field('downlinknastransport_element'):
                time_end = pkt.sniff_time
                time_diff = round((time_end - time_start).total_seconds() * 1000, 3)
                continue
            elif attack_type == 1 and order == 3 and ngap.has_field('downlinknastransport_element'):
                order = 4
            elif attack_type == 1 and order == 4 and ngap.has_field('pdusessionresourcesetuprequest_element'): 
                order = 5
            elif attack_type == 1 and order == 5 and ngap.has_field('pdusessionresourcesetupresponse_element'):
                time_end = pkt.sniff_time
                time_diff = round((time_end - time_start).total_seconds() * 1000, 3)

    pcap.close()
    return (ngap_id, time_start, time_end, time_diff)

def lists_ngap_ids(file_path_pcap, display_filter):
    """ 
    This function returns a list of all the ngap ids
    """
    ngap_ids = []

    pcap = pyshark.FileCapture(file_path_pcap, keep_packets=True)# display_filter=display_filter)
    for pkt in pcap: 
        for ngap in [i for i in pcap[int(pkt.number)-1].layers if 'ngap' == i._layer_name] :
            ngap_ids.append(ngap.ran_ue_ngap_id)
    pcap.close()
    return ngap_ids

def do_analysis(filename, display_filter, attack_type):
    lis = []
    for i in display_filter: 

        # reducing the file size based on the display filter
        extracted_files = extract_info_from_pcapng(display_filter[i], filename)

        ngap_ids = lists_ngap_ids (extracted_files, display_filter[i])

        unique_ngap_ids = [int(i) for i in set(ngap_ids)]
        unique_ngap_ids.sort()

        
        inputs = [(extracted_files, attack_type, x) for x in unique_ngap_ids]

        print("Starting multiprocessing")
        pool = multiprocessing.Pool(processes=50)

        ss = pool.starmap(process_pcap_regitsration, inputs)
        # print(ss)

        pool.close()
        pool.join()
        print("Ending multiprocessing")
        name = "reg_" +str(i) + str(attack_type) + "_" + filename.split('.')[0] + ".csv"
        lis.append(name)
        save_to_csv("reg_" +str(i) + str(attack_type) + "_" , filename.split('.')[0], ss)

    os.system("rm -rf _extraction")
    return lis

def make_fig1(ben_file):
    
    csv1 = pd.read_csv(ben_file)
    
    csv1['timestamp'] = csv1['timestamp'].apply(lambda _: datetime.strptime(_,"%Y-%m-%d %H:%M:%S.%f"))

    plt.scatter(csv1['timestamp'],csv1['diff1'], label='Connections on RAN-1', color='red',s=5)
    
    # Labeling the axes and adding a title

    plt.xlabel('Instance at which the registration request was received')
    # plt.xaxis_date()

    plt.ylabel('Time Taken For Registrations (ms)')
    plt.title('Registration Time Analysis')
    plt.tight_layout()
    plt.legend()
    # save the above plot as a file
    plt.savefig('analysis/'+ben_file.split('.')[0] + '.png', dpi=300)
    plt.close()

def make_fig2(ben_file, mal_file):
    csv1 = pd.read_csv(ben_file)
    csv2 = pd.read_csv(mal_file)
    csv1['timestamp'] = csv1['timestamp'].apply(lambda _: datetime.strptime(_,"%Y-%m-%d %H:%M:%S.%f"))
    csv2['timestamp'] = csv2['timestamp'].apply(lambda _: datetime.strptime(_,"%Y-%m-%d %H:%M:%S.%f"))
    csv2['timestamp2'] = csv2['timestamp2'].apply(lambda _: datetime.strptime(_,"%Y-%m-%d %H:%M:%S.%f"))
    
    pending = pd.DataFrame(columns=['timestamp', 'value'])

    # Iterate through each row in csv1
    for index1, row1 in csv1.iterrows():
        timestamp_csv1 = row1['timestamp']
        # print(timestamp_csv1, "-------------------", type(timestamp_csv1))
        # print(csv2['timestamp'], "-------------------", type(csv2['timestamp']))   
        # break
        # Filter csv2 based on the conditions
        filtered_csv2 = csv2[(csv2['timestamp'] < timestamp_csv1) & (csv2['timestamp'] > timestamp_csv1)]

        # count the number of elements in filtered_csv2
        selected = len(filtered_csv2.index) * 100
        # print(selected, "-------------------")
        pending.loc[row1['count']] = [row1['timestamp'], selected]


    plt.scatter(csv1['timestamp'],csv1['diff1'], label='Connections on RAN-1', color='red', marker='o')
    plt.scatter(csv2['timestamp'],csv2['diff1'], label='Connections on RAN-2', color='blue', marker='x')    
    
    # Labeling the axes and adding a title

    plt.xlabel('Instance at which the registration request was received')


    plt.scatter(csv1['timestamp'],csv1['diff1'], label='Connections on RAN-1', color='red', marker='o', s=5)
    plt.plot(pending['timestamp'],pending['value'], color = 'green', linestyle = 'solid')
    plt.legend()
    plt.tight_layout()
    plt.savefig('analysis/'+ben_file.split('.')[0] + '2.png', dpi=300 )
    plt.close()
    
if __name__ == "__main__":

    ## REMEMBER THE DISPLAY FILTER SHOULD END WITH ngap.RAN_UE_NGAP_ID
    # display_filter = {"ben":"(ip.src==192.168.56.120 or ip.dst==192.168.56.120) and ngap.RAN_UE_NGAP_ID" , "mal":"(ip.src==192.168.56.121 or ip.dst==192.168.56.121) and ngap.RAN_UE_NGAP_ID"}
    display_filter = {"ben":"(ip.src==192.168.56.120 or ip.dst==192.168.56.120) and ngap.RAN_UE_NGAP_ID"}
    attack_type = 1
    # to_run = ["captured_traffic-timeout-700-ben-300-delay-1-mal-25-delay-05-count-1-repeat-1.pcap", "captured_traffic-timeout-700-ben-300-delay-1-mal-20-delay-05-count-1-repeat-1.pcap", "captured_traffic-timeout-700-ben-300-delay-1-mal-15-delay-05-count-1-repeat-1.pcap" , "captured_traffic-timeout-700-ben-300-delay-1-mal-10-delay-05-count-1-repeat-1.pcap"]
    to_run = ["captured_traffic-timeout-700-ben-300-delay-1-mal-0-delay-05-count-1-repeat-1.pcap"]
    # x = ["reg_ben1_captured_traffic-timeout-700-ben-300-delay-1-mal-20-delay-05-count-1-repeat-1.csv", "reg_ben1_captured_traffic-timeout-700-ben-300-delay-1-mal-25-delay-05-count-1-repeat-1.csv"]
    for file in to_run: 
        l = do_analysis(file, display_filter, attack_type)
        # make_fig1(file)


