from socket import *
import os

serverName = ''
serverPort = 15004
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))

def receive_data(sock):
    bytes = b""
    while True:
        data = sock.recv(1024)
        bytes += data
        if not data:
            print('end of data sent by the server')
            break
    return bytes

def send_commands():
    print('$ ', end='')
    while True:
        command = input('')  # digita o comando
        if len(command) > 0:
            if command == 'quit':
                break
            elif command[:3] == 'scp':
                clientSocket.send(command.encode("UTF-8"))
                
                confirmation = clientSocket.recv(1024).decode()
                print(confirmation)
                clientSocket.send('received confirmation'.encode())

                file_name = clientSocket.recv(1024).decode()
                print(file_name)
                clientSocket.send('received file_name'.encode())

                print('$ ', end='')
            else:
                clientSocket.send(command.encode())

                # receive data, maybe create a function
                data = clientSocket.recv(1024)
                print(data.decode(), end='')
        else:
            # print waiting for command
            print('$ ', end='')

send_commands()
clientSocket.close()
