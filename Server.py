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
        if cmd[0:4].lower() == 'dos:':
            x = cmd.split(":",1)[1]
            out = subprocess.getoutput(x)
            return out
        return 'UNKNOWN COMMAND'
    except:
        pass


class ClientThread(threading.Thread):
    def __init__(self,clientAddress,clientsocket):
        threading.Thread.__init__(self)
        self.csocket = clientsocket
        print ("New connection added: ", clientAddress)


    def run(self):
        global reset
        global arret
        print ("Connection from : ", clientAddress)
        #self.csocket.send(bytes("Hi, This is from Server..",'utf-8'))
        while True:
            try:
                data = self.csocket.recv(1024)
                msg = data.decode()
                if len(msg) > 0:
                    if msg.lower() == 'disconnect':
                        self.csocket.send('disconnect'.encode())
                        self.csocket.close()
                        break
                    elif msg.lower() == 'kill':
                        self.csocket.send("kill".encode())
                        arret = True
                        server.close()
                        break
                    elif msg.lower() == 'reset':
                        self.csocket.send("reset".encode())
                        server.close()
                        arret = True
                        reset = True
                    else:
                        self.csocket.send(cmd(msg).encode())
            except:
                pass
        print ("Client at ", clientAddress, " disconnected...")


PORT = int(input('Please enter a port: '))
ADDRESS = '0.0.0.0'
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((ADDRESS, PORT))
server.setblocking(False)
clients = []
arret = False
reset = False

msg = ''
print("Server started")
print("Waiting for client request..")


def reset_func():
    global server
    print(server)
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((ADDRESS, PORT))
    print('resetting...')
    print(server)

while True:
    while not arret:
        try:
            server.listen(1)
            clientsock, clientAddress = server.accept()
            clients.append(clientsock)
            newthread = ClientThread(clientAddress, clientsock)
            newthread.start()
        except:
            pass
    if reset:
        for client in clients:
            client.close()
        reset_func()
        reset = False
        arret = False
    else:
        break
