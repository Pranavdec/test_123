#!/usr/bin/env python3
import sys
import re

def parse_vm_stats():
    cpu_sum = mem_sum = read_sum = write_sum = count = 0
    try:
        f = open('/tmp/vm_stats.log', 'r')
        for line in f:
            if 'resource_stress' in line:
                parts = line.split()
                cpu_sum += float(parts[9])
                mem_sum += float(parts[15])
                read_sum += float(parts[16])
                write_sum += float(parts[17])
                count += 1
        f.close()
    except (FileNotFoundError, IndexError, ValueError):
        pass
    
    print("\n===== VM Averages =====")
    if count > 0:
        print("Average CPU%: ", cpu_sum/count)
        print("Average MEM%: ", mem_sum/count)
        print("Average READ Kb/s: ", read_sum/count)
        print("Average WRITE Kb/s: ", write_sum/count)
    else:
        print("No VM process data found")

def parse_host_stats():
    cpu_sum = mem_sum = read_sum = write_sum = count = 0
    try:
        f = open('/tmp/host_stats.log', 'r')
        for line in f:
            if 'resource_stress' in line:
                parts = line.split()
                cpu_sum += float(parts[9])
                mem_sum += float(parts[15])
                read_sum += float(parts[16])
                write_sum += float(parts[17])
                count += 1
        f.close()
    except (FileNotFoundError, IndexError, ValueError):
        pass
    
    print("\n===== Host Averages =====")
    if count > 0:
        print("Average CPU%: ", cpu_sum/count)
        print("Average MEM%: ", mem_sum/count)
        print("Average READ Kb/s: ", read_sum/count)
        print("Average WRITE Kb/s: ", write_sum/count)
    else:
        print("No host process data found")

def parse_network_stats(mode):
    rx_sum = tx_sum = count = ifutil = 0
    target_iface = None
    log_file = '/tmp/vm_network.log' if mode == 'vm' else '/tmp/host_network.log'
    
    try:
        if mode == 'vm':
            f = open(log_file, 'r')
            for line in f:
                if 'IFACE' not in line:
                    parts = line.split()
                    if len(parts) > 10:
                        rx_sum += float(parts[6])
                        tx_sum += float(parts[7])
                        ifutil += float(parts[11])
                        count += 1
            f.close()
        else:
            f = open(log_file, 'r')
            for line in f:
                if 'IFACE' not in line:
                    parts = line.split()
                    if len(parts) > 10:
                        rx_sum += float(parts[6])
                        tx_sum += float(parts[7])
                        ifutil += float(parts[11])
                        count += 1
            f.close()
    except (FileNotFoundError, IndexError, ValueError):
        pass
    
    print("\n===== Network Averages =====")
    if count > 0:
        if mode == 'vm':
            print("Average RX Kb/s: ", rx_sum/count)
            print("Average TX Kb/s: ", tx_sum/count)
            print("Average IFUTIL %: ", ifutil/count)
        else:
            print("Average RX Kb/s: ", rx_sum/count)
            print("Average TX Kb/s: ", tx_sum/count)
            print("Average IFUTIL %: ", ifutil/count)
    else:
        print("No network data found")

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: analyze.py [vm|host]")
        sys.exit(1)
    
    mode = sys.argv[1]
    if mode == 'vm':
        parse_vm_stats()
        parse_network_stats('vm')
    elif mode == 'host':
        parse_host_stats()
        parse_network_stats('host')
    else:
        print("Invalid mode. Use 'vm' or 'host'")
        sys.exit(1)
