import socket


def client():
    host = "localhost"
    port = 5000  # Port du socket server

    client_socket = socket.socket()
    client_socket.connect((host, port))  # connexion au server

    user = input('Entrez votre nom d\'utilisateur : ')
    message = input(f"{user} -> ")

    while message != 'arret':
        client_socket.send(message.encode())  # envoie le message
        data = client_socket.recv(1024).decode()  # recois les reponses
        if data == 'bye':
            client_socket.close()
            client()
            break

        print('Received from server: ' + data)

        message = input(f"{user}> ")

    client_socket.close()  # Fermer la connexion


if __name__ == '__main__':
    client()