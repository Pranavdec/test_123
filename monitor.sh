#!/bin/bash

# VM Monitoring (run inside VM)
vm_monitor() {
    LOG_FILE="/tmp/vm_stats.log"
    echo "Monitoring resource_stress process..."
    
    pidstat -G "resource_stress" -urdh 1 > "$LOG_FILE" &
    PIDSTAT_PID=$!
    
    IFACE=$(ip route | awk '/default/{print $5}')
    sar -n DEV 1 > "/tmp/vm_network.log" &
    SAR_PID=$!
    
    trap "kill $PIDSTAT_PID $SAR_PID; ./analyze.py vm" SIGINT
    wait
}

# Host Monitoring (run on host)
host_monitor() {
    LOG_FILE="/tmp/host_stats.log"
    echo "Monitoring host VM processes..."
    pidstat -G "qemu|VirtualBox|vmware" -urdh 1 > "$LOG_FILE" &
    PIDSTAT_PID=$!
    
    sar -n DEV 1 > "/tmp/host_network.log" &
    SAR_PID=$!
    
    trap "kill $PIDSTAT_PID $SAR_PID; ./analyze.py host" SIGINT
    wait
}

case "$1" in
    vm) vm_monitor ;;
    host) host_monitor ;;
    *) echo "Usage: $0 [vm|host]"; exit 1 ;;
esac
