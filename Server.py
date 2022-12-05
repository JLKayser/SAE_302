import socket, threading
import sys , os , subprocess
import psutil



def cmd(cmd):
    try:
        if cmd.lower() == 'os':
            x = sys.platform
            if x == 'win32':
                x = 'OS de la machine est Windows'
            elif x == 'linux' or x == 'linux2':
                x = 'OS de la machine est Linux'
            elif x == 'darwin':
                x = 'OS de la machine est MAC OS X'
            return x
        if cmd.lower() == 'ram':
            x = str(f'- Total Memory: {psutil.virtual_memory()[0]} bytes\n - Used Memory: {psutil.virtual_memory()[1]} bytes\n - Free Memory: {psutil.virtual_memory()[4]} bytes')
            return f'RAM:\n {x}'
        if cmd.lower() == 'cpu':
            x = psutil.cpu_percent()
            return f'Capacity CPU: {x} %'
        if cmd.lower() == 'ip':
            host = socket.gethostname()
            x = socket.gethostbyname(host)
            return x
        if cmd.lower() == 'name':
            x = socket.gethostname()
            return x
        if cmd.lower() == 'help':
            return ("""CMD HELP:
    - IP
    - NAME
    - RAM
    - OS
    - CPU
    - KILL
    - RESET
    - DISCONNECT""")
    except:
        pass


class ClientThread(threading.Thread):
    def __init__(self,clientAddress,clientsocket):
        threading.Thread.__init__(self)
        self.csocket = clientsocket
        print ("New connection added: ", clientAddress)


    def run(self):
        print ("Connection from : ", clientAddress)
        #self.csocket.send(bytes("Hi, This is from Server..",'utf-8'))
        while True:
            try:
                data = self.csocket.recv(1024)
                if data is not None:
                    msg = data.decode()
                    if msg.lower() == 'disconnect':
                        self.csocket.close()
                        break
                    if msg.lower() == 'kill':
                        self.csocket.send("Kill".encode())
                        server.close()
                        break
                    self.csocket.send(cmd(msg).encode())
            except:
                pass
        print ("Client at ", clientAddress, " disconnected...")


PORT = int(input('Please enter a port: '))
ADDRESS = '0.0.0.0'
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((ADDRESS, PORT))

msg = ''
print("Server started")
print("Waiting for client request..")
while True:
    server.listen(1)
    clientsock, clientAddress = server.accept()
    newthread = ClientThread(clientAddress, clientsock)
    newthread.start()
