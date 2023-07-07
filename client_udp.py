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
        
        # if command[:3] == 'scp':
        #     encodedCommand = command.encode("UTF-8")  # codifica comando
        #     clientSocket.sendto(encodedCommand, (serverName, serverPort))  # envia comando para o servidor
        #     arquivo, serverAddress = clientSocket.recvfrom(2048)
            
        #     with open(arquivo, 'wb') as arq:
        #         while True:
        #             # recebe os dados do pacote
        #             pacote, serverAddress = clientSocket.recvfrom(2048)
        #             arq.write(pacote)
        #         arq.close()
                
        #     data, serverAddress = clientSocket.recvfrom(2048)
        #     decodedData = data.decode()
        #     print(decodedData, end='')
                    

        # encodedCommand = command.encode("UTF-8")  # codifica comando
        # clientSocket.sendto(encodedCommand, (serverName, serverPort))  # envia comando para o servidor
        # data, serverAddress = clientSocket.recvfrom(2048)
        # decodedData = data.decode()
        # print(decodedData, end='')

        if command[:3] == 'scp':
            encodedCommand = command.encode("UTF-8")
            clientSocket.sendto(encodedCommand, (serverName, serverPort))
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
            encodedCommand = command.encode("UTF-8")
            clientSocket.sendto(encodedCommand, (serverName, serverPort))
            data, serverAddress = clientSocket.recvfrom(2048)
            decodedData = data.decode()
            print(decodedData, end='')

send_commands()
clientSocket.close()