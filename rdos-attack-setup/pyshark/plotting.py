import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import numpy as np


def make_fig(ben_file, mal_file):
    csv1 = pd.read_csv(ben_file)
    csv2 = pd.read_csv(mal_file)
    csv1['timestamp'] = csv1['timestamp'].apply(lambda _: datetime.strptime(_,"%Y-%m-%d %H:%M:%S.%f"))
    csv2['timestamp'] = csv2['timestamp'].apply(lambda _: datetime.strptime(_,"%Y-%m-%d %H:%M:%S.%f"))
    csv2['timestamp2'] = csv2['timestamp2'].apply(lambda _: datetime.strptime(_,"%Y-%m-%d %H:%M:%S.%f"))
    


    plt.scatter(csv1['timestamp'],csv1['diff1'], label='Connections on RAN-1', color='red', marker='o')
    plt.scatter(csv2['timestamp'],csv2['diff1'], label='Connections on RAN-2', color='blue', marker='x')    
    
    # Labeling the axes and adding a title

    plt.xlabel('Instance at which the registration request was received')
    # plt.xaxis_date()

    plt.ylabel('Time Taken For Registrations (ms)')
    plt.title('Registration Time Analysis')
    plt.tight_layout()
    plt.legend()
    # save the above plot as a file
    plt.savefig('analysis/'+ben_file.split('.')[0] + '.png', dpi=300)
    plt.clf()
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

    plt.scatter(csv1['timestamp'],csv1['diff1'], label='Connections on RAN-1', color='red', marker='o', s=5)
    plt.plot(pending['timestamp'],pending['value'], color = 'green', linestyle = 'solid')
    plt.legend()
    plt.tight_layout()
    plt.savefig('analysis/'+ben_file.split('.')[0] + '2.png', dpi=300 )
    plt.clf()
    plt.close()    

if __name__ == "__main__":
    x = ["reg_mal1_captured_traffic-timeout-255-ben-255-delay-2-mal-500-delay-0.csv", "reg_ben1_captured_traffic-timeout-255-ben-255-delay-2-mal-500-delay-0.csv"]
    ben_file = x[1]
    mal_file = x[0]
    make_fig(ben_file, mal_file)
    make_fig2(ben_file, mal_file)


    x = ["reg_ben1_captured_traffic-timeout-250-ben-250-delay-2-mal-500-delay-0-count-1_updated.csv" , "reg_mal1_captured_traffic-timeout-250-ben-250-delay-2-mal-500-delay-0-count-1_updated.csv" ]
    ben_file = x[0]
    mal_file = x[1]
    make_fig(ben_file, mal_file)
    make_fig2(ben_file, mal_file)

    x  = ["reg_ben1_captured_traffic-timeout-255-ben-255-delay-2-mal-500-delay-0.csv" , "reg_mal1_captured_traffic-timeout-255-ben-255-delay-2-mal-500-delay-0.csv"  ]
    ben_file = x[0]
    mal_file = x[1]
    make_fig(ben_file, mal_file)
    make_fig2(ben_file, mal_file)

    x = ["reg_ben1_captured_traffic-timeout-375-ben-375-delay-2-mal-750-delay-0-count-1_updated.csv" , "reg_mal1_captured_traffic-timeout-375-ben-375-delay-2-mal-750-delay-0-count-1_updated.csv"]
    ben_file = x[0]
    mal_file = x[1]
    make_fig(ben_file, mal_file)
    make_fig2(ben_file, mal_file)

    x = ["reg_ben1_captured_traffic-timeout-382-ben-382-delay-2-mal-750-delay-0.csv" , "reg_mal1_captured_traffic-timeout-382-ben-382-delay-2-mal-750-delay-0.csv"]
    ben_file = x[0]
    mal_file = x[1]
    make_fig(ben_file, mal_file)
    make_fig2(ben_file, mal_file)

    x = ["reg_ben1_captured_traffic-timeout-510-ben-510-delay-2-mal-1000-delay-0.csv" , "reg_mal1_captured_traffic-timeout-510-ben-510-delay-2-mal-1000-delay-0.csv"]
        
    ben_file = x[0]
    mal_file = x[1]
    make_fig(ben_file, mal_file)
    make_fig2(ben_file, mal_file)