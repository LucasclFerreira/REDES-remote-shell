from socket import *
import os
import time
import sys

serverName = gethostname()
serverAddress = gethostbyname(serverName)
print(f'hostname: {serverName}; hostaddr: {serverAddress}')
serverPort = 15005
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind((serverName, serverPort))

print('server ready to receive')

try:
    while True:
        print('topo server')
        command, clientAddress = serverSocket.recvfrom(1024)
        decodedCommand = command.decode()

        if decodedCommand[:2] == 'cd':
            try:
                os.chdir(decodedCommand[3:])
                data = '$ '
                serverSocket.sendto(data.encode(), clientAddress)
            except:
                data = f'bash: cd: {decodedCommand[3:]}: Arquivo ou diretório inexistente\n'
                data += '$ '
                serverSocket.sendto(data.encode(), clientAddress)

        elif decodedCommand == 'pwd':
            data = os.getcwd() + '\n'
            data += '$ '
            serverSocket.sendto(data.encode(), clientAddress)

        elif decodedCommand == 'ls':
            directory = os.listdir()
            data = ''
            for item in directory:
                data += item + '\n'
            data += '$ '
            serverSocket.sendto(data.encode(), clientAddress)

        elif decodedCommand[:3] == 'scp':
            if not os.path.exists(decodedCommand[4:]):
                file_size = 0
                file_size = str(file_size)
                serverSocket.sendto(file_size.encode(), clientAddress)
            else:
                file_size = str(os.path.getsize(decodedCommand[4:]))
                serverSocket.sendto(file_size.encode(), clientAddress)
                ack, _ = serverSocket.recvfrom(1024)
                file = os.path.split(decodedCommand[4:])[1]
                serverSocket.sendto(file.encode(), clientAddress)
                ack, _ = serverSocket.recvfrom(1024)

                file_size = int(file_size)  # transformando em inteiro novamente
                with open(decodedCommand[4:], 'rb') as file:
                    while file_size > 0:
                        if file_size > 1024:
                            partialData = file.read(1024)
                            serverSocket.sendto(partialData, clientAddress)
                            file_size -= 1024
                            ack, _ = serverSocket.recvfrom(1024)  # esperando o client enviar um ack para proceder
                        else:
                            partialData = file.read(1024)
                            serverSocket.sendto(partialData, clientAddress)
                            file_size -= file_size
                            ack, _ = serverSocket.recvfrom(1024)  # esperando o client enviar um ack para proceder

                data = '$ '
                serverSocket.sendto(data.encode(), clientAddress)

        else:
            data = f'{decodedCommand}: command not found\n'
            data += '$ '
            serverSocket.sendto(data.encode(), clientAddress)

except KeyboardInterrupt:
    print('Server shutting down...')
finally:
    serverSocket.close()
