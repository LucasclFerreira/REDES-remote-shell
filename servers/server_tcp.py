from socket import *
import os
import time

serverPort = 15005
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverPort))
serverSocket.listen()
print('server ready to receive')

connectionSocket, clientAddress = serverSocket.accept()
print(f'connected to address {clientAddress}')
try:
    while True:
        print('topo server')
        command = connectionSocket.recv(1024)
        decodedCommand = command.decode()
        if decodedCommand[:2] == 'cd':
            try:
                os.chdir(decodedCommand[3:])
                data = '$ '
                connectionSocket.send(data.encode())
            except:
                data = f'bash: cd: {decodedCommand[3:]}: Arquivo ou diretório inexistente\n'
                data += '$ '
                connectionSocket.send(data.encode())
        elif decodedCommand == 'pwd':
            data =  os.getcwd() + '\n'
            data += '$ '
            connectionSocket.send(data.encode())
        elif decodedCommand == 'ls':
            directory = os.listdir()
            data = ''
            for item in directory:
                data += item + '\n'
            data += '$ '
            connectionSocket.send(data.encode())
        elif decodedCommand[:3] == 'scp':
            if not os.path.exists(decodedCommand[4:]):
                data = 'no such file in the directory\n'
                data += '$ '
                connectionSocket.send(data.encode())
            else:
                print('preparing conf...')
                time.sleep(1)
                file_size = str(os.path.getsize(decodedCommand[4:]))
                connectionSocket.send(file_size.encode())
                ack = connectionSocket.recv(1024) 

                # print('conf sent')
                # time.sleep(1)
                file = os.path.split(decodedCommand[4:])[1]
                connectionSocket.send(file.encode())
                ack = connectionSocket.recv(1024)

                file_size = int(file_size)  # transformando em inteiro novamente
                with open(decodedCommand[4:], 'rb') as file:
                    while file_size > 0:
                        if file_size > 1024:
                            partialData = file.read(1024)
                            connectionSocket.sendall(partialData)
                            file_size -= 1024
                            ack = connectionSocket.recv(1024)  # esperando o client enviar um ack para proceder
                        else:
                            partialData = file.read(1024)
                            connectionSocket.sendall(partialData)
                            file_size -= file_size
                            ack = connectionSocket.recv(1024)  # esperando o client enviar um ack para proceder
                data = '$ '
                connectionSocket.send(data.encode())
        else:
            data = f'{decodedCommand}: command not found\n'
            data += '$ '
            connectionSocket.send(data.encode())
except BrokenPipeError:
    print('BrokenPipeError occurred...')
    connectionSocket.close()
finally:
    connectionSocket.close()

# scp ../../../teste/teste-video.mp4