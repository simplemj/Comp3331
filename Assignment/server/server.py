import socket
import sys
import threading

localhost = '127.0.0.1'
port_number = int(sys.argv[1])
Admin_password = sys.argv[2]
credentials = dict()

class Thread:
    title = ""
    author = ""
    MessageList = []

    def __init__(self,title, author):
        self.title = title
        self.author = author
        self.MessageList = []
        with open(self.title,"w") as file:
            file.write(self.author)
            file.write("\n")

class Message:
    author = ""
    text = ""
    def __init__(self,author,text):
        self.author = author
        self.text = text

class Thread_sys:
    ThreadList = None
    
    def __init__(self):
        self.ThreadList = dict()

    def create_new_thread(self,title,author):
        if title not in self.ThreadList:
            self.ThreadList[title] = Thread(title,author)
            return True
        return False


def init_data():

    # read credentials.txt
    with open("credentials.txt", "r") as file:
        content = file.read().splitlines()
        for text in content:
            if text != "":
                data = text.split(" ")
                username, password = data[0], data[1]
                credentials[username] = password

def create_new_user(username, password):
    credentials.update({username: password})
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
    
    thread_sys = Thread_sys()
    while True:
        recv_message = server.recv(2048).decode()
        content = recv_message.split(" ")
        commandList = {"CRT", "MSG", "DLT", "EDT", "LST", "RDT", "UDP", "DWN", "RMV", "XIT", "SHT"}
        command = content[0]
        if command not in commandList:
            send_message = "Invalid"
            server.send(send_message.encode())
        else:
            print(username + " issued " + command + " command")
            if command == "CRT":
                title = content[1]
                if thread_sys.create_new_thread(title,username) == True:
                    send_message = "success"
                    server.send(message.encode())
                else:
                    send_message = "unsuccess"
                    server.send(send_message.encode())
                    
        




if __name__ == "__main__":
    init_data()
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverSocket.bind(('127.0.0.1', port_number))
    serverSocket.listen(5)
    print("Waiting for clients")
    while True:
        conn, addr = serverSocket.accept()
        serverThread = threading.Thread(target=recv_handler, args=(conn, addr))
        serverThread.daemon = True
        serverThread.start()
