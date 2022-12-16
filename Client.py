from socket import AF_INET, SOCK_STREAM , socket
from threading import Thread
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QLabel, QLineEdit, QPushButton, QMainWindow, QComboBox, QDialog, QMessageBox, QTabWidget, QVBoxLayout, QPlainTextEdit, QTextEdit, QTableWidget,QTableWidgetItem, QHeaderView, QAbstractItemView
import csv
from PyQt5 import QtCore

class TabCMD(QMainWindow):
    def __init__(self, socket):
        super().__init__()


        self.__tabs = QTabWidget()
        self.__tab = QWidget()
        self.__connected = True
        self.__tabs.resize(300,300)
        self.__tab.layout = QGridLayout()
        self.setCentralWidget(self.__tab)

        self.__text = QLabel("Welcome To my Shell", self)
        self.__tab.layout = QGridLayout()
        self.__pushCommand = QLineEdit("")
        self.socket = socket
        self.__pushCommand.setPlaceholderText("Type a command...")
        self.__envoie = QPushButton("Send")
        self.__tab.layout.addWidget(self.__pushCommand)
        self.__tab.layout.addWidget(self.__envoie)

        self.__recv = QTextEdit(self)
        self.__recv.setReadOnly(True)
        self.__tab.layout.addWidget(self.__recv)
        self.__tab.layout.addWidget(self.__text)
        self.__text.move(10, 10)
        self.__text.resize(400, 200)
        self.__tab.setLayout(self.__tab.layout)

        self.__tab.layout.addWidget(self.__text, 0, 0)
        self.__tab.layout.addWidget(self.__recv, 1, 0)
        self.__tab.layout.addWidget(self.__pushCommand, 3, 0)
        self.__tab.layout.addWidget(self.__envoie, 3, 1)

        self.__envoie.clicked.connect(self.SEND)
        self.__pushCommand.returnPressed.connect(self.SEND)
        thread_recu = Thread(target=self.RECU)
        thread_recu.start()

    def RECU(self):
        while self.__connected:
            try:
                msg = self.socket.recv(1024).decode()
                if len(msg) > 0:
                    if msg.lower() == 'reset':
                        self.socket.close()
                        self.__recv.append('RESET')
                        self.__pushCommand.setText("")
                        self.__pushCommand.setPlaceholderText("Retype a command...")
                        self.close()
                        self.deleteLater()
                    elif msg.lower() == 'kill':
                        self.socket.close()
                        self.__recv.append('KILL')
                        self.__pushCommand.setText("")
                        self.__pushCommand.setPlaceholderText("Retype a command...")
                        self.close()
                        self.deleteLater()
                    elif msg.lower() == 'disconnect':
                        self.socket.close()
                        self.__recv.append('DISCONNECTED')
                        self.__pushCommand.setText("")
                        self.__pushCommand.setPlaceholderText("Retype a command...")
                        self.close()
                        self.deleteLater()
                    self.__recv.append('-> ' + self.__pushCommand.text() + '\n' + msg + '\n')
                    self.__pushCommand.setText("")
                    self.__pushCommand.setPlaceholderText("Retype a command...")
            except:
                pass

    def SEND(self):
        try:
            msg = self.__pushCommand.text()
            self.socket.send(msg.encode())
            if msg.lower() == 'clear':
                self.__recv.setText("")
                self.__pushCommand.setText("")
                self.__pushCommand.setPlaceholderText("Retype a command...")
        except:
            pass

    def close(self):
        self.__connected = False


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        widget = QWidget()
        self.resize(450,300)
        self.setCentralWidget(widget)
        grid = QGridLayout()
        widget.setLayout(grid)
        self.__sockets = []
        self.__tabs = QTabWidget()
        self.__tab1 = QWidget()
        self.__tab2 = QWidget()
        self.__tabs.resize(300,300)

        self.__tabs.addTab(self.__tab1,"Connexion")
        self.__tabs.addTab(self.__tab2,"List_Server")

        self.__tab1.layout = QGridLayout()
        self.__tab2.layout = QGridLayout()
        self.__csv = QLabel("")
        self.__addressIP = QLineEdit("")
        self.__addressIP.setPlaceholderText("Type an IP address...")
        self.__okay = QLabel("Waiting for a connection")
        self.__port = QLineEdit("")
        self.__port.setPlaceholderText("Type an port...")
        self.__connect = QPushButton('Connect')
        self.__tab1.setLayout(self.__tab1.layout)
        self.__tableau = self.ma_table()
        self.__tab2.layout.addWidget(self.__tableau)
        self.__tab2.setLayout(self.__tab2.layout)


        grid.addWidget(self.__tabs, 0, 0, 1,2)
        self.__tab1.layout.addWidget(self.__connect, 2, 0)
        self.__tab1.layout.addWidget(self.__addressIP, 1, 0)
        self.__tab1.layout.addWidget(self.__port, 1, 1)
        self.__tab1.layout.addWidget(self.__okay, 2, 1)



        self.__connect.clicked.connect(self.__connection)
        self.__addressIP.returnPressed.connect(self.__connection)
        self.__port.returnPressed.connect(self.__connection)
        self.setWindowTitle("SAE-302")



    def __InValid(self):
        msg = QMessageBox()
        msg.setWindowTitle("Not valid")
        msg.resize(500, 500)
        msg.setIcon(QMessageBox.Critical)
        msg.setText("Please enter a valid IP address or port !")
        msg.exec()


    def __connection(self):
        try:
            HOST = self.__addressIP.text()
            PORT = int(self.__port.text())
            connection = connect(HOST,PORT)
            self.__addressIP.setText("")
            self.__addressIP.setPlaceholderText("Retype an IP address...")
            self.__port.setText("")
            self.__port.setPlaceholderText("Retype an port...")
            self.__okay.setText("Connection is successful !")
            x = TabCMD(connection)
            self.__sockets.append(x)
            self.__tabs.addTab(x,f'{HOST}:{PORT}')

        except:
            self.__InValid()


    def __connectionTable(self):
        try:
            HOST = self.__addressIP.text()
            PORT = int(self.__port.text())
            connection = connect(HOST,PORT)
            self.__okay.setText("Connection is successful !")
            x = TabCMD(connection)
            self.__sockets.append(x)
            self.__tabs.addTab(x,f'{HOST}:{PORT}')
        except:
            self.__InValid()


    def ma_table(self):
        table = QTableWidget()
        table.setColumnCount(2)
        table.setHorizontalHeaderLabels(['IP','PORT'])
        table.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
        table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        with open('info-csv.csv', 'r') as file:
            lines = file.readlines()
            for line in lines:
                elements = line.replace('\n', '').split(',')
                print(elements)
                if len(elements) == 2:
                    ip = elements[0]
                    port = elements[1]
                    if port.isdigit():
                        port = int(port)
                        row = table.rowCount()
                        table.setRowCount(table.rowCount() + 1)
                        table.setItem(row, 0, QTableWidgetItem(ip))
                        table.setItem(row, 1, QTableWidgetItem(str(port)))
                    else:
                        pass
                else:
                    pass
        return table



    def closeEvent(self, event):
        for i in self.__sockets:
            i.close()




def connect(HOST:str,PORT:int):
    client_socket = socket(AF_INET, SOCK_STREAM)
    client_socket.connect((HOST,PORT))
    client_socket.setblocking(False)
    return client_socket



if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()
