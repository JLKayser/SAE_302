from socket import AF_INET, SOCK_STREAM , socket
from threading import Thread
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QLabel, QLineEdit, QPushButton, QMainWindow, QComboBox, QDialog, QMessageBox, QTabWidget, QVBoxLayout, QPlainTextEdit, QTextEdit
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtCore import QObject, QThread, pyqtSignal
import time
from PyQt5.QtCore import Qt


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        widget = QWidget()
        self.resize(450,300)
        self.setCentralWidget(widget)
        grid = QGridLayout()
        widget.setLayout(grid)
        self.__tabs = QTabWidget()
        self.__tab1 = QWidget()
        self.__tab3 = QWidget()
        self.__tabs.resize(300,300)

        self.__tabs.addTab(self.__tab1,"Server")
        self.__tabs.addTab(self.__tab3,"Server-CMD")

        #self.tabs.setStyleSheet("QWidget { background-color: black }")
        self.__tab1.layout = QGridLayout()
        self.__tab3.layout = QGridLayout()
        self.__pushCommand = QLineEdit("")
        self.__envoie = QPushButton("Send")
        self.__pushCommand.setPlaceholderText("Type a command...")
        self.__addressIP = QLineEdit("")
        self.__addressIP.setPlaceholderText("Type an IP address...")
        self.__okay = QLabel("Waiting for a connection")
        self.__port = QLineEdit("")
        self.__port.setPlaceholderText("Type an port...")
        self.__connect = QPushButton('Connect')
        self.__tab1.layout.addWidget(self.__pushCommand)
        self.__tab1.setLayout(self.__tab1.layout)
        #self.connect.setStyleSheet("border-radius:5px;background-color:black;color:white;height:20px;width:40px;")
        self.__text = QLabel("Welcome To my Shell")
        #self.__text.setReadOnly(True)
        self.__tab3.layout.addWidget(self.__text)
        self.__text.move(10, 10)
        self.__text.resize(400, 200)
        self.__tab3.setLayout(self.__tab3.layout)
        #self.__text.setPlaceholderText('Bienvenue sur mon invite de commande !')


        grid.addWidget(self.__tabs, 0, 0)
        grid.addWidget(self.__pushCommand, 3, 0)
        grid.addWidget(self.__envoie, 3, 1)
        self.__tab1.layout.addWidget(self.__connect, 2, 0)
        self.__tab1.layout.addWidget(self.__addressIP, 1, 0)
        self.__tab1.layout.addWidget(self.__port, 1, 1)
        self.__tab1.layout.addWidget(self.__okay, 2, 1)


        self.__connect.clicked.connect(self.__connection)
        self.__addressIP.returnPressed.connect(self.__connection)
        self.__port.returnPressed.connect(self.__connection)
        self.__envoie.clicked.connect(self.__message_send)
        self.__pushCommand.returnPressed.connect(self.__message_send)
        self.setWindowTitle("SAE-302")



    def __InValid(self):
        msg = QMessageBox()
        msg.setWindowTitle("Not valid")
        msg.resize(500, 500)
        msg.setIcon(QMessageBox.Critical)
        msg.setText("Please enter a valid IP address or port !")
        msg.exec()

    def __InValidCommand(self):
        msg = QMessageBox()
        msg.setWindowTitle("Not valid")
        msg.resize(500, 500)
        msg.setIcon(QMessageBox.Critical)
        msg.setText("Please enter a valid command !")
        msg.exec()


    def __connection(self):
        try:
            HOST = self.__addressIP.text()
            PORT = int(self.__port.text())
            self.socket = connect(HOST,PORT)
            thread_recu = Thread(target=self.__message_recu)
            thread_envoie = Thread(target=self.__message_send)
            thread_recu.start()
            thread_envoie.start()
            self.__addressIP.setText("")
            self.__addressIP.setPlaceholderText("Retype an IP address...")
            self.__port.setText("")
            self.__port.setPlaceholderText("Retype an port...")
            self.__okay.setText("Connection is successful !")
        except:
            self.__InValid()


    def __message_recu(self):
        while True:
            try:
                msg = self.socket.recv(1024).decode()
                self.__text.setText('-> ' + msg)
                self.__pushCommand.setText("")
                self.__pushCommand.setPlaceholderText("Retype a command...")
            except:
                self.__InValidCommand()

    def __message_send(self):
        try:
            msg = self.__pushCommand.text()
            if msg.lower() == 'reset':
                self.socket.close()
                #client_socket = socket(AF_INET, SOCK_STREAM)
                # new_connection(connection.getpeername())
                # client_socket.connect((HOST, PORT))
                # client_socket.sendall(bytes("This is from Client", 'UTF-8'))
                # msg_send()
            if msg.lower() != 'disconnect':
                self.socket.send(msg.encode())
            else:
                self.disconnect()
        except EOFError:
            pass

    def disconnect(self):
        self.socket.send('disconnect'.encode())
        self.socket.close()
        sys.exit(0)




def connect(HOST:str,PORT:int):
    client_socket = socket(AF_INET, SOCK_STREAM)
    client_socket.connect((HOST,PORT))
    client_socket.sendall(bytes("This is from Client",'UTF-8'))
    return client_socket


'''def msg_send(connection):
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
            disconnect(connection)'''''


def new_connection():
    pass


'''def recv_msg(connection):
    while True:
        try:
            msg = connection.recv(1024).decode()
            print(msg)
        except:
            pass'''




if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()
