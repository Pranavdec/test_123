#!/bin/bash

# VM Monitoring (run inside VM)
vm_monitor() {
    LOG_FILE="/tmp/vm_stats.log"
    echo "Monitoring VM resources..."
    pidstat -G "YOUR_PROCESS_NAME" -urdh 1 > "$LOG_FILE" &
    PIDSTAT_PID=$!
    
    # Network monitoring
    IFACE=$(ip route | awk '/default/{print $5}')
    sar -n DEV 1 > "/tmp/vm_network.log" &
    SAR_PID=$!
    
    trap "kill $PIDSTAT_PID $SAR_PID; vm_summary" SIGINT
    wait
}

vm_summary() {
    echo -e "\n===== VM Averages ====="
    awk '/Average:/ {cpu+=$8; mem+=$10; io_read+=$6; io_write+=$7; count++} 
         END {printf "CPU: %.1f%%\nMemory: %.1f kB\nDisk Read: %.1f kB/s\nDisk Write: %.1f kB/s\n", 
         cpu/count, mem/count, io_read/count, io_write/count}' /tmp/vm_stats.log
    
    echo -e "\n===== Network Averages ====="
    awk '/Average/ && $2 == "'"$IFACE"'" {rx+=$5; tx+=$6; count++} 
         END {printf "%s: RX %.1f KB/s, TX %.1f KB/s\n", "'"$IFACE"'", rx/count, tx/count}' /tmp/vm_network.log
}

# Host Monitoring (run on host)
host_monitor() {
    LOG_FILE="/tmp/host_stats.log"
    echo "Monitoring host VM processes..."
    pidstat -G "qemu|VirtualBox|vmware" -urdh 1 > "$LOG_FILE" &
    PIDSTAT_PID=$!
    
    # Network monitoring for virtual interfaces
    sar -n DEV 1 > "/tmp/host_network.log" &
    SAR_PID=$!
    
    trap "kill $PIDSTAT_PID $SAR_PID; host_summary" SIGINT
    wait
}

host_summary() {
    echo -e "\n===== Host Averages ====="
    awk '/Average:/ {cpu+=$8; mem+=$10; io_read+=$6; io_write+=$7; count++} 
         END {printf "CPU: %.1f%%\nMemory: %.1f kB\nDisk Read: %.1f kB/s\nDisk Write: %.1f kB/s\n", 
         cpu/count, mem/count, io_read/count, io_write/count}' /tmp/host_stats.log
    
    echo -e "\n===== Virtual Network ====="
    awk '/Average/ && $2 ~ /virbr|vnet|vmnet/ {rx+=$5; tx+=$6; count++} 
         END {printf "RX %.1f KB/s\nTX %.1f KB/s\n", rx/count, tx/count}' /tmp/host_network.log
}

# Choose mode based on argument
case "$1" in
    vm)
        vm_monitor
        ;;
    host)
        host_monitor
        ;;
    *)
        echo "Usage: $0 [vm|host]"
        exit 1
        ;;
esac
