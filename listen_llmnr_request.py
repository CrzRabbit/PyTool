import socket
import struct
import random

def pack_data():
    hostname = 'google.com'
    dataformate = '>HHHHHHB{0}sBHHHHH'.format(len(hostname))
    data = struct.pack(dataformate,
                       0xCAFE,  #trans ID
                       0x0000,  # Flags: Standard Query
                       0x0001,  # Questions = 1
                       0x0000,  # Answer RRs = 0
                       0x0000,  # Authority RRs = 0
                       0x0000,  # Additional RRs = 0
                       len(hostname),
                       hostname.encode('utf-8'),  #hostname
                       0x00,
                       0x0001,  # host address
                       0x0001,  # Class: IN
                       0x0000,  # MAC addr
                       0x0000,
                       0x0009
                       )

server_socket4 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket4.bind(('224.0.0.252', 5355))

print('Server is running...')

while True:
    data, addr = server_socket4.recvfrom(1024)
    print(data)
    server_socket4.sendto(pack_data(), addr)