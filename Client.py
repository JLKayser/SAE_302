from socket import AF_INET, SOCK_STREAM , socket
from threading import Thread
import sys


HOST = '127.0.0.1'
PORT = 5500
client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect((HOST,PORT))
client_socket.sendall(bytes("This is from Client",'UTF-8'))

def msg_send():
    while True:
        try:
            msg = input('-> ')
            if msg != 'kill':
                client_socket.send(msg.encode('utf8'))
            else:
                clean_exit()
        except EOFError:
            clean_exit()


def recv_msg():
    while True:
        try:
            msg = client_socket.recv(1024).decode("utf8")
            print(msg)
        except OSError as error:
            return error

def clean_exit():
    client_socket.send('exit()'.encode('utf8'))
    client_socket.close()
    sys.exit(0)



while True:
    receive_thread = Thread(target=recv_msg)
    receive_thread.start()
    msg_send()
