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
    
    # if decodedCommand[:3] == 'scp':
    #     print('running command SCP...')
    #     path_head_tail = os.path.split(decodedCommand[4:])
    #     # procurar arquivo pra ver se ele existe
    #     if not path_head_tail[0]:
    #         # se for verdade o arquivo esta no diretorio atual
    #         print(f'teste path: {os.getcwd() + path_head_tail[1]}')
    #         exists = os.path.exists(os.getcwd() + path_head_tail[1])

    #     print(f'teste path: {path_head_tail[0] + path_head_tail[1]}')
    #     exists = os.path.exists(path_head_tail[0] + path_head_tail[1])
        
    #     if not exists:
    #         data = "File doesn't exist." + '\n' + os.getcwd() + '$ ' # pega o diretorio atual e concatena com '>'
    #         encodedData = data.encode()  # codigica os dados para enviar
    #         serverSocket.sendto(encodedData, clientAddress)  # envia os dados

    #     # pega nome do arquivo
    #     arquivo = path_head_tail[1]  # pegando head (nome do arquivo)
    #     serverSocket.sendto(arquivo.encode(), clientAddress)  # envia os dados

    #     # caso exista inicia transação
    #     # tam_pacote = 2048
    #     with open(arquivo, 'rb') as arq:
    #         while True:
    #             pacote = arq.read(2048)
    #             if not pacote:  # If the chunk is empty, we've reached the end of the file
    #                 break
    #             # data = os.getcwd() + '$ '  # pega o diretorio atual e concatena com '>'
    #             # encodedData = data.encode()  # codigica os dados para enviar
    #             serverSocket.sendto(pacote, clientAddress)  # envia os dados
    #         arq.close()
    #     data = os.getcwd() + '$ '
    #     encodedData = data.encode()  # codigica os dados para enviar
    #     serverSocket.sendto(encodedData, clientAddress)  # envia os dados

    if decodedCommand[:3] == 'scp':
        print('Executando comando SCP...')
        path_head_tail = os.path.split(decodedCommand[4:])
        exists = os.path.exists(decodedCommand[4:])

        if not exists:
            data = "Arquivo não existe." + '\n' + os.getcwd() + '$ '
            encodedData = data.encode()
            serverSocket.sendto(encodedData, clientAddress)
        else:
            arquivo = path_head_tail[1]
            serverSocket.sendto(arquivo.encode(), clientAddress)

            with open(decodedCommand[4:], 'rb') as file:
                while True:
                    chunk = file.read(2048)
                    serverSocket.sendto(chunk, clientAddress)
                    if not chunk:
                        break
                    
                file.close()

            data = os.getcwd() + '$ '
            encodedData = data.encode()
            serverSocket.sendto(encodedData, clientAddress)