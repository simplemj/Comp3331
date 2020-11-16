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
        username = input("Enter username: ")
        clientSocket.send(username.encode())
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
        elif recv_message == "incorrect":
            print("Incorrect syntax for " + command)
        else:
            if command == "CRT":
                title = content[1]
                if recv_message == "success":
                   print("Thread " + title + " created")
                else:
                    print("Thread " + title + " exists" )
            elif command == "LST":
                if len(content) != 1:
                    print("Incorrect syntax for LST")
                elif recv_message == "Empty":
                    print("No threads to list")
                else:
                    print("The list of active threads:")
                    print(recv_message)
            elif command == "MSG":
                title = content[1]
                if recv_message == "unsuccess":
                    print("Thread " + title + " is not exists")
                else:
                    print("Message posted to " + title + " thread")
            elif command == "XIT":
                if recv_message == "success":
                    print("Goodbye")
                break
            elif command == "RMV":
                title = content[1]
                if recv_message == "notexists":
                    print("Thread " + title + " not exists")
                elif recv_message == "unsuccess":
                    print("The thread was created by another user and cannot be removed")
                elif recv_message == "success":
                    print("Thread " + title + " removed")
            elif command == "RDT":
                title = content[1]
                if recv_message == "notexists":
                    print("Thread " + title + " does not exists")
                else:
                    print(recv_message)
            elif command == "EDT":
                if recv_message == "unsuccess":
                    print("The message belongs to another user and cannot be edited")
                else:
                    print("The message has been edited")
            elif command == "DLT":
                if recv_message == "unsuccess":
                    print("The message belongs to another user and cannot be deleted")
                else:
                    print("The message has been deleted")
            elif command == "UDP":
                title = content[1]
                file_name = content[2]
                if recv_message == "exists":
                    with open(file_name, "rb") as file:
                        send_message = file.read()
                    clientSocket.send(send_message)
                    recv_message = clientSocket.recv(2048).decode()
                    if recv_message == "success":
                        print(1)
                else:
                    print("Thread does not exists")




            

        

if __name__ == "__main__":
    
    recv_hurder()

