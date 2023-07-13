from socket import *
import os

serverPort = 15004
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverPort))
serverSocket.listen()
print('server ready to receive')

def scp(conn, file_path):
    file_name = os.path.split(file_path)[1]
    file_name = file_name.encode()
    # print(file_name)
    if os.path.exists(file_path):
        conn.send('EXISTS'.encode())
        confirmation = conn.recv(1024).decode()
        print(confirmation)
        conn.send(file_name)
        confirmation = conn.recv(1024).decode()
        print(confirmation)


connectionSocket, clientAddress = serverSocket.accept()
print(f'connected to address {clientAddress}')
try:
    while True:
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
            scp(connectionSocket, decodedCommand[4:])
        else:
            data = f'{decodedCommand}: command not found\n'
            data += '$ '
            connectionSocket.send(data.encode())
except BrokenPipeError:
    print('BrokenPipeError occurred...')
    connectionSocket.close()
finally:
    connectionSocket.close()
