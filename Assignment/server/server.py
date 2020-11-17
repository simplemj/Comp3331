import socket
import sys
import threading
import os

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
    # command MSG
    def post_message(self,username,message):
        flag = 1
        # create new Message
        new_message = Message(username,message)
        # add to the All content list and message list
        self.Content_list.append(new_message)
        self.Message_list.append(new_message)
        # update the file
        with open(self.title, "w") as file:
            first_line = self.author + "\n"
            file.write(first_line)
            for content in self.Content_list:
                if content.type == "file":
                    tmp = content.author + " uploaded " + content.filename + "\n"
                    file.write(tmp)
                else:
                    tmp = str(flag) + " " + content.author + ": " + content.text + "\n"
                    file.write(tmp)
                    flag += 1
    # command RDT
    def read_thread(self):
        flag = 1
        result = ""
        # copy content list to result string
        for content in self.Content_list:
            if content.type == "file":
                result = result + content.author + " uploaded " + content.filename + "\n"
            else:
                result = result + str(flag) + " " + content.author + ": " + content.text + "\n"
                flag += 1
        result = result[:-1]
        return result
    # command EDT
    def edit_message(self,username,message_number,message):
        # check the message author whether same as username
        if self.Message_list[message_number-1].author == username:
            self.Message_list[message_number-1].text = message
            flag = 1
            # update thread content file
            with open(self.title, "w") as file:
                first_line = self.author + "\n"
                file.write(first_line)
                for content in self.Content_list:
                    if content.type == "file":
                        tmp = content.author + " uploaded " + content.filename + "\n"
                        file.write(tmp)
                    else:
                        tmp = str(flag) + " " + content.author + ": " + content.text + "\n"
                        file.write(tmp)
                        flag += 1
            return True
        return False
    # command DLT
    def delete_message(self,username,message_number):
        if self.Message_list[message_number-1].author == username:
            # remove content list
            self.Content_list.remove(self.Message_list[message_number-1])
            # remove message list
            self.Message_list.remove(self.Message_list[message_number-1])
            flag = 1
            # update thread content file
            with open(self.title, "w") as file:
                first_line = self.author + "\n"
                file.write(first_line)
                for content in self.Content_list:
                    if content.type == "file":
                        tmp = content.author + " uploaded " + content.filename + "\n"
                        file.write(tmp)
                    else:
                        tmp = str(flag) + " " + content.author + ": " + content.text + "\n"
                        file.write(tmp)
                        flag += 1
            return True
        return False
    # command UDP
    def upload_file(self,title,filename,username,content):
        # create new file
        file = File(filename,username)
        # add new file into content list and file list
        self.Content_list.append(file)
        self.File_list.append(file)
        # write content to file
        with open(title + "-" + filename, "wb") as file:
            file.write(content)
        flag = 1
        # update thread content file
        with open(self.title, "w") as file:
            first_line = self.author + "\n"
            file.write(first_line)
            for content in self.Content_list:
                if content.type == "file":
                    tmp = content.author + " uploaded " + content.filename + "\n"
                    file.write(tmp)
                else:
                    tmp = str(flag) + " " + content.author + ": " + content.text + "\n"
                    file.write(tmp)
                    flag += 1
    # command DWN
    def download_file(self,filename):
        for file in self.File_list:
            # find the file
            if file.filename == filename:
                # read the DWN file content return it
                with open(self.title + "-" + filename,"rb") as content:
                    result = content.read()
                return result
        # if not exist return false
        return False
    
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

# Thread_sys include all thread data
class Thread_sys:
    ThreadList = dict()
    user_list = []
    def __init__(self):
        self.ThreadList = dict()
        self.user_list = []
    # command CRT
    def create_new_thread(self,title,author):
        if title not in self.ThreadList:
            self.ThreadList[title] = Thread(title,author)
            return True
        return False
    # command LST
    def ListThread(self):
        content = ""
        # iterate all title
        for title in self.ThreadList.keys():
            content = content + title
            content = content + "\n"
        if content == "":
            return False
        else:
            content = content[:-1]
        return content
    # command DLT   
    def delete_thread(self,title):
        os.remove(title)
        del self.ThreadList[title]
    # add user to login list
    def login(self,username):
        self.user_list.append(username)
    # remove user to login list
    def logout(self,username):
        self.user_list.remove(username)

