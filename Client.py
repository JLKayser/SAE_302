import threading
from socket import AF_INET, SOCK_STREAM , socket
from threading import Thread
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QLabel, QLineEdit, QPushButton, QMainWindow, QComboBox, QDialog, QMessageBox , QTabWidget , QVBoxLayout
from PyQt5.QtCore import QCoreApplication

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        #self.__aide = None

        widget = QWidget()
        self.resize(450,300)
        self.setCentralWidget(widget)
        grid = QGridLayout()
        widget.setLayout(grid)
        self.__tabs = QTabWidget()
        self.__tab1 = QWidget()
        self.__tab2 = QWidget()
        self.__tab3 = QWidget()
        self.__tabs.resize(300,300)

        self.__tabs.addTab(self.__tab1,"Server")
        self.__tabs.addTab(self.__tab2,"Client")
        self.__tabs.addTab(self.__tab3,"Server_msg")

        #self.tabs.setStyleSheet("QWidget { background-color: black }")
        self.__tab1.layout = QGridLayout()
        self.__tab2.layout = QGridLayout()
        self.__tab3.layout = QGridLayout()
        self.__pushCommand = QLineEdit("")
        self.__pushCommand.setPlaceholderText("Type an command...")
        self.__addressIP = QLineEdit("")
        self.__addressIP.setPlaceholderText("Type an IP address...")
        self.__port = QLineEdit("")
        self.__port.setPlaceholderText("Type an port...")
        self.__connect = QPushButton('Connect')
        self.__tab1.layout.addWidget(self.__pushCommand)
        self.__tab1.setLayout(self.__tab1.layout)
        #self.connect.setStyleSheet("border-radius:5px;background-color:black;color:white;height:20px;width:40px;")
        self.__label = QLabel('-> ')
        self.__tab3.layout.addWidget(self.__label)
        self.__tab3.setLayout(self.__tab3.layout)

        grid.addWidget(self.__tabs, 0, 0)
        grid.addWidget(self.__pushCommand, 3, 0)
        self.__tab1.layout.addWidget(self.__connect, 2, 0)
        self.__tab1.layout.addWidget(self.__addressIP, 1, 0)
        self.__tab1.layout.addWidget(self.__port, 1, 1)



        '''self.__help.clicked.connect(self.__Help)'''
        self.__connect.clicked.connect(self.__connection)
        self.setWindowTitle("SAE-302")

    '''def __Help(self):
        msg = QMessageBox()
        msg.setWindowTitle("Aide")
        msg.resize(500, 500)
        msg.setIcon(QMessageBox.Information)
        msg.setText("")
        msg.exec()'''


    def __connection(self):
        HOST = self.__addressIP.text()
        PORT = int(self.__port.text())
        self.socket = connect(HOST,PORT)
        receive_thread = Thread(target=recv_msg, args=[self.socket])
        thread_send = Thread(target=msg_send , args=[self.socket])
        receive_thread.start()
        thread_send.start()
        self.__addressIP.setText("")
        self.__addressIP.setPlaceholderText("Retype an IP address...")
        self.__port.setText("")
        self.__port.setPlaceholderText("Retype an port...")


    def message_recu(self):
        msg = self.socket.recv(1024).decode()
        self.__label.setText(self.__label.text() + '\n' + msg)




def connect(HOST:str,PORT:int):
    client_socket = socket(AF_INET, SOCK_STREAM)
    client_socket.connect((HOST,PORT))
    client_socket.sendall(bytes("This is from Client",'UTF-8'))
    Thread(target=recv_msg, args=[client_socket])
    return client_socket


def msg_send(connection):
    user = input('Enter your username : ')
    while True:
        try:
            msg = input(f'{user}-> ')
            if msg == 'reset':
                connection.close()
                client_socket = socket(AF_INET, SOCK_STREAM)
                #new_connection(connection.getpeername())
                #client_socket.connect((HOST, PORT))
                #client_socket.sendall(bytes("This is from Client", 'UTF-8'))
                #msg_send()
            if msg != 'disconnect':
                connection.send(msg.encode())
            else:
                disconnect(connection)
        except EOFError:
            disconnect(connection)


def new_connection():
    pass


def recv_msg(connection):
    while True:
        try:
            msg = connection.recv(1024).decode()
            print(msg)
        except:
            pass



def disconnect(connection):
    connection.send('disconnect'.encode())
    connection.close()
    sys.exit(0)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()
