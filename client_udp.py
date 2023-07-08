from socket import *
import os
import sys

serverName = ''
serverPort = 12000
clientSocket = socket(AF_INET, SOCK_DGRAM)

def send_commands():
    print(os.getcwd() + '$ ', end='')
    while True:
        command = input('')  # digita o comando

        if len(command) > 0:
            if command == 'quit':
                break
            elif command[:3] == 'scp':
                encodedCommand = command.encode("UTF-8")
                clientSocket.sendto(encodedCommand, (serverName, serverPort))
                confirmation, serverAddress = clientSocket.recvfrom(2048)
                if confirmation.decode() == 'yes':
                    arquivo, serverAddress = clientSocket.recvfrom(2048)
                    arquivo = arquivo.decode()

                    with open(arquivo, 'wb') as file:
                        while True:
                            chunk, serverAddress = clientSocket.recvfrom(2048)
                            if not chunk:
                                break
                            file.write(chunk)
                        file.close()

                    data, serverAddress = clientSocket.recvfrom(2048)
                    decodedData = data.decode()
                    print(decodedData, end='')
                else:
                    print(confirmation.decode(), end='')

            else:
                encodedCommand = command.encode("UTF-8")
                clientSocket.sendto(encodedCommand, (serverName, serverPort))
                data, serverAddress = clientSocket.recvfrom(2048)
                decodedData = data.decode()
                print(decodedData, end='')
        else:
            print(os.getcwd() + '$ ', end='')

send_commands()
clientSocket.close()