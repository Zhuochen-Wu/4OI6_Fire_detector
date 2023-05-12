import socket

# TCP client settings
TCP_IP = '192.168.50.1'
TCP_PORT = 10000

# Connect to the server
tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp_socket.connect((TCP_IP, TCP_PORT))

# Receive data from the server
while True:
    data = tcp_socket.recv(1024).decode().strip()
    if not data:
        break
    print(data)

# Close the connection
tcp_socket.close()
