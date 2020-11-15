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
    Content_list = []
    Message_list = []
    File_list = []

    def __init__(self,title, author):
        self.title = title
        self.author = author
        self.Content_list = []
        self.Message_list = []
        self.File_list = []
        with open(self.title,"w") as file:
            file.write(self.author)
            file.write("\n")
    
    def post_message(self,username,message):
        flag = 1
        new_message = Message(username,message)
        self.Content_list.append(new_message)
        self.Message_list.append(new_message)
        with open(self.title, "w") as file:
            first_line = self.author + "\n"
            file.write(first_line)
            for content in self.Content_list:
                if content.type == "message":
                    tmp = str(flag) + " " + username + ": " + content.text + "\n"
                    file.write(tmp)
                flag += 1
            with open(self.title, "a") as file:
                for content in self.Content_list:
                    if content.type == "file":
                        tmp = username + "uploaded" + content.filename
                        file.write(tmp)

class Message:
    author = ""
    text = ""
    type = "message"
    def __init__(self,author,text):
        self.author = author
        self.text = text

class File:
    author = ""
    filename = ""
    type = "file"

    def __init__(self,filename,author):
        self.filename = filename
        self.author = author

class Thread_sys:
    ThreadList = dict()
    
    def __init__(self):
        self.ThreadList = dict()

    def create_new_thread(self,title,author):
        if title not in self.ThreadList:
            self.ThreadList[title] = Thread(title,author)
            return True
        return False
    
    def ListThread(self):
        content = ""
        for title in self.ThreadList.keys():
            content = content + title
            content = content + "\n"
        if content == "":
            return False
        else:
            content = content[:-1]
        return content


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
            elif command == "LST":
                thread_list = thread_sys.ListThread()
                if thread_list == False:
                    send_message = "Empty"
                    server.send(send_message.encode())
                else:
                    server.send(thread_list.encode())
            elif command == "MSG":
                title = content[1]
                if title not in thread_sys.ThreadList:
                    send_message = "unsuccess"
                    server.send(send_message.encode())
                    print("Thread " + title + " is not exists")
                else:
                    message = ""
                    length = len(content)
                    i = 2
                    while i < length:
                        message += content[i]
                        message += " "
                        i += 1
                    thread_sys.ThreadList[title].post_message(username,message)
                    send_message = "success"
                    server.send(send_message.encode())
                    print("Message posted to " + title + " thread")
                    
                    

if __name__ == "__main__":
    thread_sys = Thread_sys()
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
