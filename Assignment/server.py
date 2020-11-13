import socket
import sys
import threading

localhost = '127.0.0.1'
port_number = int(sys.argv[1])
Admin_password = sys.argv[2]

class User:
    User_name = ""
    Password = ""
    State = False

    def __init__(self,Username,Password):
        self.Password = Password
        self.User_name = Username
        self.State = False

class User_file:
    UserList = dict()
    file_name = ""
    def __init__(self,fileName):
        self.file_name = fileName
        self.UserList = dict()
        with open(self.file_name,'r') as file:
            line = file.read().splitlines()
            for content in line:
                if content != "":
                    data = content.split(" ")
                    username = data[0]
                    password = data[1]
                    self.UserList[username] = User(username,password)



def recv_handler(connectionsocket):
    while True:
        datarecv, _ = connectionsocket.recvfrom(1024)
        clientcommand = datarecv.decode()
        if not clientcommand:
            print("!!!!Exception: Client connection close without logout!!!!")
            break
    connectionsocket.close()



if __name__ == "__main__":
    socketserver = socket.socket(socket.AF_INET,socket.SOCK_STREAM) 
    socketserver.bind((localhost, port_number))
    socketserver.listen(5)
    print("Waiting for client")
    while True:
        connectionsocket, address = socketserver.accept()
        client_thread = threading.Thread(name="client_thread", target= recv_handler, args=(connectionsocket,))
        client_thread.daemon=True
        client_thread.start()
