from socket import *
import os
import sys

serverName = ''
serverPort = 12000
clientSocket = socket(AF_INET, SOCK_DGRAM)

def send_commands():
    while True:
        command = input('')  # digita o comando

        if command == 'quit':
            break
        
        if command[:3] == 'scp':
            encodedCommand = command.encode("UTF-8")  # codifica comando
            clientSocket.sendto(encodedCommand, (serverName, serverPort))  # envia comando para o servidor
            arquivo, serverAddress = clientSocket.recvfrom(2048)

            with open(arquivo, 'wb') as arq:
                while True:
                    pacote, serverAddress = clientSocket.recvfrom(2048)
                    
                    if not pacote:
                        break

                    arq.write(pacote)
            data, serverAddress = clientSocket.recvfrom(2048)
            decodedData = data.decode()
            print(decodedData, end='')
                    

        encodedCommand = command.encode("UTF-8")  # codifica comando
        clientSocket.sendto(encodedCommand, (serverName, serverPort))  # envia comando para o servidor
        data, serverAddress = clientSocket.recvfrom(2048)
        decodedData = data.decode()
        print(decodedData, end='')

send_commands()
clientSocket.close()