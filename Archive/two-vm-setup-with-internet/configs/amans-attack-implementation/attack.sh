#/bin/sh

while :
do
        sudo ./build/nr-ue -c config/open5gs-ue_1.yaml &
        # sudo ./build/nr-ue -c config/open5gs-ue_2.yaml &
        # sudo ./build/nr-ue -c config/open5gs-ue_3.yaml &
        # sudo ./build/nr-ue -c config/open5gs-ue_4.yaml &
        # sudo ./build/nr-ue -c config/open5gs-ue_5.yaml &
        # sudo ./build/nr-ue -c config/open5gs-ue_6.yaml &
        sleep 2
        # processId1 = $(ps -ef | grep 'sudo ./build/nr-ue -c config/open5gs_ue_1.yaml' | grep -v 'grep' | awk '{ printf $2 }')
        # processId2 = $(ps -ef | grep 'sudo ./build/nr-ue -c config/open5gs-ue_2.yaml' | grep -v 'grep' | awk '{ printf $2 }')
        # processId3 = $(ps -ef | grep 'sudo ./build/nr-ue -c config/open5gs-ue_3.yaml' | grep -v 'grep' | awk '{ printf $2 }')
        # processId4 = $(ps -ef | grep 'sudo ./build/nr-ue -c config/open5gs_ue_4.yaml' | grep -v 'grep' | awk '{ printf $2 }')
        # processId5 = $(ps -ef | grep 'sudo ./build/nr-ue -c config    /open5gs-ue_5.yaml' | grep -v 'grep' | awk '{ printf $2 }')
        # processId6 = $(ps -ef | grep 'sudo ./build/nr-ue -c config/open5gs-ue_6.yaml' | grep -v 'grep' | awk '{ printf $2 }')
        # kill -9 $processId1
        # kill -9 $processId2
        # kill -9 $processId3
        # kill -9 $processId4
        # kill -9 $processId5
        # kill -9 $processId6        
done
