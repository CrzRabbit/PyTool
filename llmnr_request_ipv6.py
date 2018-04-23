import socket
import struct
import random

if __name__ == '__main__':

    client_socket4 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_socket6 = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
    hostname = 'gprs-pc'
    dataformate = '>HHHHHHB{0}sBHH'.format(len(hostname))
    data = struct.pack(dataformate,
                       random.randint(0, 65535),  #trans ID
                       0x0000,  #Flags: Standard Query
                       0x0001,  #Questions = 1
                       0x0000,  #Answer RRs = 0
                       0x0000,  #Authority RRs = 0
                       0x0000,  #Additional RRs = 0
                       len(hostname),
                       hostname.encode('utf-8'),  #hostname
                       0x00,
                       0x0001,  # host address
                       0x0001   # Class: IN
                       )
    print(data)
    client_socket4.sendto(data, ('224.0.0.252', 5355))
    client_socket6.sendto(data, ('FF02:0:0:0:0:0:1:3', 5355))
    print(client_socket4.recvfrom(1024).decode('utr-8'))
    print(client_socket6.recvfrom(1024).decode('utf-8'))