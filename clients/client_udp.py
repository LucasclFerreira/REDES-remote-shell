from socket import *
import os
import sys

serverName = ''
serverPort = 12000
clientSocket = socket(AF_INET, SOCK_DGRAM)

def send_commands():
    print(os.getcwd() + '$ ', end='')
    while True:
        command = input('')
        if len(command) > 0:
            if command == 'quit':
                break
            elif command[:3] == 'scp':
                clientSocket.sendto(command.encode("UTF-8"), (serverName, serverPort))
                confirmation, serverAddress = clientSocket.recvfrom(2048)
                if confirmation.decode() == 'yes':
                    arquivo, serverAddress = clientSocket.recvfrom(2048)
                    with open(arquivo.decode(), 'wb') as file:
                        while True:
                            partialData, serverAddress = clientSocket.recvfrom(2048)
                            if not partialData:
                                break
                            file.write(partialData)
                        file.close()
                    data, serverAddress = clientSocket.recvfrom(2048)
                    print(data.decode(), end='')
                else:
                    print(confirmation.decode(), end='')
            else:
                clientSocket.sendto(command.encode("UTF-8"), (serverName, serverPort))
                data, serverAddress = clientSocket.recvfrom(2048)
                print(data.decode(), end='')
        else:
            print(os.getcwd() + '$ ', end='')

send_commands()
clientSocket.close()