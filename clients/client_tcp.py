from socket import *
import os

serverName = ''
serverPort = 15003
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))

def receive_data(sock):
    bytes = b""
    while True:
        data = sock.recv(1024)
        bytes += data
        if not data:
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
                confirmation = clientSocket.recv(1024)
                if confirmation.decode() == 'yes':
                    arquivo = clientSocket.recv(1024)
                    with open(arquivo.decode(), 'wb') as file:
                        while True:
                            partialData = clientSocket.recv(1024)
                            if not partialData:
                                break
                            file.write(partialData)
                        file.close()
                    data = clientSocket.recv(1024)
                    print(data.decode(), end='')
                else:
                    print(confirmation.decode(), end='')
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
