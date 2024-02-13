import pyshark
import os 
import csv
import argparse
import multiprocessing
import time
import sys
"""

"""
def extract_info_from_pcapng (display_filter, pcapng_file): 
    """ 
    This function extracts the information from a pcapng file and returns a csv file and a pcap file
    """
    filename = pcapng_file.split('.')[0]
    os.system("mkdir _extraction")
    os.system('tshark -r '+ pcapng_file + ' -Y "' + display_filter + '" -w _extraction/' + filename +'.pcap')
    
    return '_extraction/'+filename+".pcap"

def save_to_csv(type_of_data,filename, data):
    """ 
    This function saves the data to a csv file
    """    
    with open(type_of_data+filename+".csv", "w") as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=',')
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
    for i in display_filter: 

        # reducing the file size based on the display filter
        extracted_files = extract_info_from_pcapng(display_filter[i], filename)

        ngap_ids = lists_ngap_ids (extracted_files, display_filter[i])

        unique_ngap_ids = [int(i) for i in set(ngap_ids)]
        unique_ngap_ids.sort()

        
        inputs = [(extracted_files, attack_type, x) for x in unique_ngap_ids]

        print("Starting multiprocessing")
        pool = multiprocessing.Pool(processes=4)

        ss = pool.starmap(process_pcap_regitsration, inputs)
        # print(ss)

        pool.close()
        pool.join()


        save_to_csv("reg_" +str(i) + str(attack_type) + "_" , filename.split('.')[0], ss)

    os.system("rm -rf _extraction")

if __name__ == "__main__":

    ## REMEMBER THE DISPLAY FILTER SHOULD END WITH ngap.RAN_UE_NGAP_ID
    display_filter = {"ben":"(ip.src==192.168.56.120 or ip.dst==192.168.56.120) and ngap.RAN_UE_NGAP_ID" , "mal":"(ip.src==192.168.56.121 or ip.dst==192.168.56.121) and ngap.RAN_UE_NGAP_ID"}
    # display_filter = {"ben":"(ip.src==192.168.56.120 or ip.dst==192.168.56.120) and ngap.RAN_UE_NGAP_ID"}
    # display_filter = {"mal":"(ip.src==192.168.56.121 or ip.dst==192.168.56.121) and ngap.RAN_UE_NGAP_ID"}
    # filename = "captured_traffic.pcap"
    # filename = "captured_traffic_updated.pcap"
    # filename = "captured_traffic-timeout-250-ben-250-delay-2-mal-500-delay-0-count-1.pcap"
    # output_file = "to_plot.csv"
    attack_type = 1
    to_run =  ["captured_traffic-timeout-250-ben-250-delay-2-mal-500-delay-0-count-1_updated.pcap" ,  "captured_traffic-timeout-255-ben-255-delay-2-mal-500-delay-0.01-count-1_updated.pcap" ,  "captured_traffic-timeout-255-ben-255-delay-2-mal-500-delay-0.01-count-1-repeat-1_updated.pcap" ,  "captured_traffic-timeout-255-ben-255-delay-2-mal-500-delay-0.01-count-1-repeat-1.pcap" ,  "captured_traffic-timeout-375-ben-375-delay-2-mal-750-delay-0-count-1_updated.pcap" ,  "captured_traffic-timeout-382-ben-382-delay-2-mal-750-delay-0.01-count-1_updated.pcap" ,  "captured_traffic-timeout-510-ben-510-delay-2-mal-1000-delay-0.01-count-1_updated.pcap" ,  "captured_traffic-timeout-600-ben-600-delay-2-mal-1000-delay-0.1-count-1_updated.pcap" ,  "captured_traffic-timeout-714-ben-714-delay-2-mal-1400-delay-0.01-count-1_updated.pcap" ,  "captured_traffic-timeout-765-ben-765-delay-2-mal-1500-delay-0.01-count-1_updated.pcap" ]

    for file in to_run: 
        do_analysis(file, display_filter, attack_type)