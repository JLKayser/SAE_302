import socket, threading
import sys , os , subprocess


def ipconfig():
    cmd = str(subprocess.check_output('ipconfig',shell=True))
    x = cmd.replace('\\r',"").replace('\\b','').replace('\\n','\n').replace('\\xff','')
    return x


def hostname():
    cmd = str(subprocess.check_output('hostname',shell=True))
    x = cmd.replace('\\r', "").replace('\\b', '').replace('\\n', '\n').replace('\\xff', '').replace('b',"")
    return x


def os_command():
    cmd = sys.platform
    if cmd == 'win32':
        cmd = 'L\'os de la machine est Windows 10'
    x = cmd.replace('\\r', "").replace('\\b', '').replace('\\n', '\n').replace('\\xff', '')
    return x


def reset():
    x = sys.argv[0]
    cmd = os.system(x + ' py')
    return cmd


class ClientThread(threading.Thread):
    def __init__(self,clientAddress,clientsocket):
        threading.Thread.__init__(self)
        self.csocket = clientsocket
        print ("New connection added: ", clientAddress)


    def run(self):
        print ("Connection from : ", clientAddress)
        #self.csocket.send(bytes("Hi, This is from Server..",'utf-8'))
        msg = ''
        while True:
            data = self.csocket.recv(2048)
            msg = data.decode()
            if msg=='disconnect':
              break
            if msg=='kill':
                server.close()
                break
            if msg=='reset':
                reset()
                break
            if msg=='ip':
                self.csocket.send(ipconfig().encode())
            if msg=='hostname':
                self.csocket.send(hostname().encode())
            if msg=='os':
                self.csocket.send(os_command().encode())
            print ("from client", msg)
        print ("Client at ", clientAddress , " disconnected...")


PORT = 5500
ADDRESS = '127.0.0.1'
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((ADDRESS, PORT))

print("Server started")
print("Waiting for client request..")
while True:
    server.listen(1)
    clientsock, clientAddress = server.accept()
    newthread = ClientThread(clientAddress, clientsock)
    newthread.start()
