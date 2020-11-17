import socket
import threading
import sys
import os

server_name = sys.argv[1]
server_port = int(sys.argv[2])
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientSocket.connect((server_name, server_port))

def recv_hurder():
    # while loop for login process
    while True:
        # while loop for check the user whether has readly login
        while True:
            username = input("Enter username: ")
            clientSocket.send(username.encode())
            message = clientSocket.recv(2048).decode()
            if message == "uncontinues":
                print(username + " has already logged in")
            elif message == "continues":
                send_message = "next"
                clientSocket.send(send_message.encode())
                break
        
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

    # while loop for command process
    while True:
        command_menu = "Enter one of the following commands: CRT, MSG, DLT, EDT, LST, RDT, UDP, DWN, RMV, XIT, SHT: "
        content = input(command_menu)
        clientSocket.send(content.encode())
        content = content.split(" ")
        command = content[0]
        recv_message = clientSocket.recv(2048).decode()
        # invalid command
        if recv_message == "Invalid":
            print("Invalid commmand")
        # command format incorrect
        elif recv_message == "incorrect":
            print("Incorrect syntax for " + command)
        else:
            # command CRT
            if command == "CRT":
                title = content[1]
                if recv_message == "success":
                   print("Thread " + title + " created")
                else:
                    print("Thread " + title + " exists" )
            # command LST
            elif command == "LST":
                if recv_message == "Empty":
                    print("No threads to list")
                else:
                    print("The list of active threads:")
                    print(recv_message)
            # command MSG
            elif command == "MSG":
                title = content[1]
                if recv_message == "unsuccess":
                    print("Thread " + title + " is not exists")
                else:
                    print("Message posted to " + title + " thread")
            # command XIT
            elif command == "XIT":
                if recv_message == "success":
                    print("Goodbye")
                break
            # command RMV
            elif command == "RMV":
                title = content[1]
                if recv_message == "notexists":
                    print("Thread " + title + " not exists")
                elif recv_message == "unsuccess":
                    print("The thread was created by another user and cannot be removed")
                elif recv_message == "success":
                    print("Thread " + title + " removed")
            # command RDT
            elif command == "RDT":
                title = content[1]
                if recv_message == "notexists":
                    print("Thread " + title + " does not exists")
                else:
                    print(recv_message)
            # command EDT
            elif command == "EDT":
                if recv_message == "unsuccess":
                    print("The message belongs to another user and cannot be edited")
                else:
                    print("The message has been edited")
            # command DLT
            elif command == "DLT":
                if recv_message == "unsuccess":
                    print("The message belongs to another user and cannot be deleted")
                else:
                    print("The message has been deleted")
            # command UDP
            elif command == "UDP":
                title = content[1]
                file_name = content[2]
                # the thread is exists
                if recv_message == "exists":
                    # get the file size
                    size = os.path.getsize(file_name)
                    send_message = str(size)
                    # send the size to server
                    clientSocket.send(send_message.encode())
                    recv_message = clientSocket.recv(2048).decode()
                    if recv_message == "next":
                        with open(file_name, "rb") as file:
                            send_message = file.read()
                        clientSocket.send(send_message)
                        recv_message = clientSocket.recv(2048).decode()
                        if recv_message == "success":
                            print(file_name + " uploaded to " + title + " thread")
                else:
                    print("Thread does not exists")
            # command DWN
            elif command == "DWN":
                title = content[1]
                file_name = content[2]
                # handler thread noe exists
                if recv_message == "nottitle":
                        print("Thread does not exists")
                elif recv_message == "notexists":
                    print("File does not exist in Thread " + title)
                else:
                    size = int(recv_message)
                    send_message = "download"
                    clientSocket.send(send_message.encode())
                    recv_message = clientSocket.recv(size)
                    # write download file content into new file
                    with open(file_name, "wb") as file:
                        file.write(recv_message)
                    print(file_name + " successfully downloaded")


if __name__ == "__main__":
    
    recv_hurder()

