import socket
import sys
import threading

localhost = '127.0.0.1'
port_number = int(sys.argv[1])
Admin_password = sys.argv[2]
credentials = dict()



def init_data():

    # read credentials.txt
    with open("credentials.txt", "r") as file:
        content = file.read().splitlines()
        for text in content:
            if text != "":
                data = text.split(" ")
                user, pwd = data[0], data[1]
                credentials[user] = pwd

def create_new_user(username, password):

    credentials.update({username: password})

    # update credentials.txt
    with open("credentials.txt", "a") as fp:
        fp.write("\n" + username + " " + password)

def recv_handler(server,connectionsocket):
    flag = 1
    
    # Determine if the user is registered
    while True:
        if flag == 1:
            print("Client connected")
            flag += 1

        username = server.recv(2048).decode()
        if username in credentials:
            message = "registered"
            server.send(message.encode())
            password = server.recv(2048).decode()
        else:
            print("New user")
            message = username
            server.send(message.encode())
            password = server.recv(2048).decode()
            create_new_user(username, password)
        
        
        if(credentials[username] == password):
            message = "success"
            server.send(message.encode())
            print(username + " successful login")
            break
        print("Incorrect password")
        message = "unsuccess"
        server.send(message.encode())

    while True:
        message = server.recv(2048).decode()
        




if __name__ == "__main__":
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverSocket.bind(('127.0.0.1', port_number))
    serverSocket.listen(5)
    init_data()
    print("Waiting for clients")
    while True:
        conn, addr = serverSocket.accept()
        serverThread = threading.Thread(target=recv_handler, args=(conn, addr))
        serverThread.daemon = True
        serverThread.start()
