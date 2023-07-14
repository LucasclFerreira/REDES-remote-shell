from socket import *
import os
import sys

serverName = gethostname()
serverAddress = gethostbyname(serverName)
serverPort = 12000
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind((serverAddress, serverPort))
print('server ready to receive')

while True:
    command, clientAddress = serverSocket.recvfrom(2048)
    print(f'connected to address {clientAddress}')
    decodedCommand = command.decode("UTF-8")
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
        data =  os.getcwd() + '\n'
        data += '$ '
        serverSocket.sendto(data.encode(), clientAddress)
    elif decodedCommand == 'ls':
        directory = os.listdir()
        data = ''
        for item in directory:
            data += item + '\n'
        data += os.getcwd() + '$ '
        serverSocket.sendto(data.encode(), clientAddress)
    elif decodedCommand[:3] == 'scp':
        if not os.path.exists(decodedCommand[4:]):
            data = 'no such file in the directory\n'
            data += '$ '
            serverSocket.sendto(data.encode(), clientAddress)
        else:
            confirmation = 'yes'
            serverSocket.sendto(confirmation.encode(), clientAddress)

            file = os.path.split(decodedCommand[4:])[1]
            serverSocket.sendto(file.encode(), clientAddress)

            with open(decodedCommand[4:], 'rb') as file:
                while True:
                    partialData = file.read(2048)
                    serverSocket.sendto(partialData, clientAddress)
                    if not partialData:
                        break
                file.close()
            data = '$ '
            serverSocket.sendto(data.encode(), clientAddress)
    else:
        data = f'{decodedCommand}: command not found\n'
        data += '$ '
        serverSocket.sendto(data.encode(), clientAddress)