def init_data():
    # read credentials.txt
    with open("credentials.txt", "r") as file:
        content = file.read().splitlines()
        for text in content:
            if text != "":
                data = text.split(" ")
                username, password = data[0], data[1]
                credentials[username] = password
# add new user to credential file
def create_new_user(username, password):
    credentials.update({username: password})
    with open("credentials.txt", "a") as fp:
        fp.write("\n" + username + " " + password)
# implement invalid command 
def command_handler(command,content):
    length1_command = {"LST", "XIT"}
    length2_command = {"CRT", "RDT", "RMV", "SHT"}
    length3_commmand = {"DLT", "UPD", "DWN"}
    greater_than3_command = {"MSG","EDT"}
    if command in length1_command and len(content) == 1:
        return True
    elif command in length2_command and len(content) == 2:
        return True
    elif command in length3_commmand and len(content) == 3:
        return True
    elif command in greater_than3_command and len(content) >= 3:
        return True
    return False

def recv_handler(server,connectionsocket):
    flag = 1
    
    # while loop for login
    while True:
        # set flag only print once
        if flag == 1:
            print("Client connected")
            flag += 1
        # while loop for check the user whether has readly login
        while True:
            username = server.recv(2048).decode()
            # check the user whether in user login list
            if username in thread_sys.user_list:
                send_message = "uncontinues"
                server.send(send_message.encode())
                print(username + " has already logged in")
            else:
                send_message = "continues"
                server.send(send_message.encode())
                break
        # check the user whether is new user
        recv_message = server.recv(2048).decode()    
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
        # check the password whether is correct
        if(credentials[username] == password):
            message = "success"
            server.send(message.encode())
            print(username + " successful login")
            thread_sys.login(username)
            break
        print("Incorrect password")
        message = "unsuccess"
        server.send(message.encode())
    
    # while loop for command process
    while True:
        # recv command string 
        recv_message = server.recv(2048).decode()
        # splite the string into a list
        content = recv_message.split(" ")
        commandList = {"CRT", "MSG", "DLT", "EDT", "LST", "RDT", "UPD", "DWN", "RMV", "XIT", "SHT"}
        command = content[0]
        send_message = ""
        # check the command whether in command list
        if command not in commandList:
            send_message = "Invalid"
            server.send(send_message.encode())
        else:
            # check the command format whether match the list
            if command_handler(command,content) == False:
                send_message = "incorrect"
                server.send(send_message.encode())
            else:
                print(username + " issued " + command + " command")
                # command CRT
                if command == "CRT":
                    title = content[1]
                    # check the thread whether has been created 
                    if thread_sys.create_new_thread(title,username) == True:
                        send_message = "success"
                        server.send(send_message.encode())
                        print("Thread " + title + " created")
                    else:
                        send_message = "unsuccess"
                        server.send(send_message.encode())
                # command LST
                elif command == "LST":
                    thread_list = thread_sys.ListThread()
                    # check the list whether size is 0
                    if thread_list == False:
                        send_message = "Empty"
                        server.send(send_message.encode())
                    else:
                        server.send(thread_list.encode())
                # command MSG
                elif command == "MSG":
                    title = content[1]
                    # check the thread whether is exist
                    if title not in thread_sys.ThreadList:
                        send_message = "unsuccess"
                        server.send(send_message.encode())
                        print("Thread " + title + " is not exists")
                    else:
                        message = ""
                        length = len(content)
                        # combine the post message into one list
                        i = 2
                        while i < length:
                            message += content[i]
                            message += " "
                            i += 1
                        thread_sys.ThreadList[title].post_message(username,message)
                        send_message = "success"
                        server.send(send_message.encode())
                        print("Message posted to " + title + " thread")
                # command XIT
                elif command == "XIT":
                    print(username + " exited")
                    # logout the current user
                    thread_sys.logout(username)
                    # check whether has other user has login
                    if len(thread_sys.user_list) == 0:
                        print("Waiting for clients")
                    send_message = "success"
                    server.send(send_message.encode())
                    break
                # command RMV
                elif command == "RMV":
                    title = content[1]
                    # check the thread title whether in thread list
                    if title not in thread_sys.ThreadList:
                        send_message = "notexists"
                        print("Thread " + title + " is not exists")
                    else:
                        # check the current user whether is the thread author
                        if thread_sys.ThreadList[title].author != username:
                            send_message = "unsuccess"
                            print("Thread " + title + " cannot be removed")
                        else:
                            thread_sys.delete_thread(title)
                            send_message = "success"
                            print("Thread " + title + " removed")
                    server.send(send_message.encode())
                # command RDT
                elif command == "RDT":
                    title = content[1]
                    # check the thread title whether in thread list
                    if title not in thread_sys.ThreadList:
                        send_message = "notexists"
                        print("Incorrect thread specified")
                    else:
                        send_message = thread_sys.ThreadList[title].read_thread()
                        if send_message == "":
                            print("Thread " + title + " is empty")
                        else: 
                            print("Thread " + title + " read")
                    server.send(send_message.encode())
                # command EDT
                elif command == "EDT":
                    title = content[1]
                    message_number = int(content[2])
                    # check the thread title whether in thread list
                    if title not in thread_sys.ThreadList:
                        send_message = "notexists"
                        print("Incorrect thread specified")
                    else:
                        # combine the command message
                        message = ""
                        length = len(content)
                        i = 3
                        while i < length:
                            message += content[i]
                            message += " "
                            i += 1
                        # check the thread message whether has been edit successfully
                        if thread_sys.ThreadList[title].edit_message(username,message_number, message) == False:
                            send_message = "unsuccess"
                            print("Message cannot be edited")
                        else:
                            send_message = "success"
                            print("Message has been edited")
                        server.send(send_message.encode())
                # command DLT
                elif command == "DLT":
                    title = content[1]
                    message_number = int(content[2])
                    # check the current user whether can delete that message
                    if thread_sys.ThreadList[title].delete_message(username,message_number) == False:
                            send_message = "unsuccess"
                            print("Message cannot be deleted")
                    else:
                        send_message = "success"
                        print("Message has been deleted")
                    server.send(send_message.encode())
                # command UDP
                elif command == "UPD":
                    title = content[1]
                    filename = content[2]
                    # check the thread title whether in thread list
                    if title not in thread_sys.ThreadList:
                        send_message = "notexists"
                    else:
                        send_message = "exists"
                    server.send(send_message.encode())
                    recv_message = server.recv(2048).decode()
                    # recv the binary file size
                    size = int(recv_message)
                    send_message = "next"
                    server.send(send_message.encode())
                    # recv the binary file
                    content = server.recv(size)
                    thread_sys.ThreadList[title].upload_file(title,filename,username,content)
                    print(username + " uploaded file " + filename + " to " + title + " thread")
                    send_message = "success"
                    server.send(send_message.encode())
                # command DWN
                elif command == "DWN":
                    title = content[1]
                    filename = content[2]
                    # check the thread title whether in thread list
                    if title not in thread_sys.ThreadList:
                        send_message = "nottitle"
                        server.send(send_message.encode())
                        print("Thread " + title + " does not exists")
                    else:
                        download_file = thread_sys.ThreadList[title].download_file(filename)
                        # check the thread whether exist
                        if  download_file == False:
                            send_message = "notexists"
                            server.send(send_message.encode())
                            print(filename + " does not exist in Thread " + title)
                        else:
                            # get the size of download file
                            size = os.path.getsize(title + "-" +filename)
                            send_message = str(size)
                            server.send(send_message.encode())
                            if server.recv(2048).decode() == "download":
                                server.send(download_file)
                                print(filename + " downloaded from Thread " + title)
                    

if __name__ == "__main__":
    # create thread system 
    thread_sys = Thread_sys()
    # read all the data for system
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
