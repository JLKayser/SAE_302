import socket, threading
import sys , os , subprocess
import psutil


def ipconfig():
    host = socket.gethostname()
    cmd = socket.gethostbyname(host)
    x = cmd.replace('\\r', "").replace('\\b', '').replace('\\n', '\n').replace('\\xff', '').replace("'", '')
    return x


def hostname():
    cmd = str(subprocess.check_output('hostname',shell=True))
    x = cmd.replace('\\r', "").replace('\\b', '').replace('\\n', '\n').replace('\\xff', '').replace('b',"").replace("'",'')
    return x


def os_command():
    cmd = sys.platform
    if cmd == 'win32':
        cmd = 'OS de la machine est Windows'
    if cmd == 'linux' or cmd == 'linux2':
        cmd = 'OS de la machine est Linux'
    if cmd == 'darwin':
        cmd = 'OS de la machine est MAC OS X'
    x = cmd.replace('\\r', "").replace('\\b', '').replace('\\n', '\n').replace('\\xff', '').replace("'",'')
    return x

def ram():
    cmd = str(subprocess.check_output('wmic memphysical get MaxCapacity', shell=True))
    x = cmd.replace('\\r', "").replace('\\b', '').replace('\\n', '').replace('\\xff', '').replace('b', "").replace("'",'')
    return f'RAM {x}KB'


def aide():
    return ('CMD HELP:\n'
            '- IP\n'
            '- HOSTNAME\n'
            '- RAM\n'
            '- OS\n'
            '- CPU\n')


def cpu():
    cmd = psutil.cpu_percent()
    return f'Capacity CPU: {cmd} %'


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
                    if msg.lower() == 'disconnect':
                      break
                    if msg.lower() == 'kill':
                        self.csocket.send("Kill".encode())
                        server.close()
                        break
                    '''if msg=='reset':
                        reset()
                        break'''
                    if msg.lower() == 'ip':
                        self.csocket.send(ipconfig().encode())
                    if msg.lower() == 'hostname':
                        self.csocket.send(hostname().encode())
                    if msg.lower() == 'os':
                        self.csocket.send(os_command().encode())
                    if msg.lower() == 'ram':
                        self.csocket.send(ram().encode())
                    if msg.lower() == 'help':
                        self.csocket.send(aide().encode())
                    if msg.lower() == 'cpu':
                        self.csocket.send(cpu().encode())
                    print ("from client", msg)
            except:
                print("Client disconnected")
                self.csocket.close()
                break
        print ("Client at ", clientAddress, " disconnected...")


PORT = 5500
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
