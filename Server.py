import socket
import os


def ipconfig():
    cmd = os.system('ipconfig')
    return cmd

ipconfig()

'''def server():
    # Recevoir le hostname soit ip de la machine
    host = "localhost"
    port = 5000  # Port

    server_socket = socket.socket()  # get instance
    server_socket.bind((host, port))

    # nombre de client qui peuvent se connecter en meme temp
    server_socket.listen(2)

    conn, address = server_socket.accept()  # accepte les nouvelles connexions
    print("Connection from: " + str(address))
    while True:
        # recois les données et n accepte pas au dessus de 1024 bytes
        data = conn.recv(1024).decode()
        if not data:
            # Si les données ne sont pas recus break
            server_socket.close()
            server()
            break
        print("from connected user: " + str(data))
        data = input(' -> ')
        conn.send(data.encode())  # Envoyer les données au client

    conn.close()  # Fermer la connexion


if __name__ == '__main__':
    server()'''