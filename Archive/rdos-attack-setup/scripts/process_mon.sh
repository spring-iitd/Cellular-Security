
#!/bin/bash

process_pid=$(pgrep open5gs-amfd)
output_file="utilization.log"
echo "Time, CPU (%), Memory (%)" > "$output_file"
while ps -p "$process_pid" > /dev/null; do
    result=$(pidstat -p "$process_pid" -u -r 1 1 | awk 'NR==4 {cpu_usage=$8} NR==7 {memory_usage=$8} END {print cpu_usage, memory_usage}')
    cpu_utilization=$(echo "$result" | awk '{print $1}')
    mem_utilization=$(echo "$result" | awk '{print $2}')
    timestamp=$(date +%s)
    echo "$timestamp, $cpu_utilization, $mem_utilization " >> "$output_file"
done