import sys
import time
import math
import socket
import threading
import os
import signal
import setproctitle  # Install with: pip install setproctitle

def exit_handler(signum, frame):
    print("\n=== Stress test completed ===")
    print("Resources released. Exiting cleanly.")
    os._exit(0)

# Set unique process name
setproctitle.setproctitle("resource_stress")

# Register signal handler
signal.signal(signal.SIGINT, exit_handler)
signal.signal(signal.SIGTERM, exit_handler)

# CPU stress
def cpu_load():
    while True:
        [math.sqrt(i**2) for i in range(1_000_000)]

# Memory stress
def mem_load():
    data = bytearray()
    try:
        while True:
            data.extend(bytearray(1024*1024))  # 1MB chunks
            time.sleep(0.1)
    except MemoryError:
        pass

# Network stress
def net_load():
    def server():
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(('', 12345))
            s.listen()
            while True:
                conn, addr = s.accept()
                with conn:
                    while True:
                        data = conn.recv(1024)
                        if not data: break

    def client():
        while True:
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.connect(('127.0.0.1', 12346))
                    s.sendall(b'X' * 1024)
            except:
                time.sleep(0.1)

    threading.Thread(target=server, daemon=True).start()
    threading.Thread(target=client, daemon=True).start()

# I/O stress
def io_load():
    while True:
        with open('iotest.dat', 'wb') as f:
            f.write(os.urandom(1024*1024))  # 1MB
        os.remove('iotest.dat')
        

        
if __name__ == '__main__':
    print(f"Stress test PID: {os.getpid()}")
    print("=== Starting stress test ===")
    
    threading.Thread(target=cpu_load, daemon=True).start()
    threading.Thread(target=mem_load, daemon=True).start()
    threading.Thread(target=net_load, daemon=True).start()
    threading.Thread(target=io_load, daemon=True).start()
    
    try:
        time.sleep(60)
        print("completed")
        exit(0)
    except KeyboardInterrupt:
        exit_handler(None, None)
