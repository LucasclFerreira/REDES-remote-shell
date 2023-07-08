from socket import *
import os
import sys

serverPort = 12000
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(('', serverPort))
print('server pronto para receber')

while True:
    command, clientAddress = serverSocket.recvfrom(2048)  # recebo o comando enviado pelo cliente
    decodedCommand = command.decode("UTF-8")  # decodifica o comando
    
    if decodedCommand[:2] == 'cd':  # se o comando for cd...
        try:
            # print('running command CD...')
            os.chdir(decodedCommand[3:])  # pega o que foi passado depois do cd e executa
            data = os.getcwd() + '$ '  # pega o diretorio atual e concatena com '>'
            encodedData = data.encode()  # codigica os dados para enviar
            serverSocket.sendto(encodedData, clientAddress)  # envia os dados
        except:
            data = f'bash: cd: {decodedCommand[3:]}: Arquivo ou diretório inexistente\n'
            data += os.getcwd() + '$ '  # pega o diretorio atual e concatena com '>'
            encodedData = data.encode()  # codigica os dados para enviar
            serverSocket.sendto(encodedData, clientAddress)  # envia os dados
    elif decodedCommand == 'pwd':
        # print('running command PWD...')
        data = os.getcwd() + '\n' + os.getcwd() + '$ ' # pega o diretorio atual e concatena com '>'
        encodedData = data.encode()  # codigica os dados para enviar
        serverSocket.sendto(encodedData, clientAddress)  # envia os dados
    elif decodedCommand == 'ls':
        # print('running command LS...')
        directory = os.listdir()  # pega o diretorio atual e concatena com '>'
        data = ''
        for item in directory:
            data += item + '\n'
        data = data + os.getcwd() + '$ '
        encodedData = data.encode()  # codigica os dados para enviar
        serverSocket.sendto(encodedData, clientAddress)  # envia os dados
    elif decodedCommand[:3] == 'scp':
        # print('Executando comando SCP...')
        path_head_tail = os.path.split(decodedCommand[4:])
        exists = os.path.exists(decodedCommand[4:])

        if not exists:
            data = "no such file in the directory" + '\n' + os.getcwd() + '$ '
            encodedData = data.encode()
            serverSocket.sendto(encodedData, clientAddress)
        else:
            confirmation = 'yes'
            serverSocket.sendto(confirmation.encode(), clientAddress)
            file = path_head_tail[1]
            serverSocket.sendto(file.encode(), clientAddress)

            with open(decodedCommand[4:], 'rb') as file:
                while True:
                    packet = file.read(2048)
                    serverSocket.sendto(packet, clientAddress)
                    if not packet:
                        break
                    
                file.close()

            data = os.getcwd() + '$ '
            encodedData = data.encode()
            serverSocket.sendto(encodedData, clientAddress)
    else:
        data = f'{decodedCommand.split(" ")[0]}: command not found\n' + os.getcwd() + '$ '
        encodedData = data.encode()
        serverSocket.sendto(encodedData, clientAddress)