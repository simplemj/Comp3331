import socket
import threading
import sys

server_name = sys.argv[1]
server_port = int(sys.argv[2])
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientSocket.connect((server_name, server_port))

def recv_hurder():
    # login process
    while True:
        clientSocket.send(input("Enter username: ").encode())
        message = clientSocket.recv(2048).decode()
    
        # Enter password
        if message == "registered":
            clientSocket.send(input("Enter password: ").encode())
        else:
            clientSocket.send(input("Enter new password for " + message + ": ").encode())

        status = clientSocket.recv(2048).decode()
        if status == "success":
            print("Welcome to the forum")
            break
        elif status == "unsuccess":
            print("Invalid password")
            continue

    # command process
    while True:
        command_menu = "Enter one of the following commands: CRT, MSG, DLT, EDT, LST, RDT, UDP, DWN, RMV, XIT, SHT: "
        content = input(command_menu)
        clientSocket.send(content.encode())
        content = content.split(" ")
        command = content[0]
        recv_message = clientSocket.recv(2048).decode()
        if recv_message == "Invalid":
            print("Invalid commmand")
        else:
            if command == "CRT":
                title = content[1]
                if recv_message == "success":
                   print("Thread " + title + " created")
                else:
                    print("Thread " + title + " exists" )

            

        

if __name__ == "__main__":
    
    recv_hurder()

