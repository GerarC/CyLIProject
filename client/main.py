import socket

HOST = "192.168.1.12"
PORT = 9000
BUFFSZ = 1024

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST,PORT))
    s.sendall("Hello World".encode())
    data = s.recv(1024)

print(f"Received {data.decode()}")

