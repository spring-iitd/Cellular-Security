import pyshark
import os 
import csv
import argparse
"""

"""
def extract_info_from_pcapng (display_filter, pcapng_file): 
    """ 
    This function extracts the information from a pcapng file and returns a csv file and a pcap file
    """
    filename = pcapng_file.split('.')[0]
    os.system("mkdir _extraction")
    os.system('tshark -r '+ pcapng_file + ' -Y "' + display_filter + '" -w _extraction/' + filename +'.pcap')
    os.system('tshark -r _extraction/'+filename+'.pcap -T fields -e frame.number -e _ws.col.Info -E separator=, > _extraction/'+filename+'.csv')

    return ['_extraction/'+filename+".csv", '_extraction/'+filename+".pcap"]

def save_to_csv(type_of_data,filename, data):
    """ 
    This function saves the data to a csv file
    """    
    with open(type_of_data+filename+".csv", "w") as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=',')
        for key in data:
            csv_writer.writerow([key, data[key]])

def read_and_map_info(file_path_csv, file_path_pcap): 
    """ 
    This function reads a csv file which has two columns and returns a dictionary of them
    The first column is the key and the second column is the value
    The csv file should not have any header
    """
    pcap = pyshark.FileCapture(file_path_pcap, keep_packets=True, use_json=True)
    with open(file_path_csv, "r") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        frame_info = {}
        for row in csv_reader: 
            f_no = int(row[0])
            frame_info[f_no] = [', '.join(row[1:]), pcap[f_no - 1].sniff_time]
            if 'udp' in pcap[f_no - 1]:
                frame_info[f_no].append(pcap[f_no - 1].udp.stream)
    pcap.close()
    return frame_info

def process_pcap_regitsration(mapped_pcap, attack_type):
    # Flags
    rrc_setup_request = "RRC Setup Request"
    downlink_transport = "DownlinkNASTransport"
    downlink_info_transfer = "DL Information Transfer"
    inital_context_response = "InitialContextSetupResponse"
    pdu_session_request = "PDUSessionResourceSetupRequest"
    pdu_session_response = "PDUSessionResourceSetupResponse"
    
    # Flag Variables 
    seen_flag = False
    # Time Variables
    frames_used = []
    time_start = 0
    time_end = 0
    mapped_stream_with_time = {}
    # Stream Variables
    stream_id = 0 
    count = 0 

    if attack_type == 1: 
        for frame_no in mapped_pcap:
            if rrc_setup_request in mapped_pcap[frame_no][0]:
                time_start = mapped_pcap[frame_no][1]
                stream_id = mapped_pcap[frame_no][2]

                seen_flag = True
                count += 1

            if seen_flag == True and pdu_session_response in mapped_pcap[frame_no][0]:
                time_end = mapped_pcap[frame_no][1]
                mapped_stream_with_time[count] = round((time_end - time_start).total_seconds() * 1000, 3)
                
                # resetting the variables
                seen_flag = False
                time_start = 0
                time_end = 0
                stream_id = 0
                # frames_used = []

              

    return mapped_stream_with_time

if __name__ == "__main__":
    
    # Defining the arguments for the script
    parser = argparse.ArgumentParser(description='''it does the analysis of a given pcap file and writes the results to a csv file. ''')
    parser.add_argument("-f","--file",type=str, help="pcap file to analyze", default="captured_traffic.pcap")
    parser.add_argument("-d","--display_filter",type=str, help="This is the display filter to use", default="((ip.src==192.168.56.130 and ip.dst == 192.168.56.120) or (ip.src == 192.168.56.120 and ip.dst == 192.168.56.130 ) or (ip.src == 192.168.56.102 and ip.dst == 192.168.56.120) or (ip.src == 192.168.56.120 and ip.dst == 192.168.56.102 )) and  (nr-rrc || ngap || nas-5gs)")
    parser.add_argument("-o","--output",type=str, help="output file name")

    parser.add_argument('-a','--attack_type', required=False,type=int, default=1, help='This variable can take 3 values.\n 1 for Registration + PDU session \n, 2 for Registration only\n 3 for PDU session only')
    args=parser.parse_args()
    
    # assigning the arguments to variables
    display_filter = args.display_filter
    display_filter = "(ip.src==192.168.56.121 or ip.dst==192.168.56.121) and ngap.RAN_UE_NGAP_ID"

    filename = args.file
    output_file = args.output
    attack_type = args.attack_type


    # reducing the file size based on the display filter
    extracted_files = extract_info_from_pcapng(display_filter, filename)
    # extracted_files = ['_extraction/captured_traffic.csv', '_extraction/captured_traffic.pcap']

    # # reading the reduced file and extracting the frame info
    # mapped_pcap = read_and_map_info(extracted_files[0], extracted_files[1])
    # # print(mapped_pcap)        

    # # processing the pcap file
    # processed_file = process_pcap_regitsration(mapped_pcap, attack_type)
    
    # print(processed_file)
    # # saving the data to csv file
    # save_to_csv("registration_" + str(attack_type) + "_" , filename.split('.')[0], processed_file)

    # os.system("rm -rf _extraction")