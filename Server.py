import socket, threading
import sys , os , subprocess


def ipconfig():
    cmd = str(subprocess.check_output('ipconfig',shell=True))
    x = cmd.replace('\\r',"").replace('\\b','').replace('\\n','\n').replace('\\xff','').replace("'",'')
    return x


def hostname():
    cmd = str(subprocess.check_output('hostname',shell=True))
    x = cmd.replace('\\r', "").replace('\\b', '').replace('\\n', '\n').replace('\\xff', '').replace('b',"").replace("'",'')
    return x


def os_command():
    cmd = sys.platform
    if cmd == 'win32':
        cmd = 'OS de la machine est Windows 10'
    x = cmd.replace('\\r', "").replace('\\b', '').replace('\\n', '\n').replace('\\xff', '').replace("'",'')
    return x

def ram():
    cmd = str(subprocess.check_output('wmic memphysical get MaxCapacity', shell=True))
    x = cmd.replace('\\r', "").replace('\\b', '').replace('\\n', '').replace('\\xff', '').replace('b', "").replace("'",'')
    return f'{x} KB'


'''def reset():
    x = sys.argv[0]
    cmd = os.system(x + ' py')
    return cmd'''


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
                data = self.csocket.recv(2048)
                if data is not None:
                    msg = data.decode()
                    if msg == 'disconnect':
                      break
                    if msg == 'kill':
                        server.close()
                        break
                    '''if msg=='reset':
                        reset()
                        break'''
                    if msg == 'ip':
                        self.csocket.send(ipconfig().encode())
                    if msg == 'hostname':
                        self.csocket.send(hostname().encode())
                    if msg == 'os':
                        self.csocket.send(os_command().encode())
                    if msg == 'ram':
                        self.csocket.send(ram().encode())
                    print ("from client", msg)
            except:
                print("Client disconnected")
                self.csocket.close()
                break
        print ("Client at ", clientAddress, " disconnected...")


PORT = 5500
ADDRESS = '127.0.0.1'
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
