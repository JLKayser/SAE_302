import socket
PORT = 3500
ADDRESS = '127.0.0.1'
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((ADDRESS, PORT))
client.sendall(bytes("This is from Client",'UTF-8'))



while True:
    in_data =  client.recv(1024)
    print("From Server :" ,in_data.decode())
    out_data = input()
    client.sendall(bytes(out_data,'UTF-8'))
    if out_data=='bye':
        break
client.close()
