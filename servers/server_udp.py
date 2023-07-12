from socket import *
import os
import sys

serverPort = 12000
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(('', serverPort))
print('server ready to receive')

while True:
    command, clientAddress = serverSocket.recvfrom(2048)
    print(f'connected to address {clientAddress}')
    decodedCommand = command.decode("UTF-8")
    if decodedCommand[:2] == 'cd':
        try:
            # print('running command CD...')
            os.chdir(decodedCommand[3:])

            # send waiting for command
            data = os.getcwd() + '$ '
            serverSocket.sendto(data.encode(), clientAddress)
        except:
            data = f'bash: cd: {decodedCommand[3:]}: Arquivo ou diretório inexistente\n'

            # send waiting for command
            data += os.getcwd() + '$ '
            serverSocket.sendto(data.encode(), clientAddress)
    elif decodedCommand == 'pwd':
        # print('running command PWD...')
        data =  os.getcwd() + '\n'

        # send waiting for command
        data += os.getcwd() + '$ '
        serverSocket.sendto(data.encode(), clientAddress)
    elif decodedCommand == 'ls':
        # print('running command LS...')
        directory = os.listdir()  # pega o diretorio atual e concatena com '>'
        data = ''
        for item in directory:
            data += item + '\n'
        
        # send waiting for command
        data += os.getcwd() + '$ '
        serverSocket.sendto(data.encode(), clientAddress)  # envia os dados
    elif decodedCommand[:3] == 'scp':
        # print('Executando comando SCP...')
        if not os.path.exists(decodedCommand[4:]):
            data = 'no such file in the directory\n'

            # send waiting for command
            data += os.getcwd() + '$ '  # maybe os.getcwd ad default
            serverSocket.sendto(data.encode(), clientAddress)
        else:
            confirmation = 'yes'  # and you can pass a value if you want to
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

            # send waiting command
            data = os.getcwd() + '$ '
            serverSocket.sendto(data.encode(), clientAddress)
    else:
        data = f'{decodedCommand}: command not found\n'

        # send waiting commands
        data += os.getcwd() + '$ '
        serverSocket.sendto(data.encode(), clientAddress)