from socket import *
import sys
import time

serverName = sys.argv[1]
serverPort = 15005
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))

def send_commands():
    print('$ ', end='')
    while True:
        # print(' topo client: ', end='')
        command = input('')  # digita o comando
        if len(command) > 0:
            if command == 'quit':
                break
            elif command[:3] == 'scp':
                clientSocket.send(command.encode("UTF-8"))
                file_size = int(clientSocket.recv(1024).decode())
                if file_size != 0:
                    clientSocket.send(b"ack")

                    arquivo = clientSocket.recv(1024)
                    clientSocket.send(b"ack")

                    with open(arquivo.decode(), 'wb') as file:
                        while file_size > 0:
                            if file_size > 1024:
                                partialData = clientSocket.recv(1024)
                                file.write(partialData)
                                file_size -= 1024
                                clientSocket.send(b"ack")
                            else:
                                partialData = clientSocket.recv(1024)
                                file.write(partialData)
                                file_size -= file_size
                                clientSocket.send(b"ack")
                    data = clientSocket.recv(1024)
                    print(data.decode(), end='')
                else:
                    print('no such file in the directory\n$ ', end='')
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