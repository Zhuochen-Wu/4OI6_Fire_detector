import serial
import socket
import threading
import time

# TCP server settings
TCP_IP = '0.0.0.0'
TCP_PORT = 10000

# Open the serial port for reading
ser = serial.Serial('/dev/ttyACM0', 9600)

# Function to handle incoming TCP connections
def handle_connection(conn, addr):
    print(f"New client connected: {addr}")
    
    while True:
        try:
            line = ser.readline().decode().strip()
        except Exception as e:
            print(f"Error reading serial port: {e}")
            break
        
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        message = f"{timestamp}: {line}"
        print(message)
        try:
            conn.sendall(message.encode())
        except Exception as e:
            print(f"Error sending data over TCP: {e}")
            break
    
    conn.close()
    print(f"Client disconnected: {addr}")

# Start the TCP server
tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
tcp_socket.bind((TCP_IP, TCP_PORT))
tcp_socket.listen(1)
print(f"TCP server listening on {TCP_IP}:{TCP_PORT}")

while True:
    # Wait for a new client to connect
    conn, addr = tcp_socket.accept()

    # Handle the connection in a new thread
    threading.Thread(target=handle_connection, args=(conn, addr)).start()
