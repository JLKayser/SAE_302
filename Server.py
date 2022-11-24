import socket, threading
import sys , os


def ipconfig():
    cmd = os.system('ipconfig')
    return cmd


def hostname():
    cmd = os.system('hostname')
    return cmd


def os_command():
    cmd = sys.platform
    if cmd == 'win32':
        cmd = 'L\'os de la machine est Windows 10'
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
            if msg=='bye':
              break
            if msg=='ip':
                self.csocket.send(ipconfig())
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
