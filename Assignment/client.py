import socket
import threading
import sys

server_name = sys.argv[1]
server_port = int(sys.argv[2])
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientSocket.connect((server_name, server_port))

def recv_server():
    clientSocket.send(input("Username: ").encode())
    message = clientSocket.recv(2048).decode()
    if message == 'unregistered':
        print("New User")

if __name__ == "__main__":
    
    recv_server()

