from socket import AF_INET, SOCK_STREAM , socket
from threading import Thread
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QLabel, QLineEdit, QPushButton, QMainWindow, QComboBox, \
    QDialog, QMessageBox , QTabWidget , QVBoxLayout
from PyQt5.QtCore import QCoreApplication

'''class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        #self.__aide = None

        widget = QWidget()
        self.resize(450,300)
        self.setCentralWidget(widget)
        grid = QGridLayout()
        widget.setLayout(grid)
        self.tabs = QTabWidget()
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tabs.resize(300,300)

        self.tabs.addTab(self.tab1,"Server")
        self.tabs.addTab(self.tab2,"Client")

        #self.tabs.setStyleSheet("QWidget { background-color: black }")
        self.tab1.layout = QGridLayout()
        self.pushCommand = QLineEdit("")
        self.connect = QPushButton('Connect')
        self.tab1.layout.addWidget(self.pushCommand)
        self.tab1.setLayout(self.tab1.layout)

        grid.addWidget(self.tabs, 0, 0)
        grid.addWidget(self.pushCommand, 3, 0)
        self.tab1.layout.addWidget(self.connect, 2 ,0)




        self.__convertir.clicked.connect(self.__ConversionCK)
        self.__help.clicked.connect(self.__Help)
        self.setWindowTitle("SAE-302")

    def __Help(self):
        msg = QMessageBox()
        msg.setWindowTitle("Aide")
        msg.resize(500, 500)
        msg.setIcon(QMessageBox.Information)
        msg.setText("Permet de convertir un nombre soit de Kelvin vers Celcuis, soit de Celcuis vers Kelvin.")
        msg.exec()




if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()'''

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
            msg = client_socket.recv(1024).decode()
            print(msg)
        except OSError as error:
            return error

def clean_exit():
    client_socket.send('exit()'.encode())
    client_socket.close()
    sys.exit(0)



while True:
    receive_thread = Thread(target=recv_msg)
    thread_send = Thread(target=msg_send)
    receive_thread.start()
    thread_send.start()
    msg_send()
