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
            print('running command CD...')
            os.chdir(decodedCommand[3:])  # pega o que foi passado depois do cd e executa
            data = os.getcwd() + '$ '  # pega o diretorio atual e concatena com '>'
            encodedData = data.encode()  # codigica os dados para enviar
            serverSocket.sendto(encodedData, clientAddress)  # envia os dados
        except:
            data = f'bash: cd: {decodedCommand[3:]}: Arquivo ou diretório inexistente\n'
            data += os.getcwd() + '$ '  # pega o diretorio atual e concatena com '>'
            encodedData = data.encode()  # codigica os dados para enviar
            serverSocket.sendto(encodedData, clientAddress)  # envia os dados

    if decodedCommand == 'pwd':
        print('running command PWD...')
        data = os.getcwd() + '\n' + os.getcwd() + '$ ' # pega o diretorio atual e concatena com '>'
        encodedData = data.encode()  # codigica os dados para enviar
        serverSocket.sendto(encodedData, clientAddress)  # envia os dados

    if decodedCommand == 'ls':
        print('running command LS...')
        directory = os.listdir()  # pega o diretorio atual e concatena com '>'
        data = ''
        for item in directory:
            data += item + '\n'
        data = data + os.getcwd() + '$ '
        encodedData = data.encode()  # codigica os dados para enviar
        serverSocket.sendto(encodedData, clientAddress)  # envia os dados
    
    if decodedCommand[:3] == 'scp':
        # procurar arquivo pra ver se ele existe

        # pega nome do arquivo
        arquivo = ""

        # caso exista inicia transação
        tam_pacote = 2048
        with open(arquivo, 'rb') as arq:
            while True:
                pacote = arq.read(tam_pacote)
                if not pacote:  # If the chunk is empty, we've reached the end of the file
                    break
                # data = os.getcwd() + '$ '  # pega o diretorio atual e concatena com '>'
                # encodedData = data.encode()  # codigica os dados para enviar
                serverSocket.sendto(pacote, clientAddress)  # envia os dados
                