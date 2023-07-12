from socket import *
import os

serverPort = 12000
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('192.168.1.7', serverPort))
serverSocket.listen()
print('Server ready to receive')

while True:
    connectionSocket, clientAddress = serverSocket.accept()
    print(f'Connected to {clientAddress}')
    command = connectionSocket.recv(4096)  # receive the command from the client
    decodedCommand = command.decode("UTF-8")  # decode the command
    
    if decodedCommand[:2] == 'cd':  # if the command is cd...
        try:
            os.chdir(decodedCommand[3:])  # get the directory specified after cd and execute
            data = os.getcwd() + '$ '  # get the current directory and append '>'
            encodedData = data.encode()  # encode the data to send
            connectionSocket.send(encodedData)  # send the data
        except Exception as e:
            data = f'bash: cd: {decodedCommand[3:]}: no such file or directory\n'
            data += os.getcwd() + '$ '  # get the current directory and append '>'
            encodedData = data.encode()  # encode the data to send
            connectionSocket.send(encodedData)  # send the data
    elif decodedCommand == 'pwd':
        data = os.getcwd() + '\n' + os.getcwd() + '$ '  # get the current directory and append '>'
        encodedData = data.encode()  # encode the data to send
        connectionSocket.send(encodedData)  # send the data
    elif decodedCommand == 'ls':
        directory = os.listdir()  # get the current directory
        data = ''
        for item in directory:
            data += item + '\n'
        data = data + os.getcwd() + '$ '
        encodedData = data.encode()  # encode the data to send
        connectionSocket.send(encodedData)  # send the data
    elif decodedCommand[:3] == 'scp':
        path_head_tail = os.path.split(decodedCommand[4:])
        exists = os.path.exists(decodedCommand[4:])

        if not exists:
            data = "no such file in the directory" + '\n' + os.getcwd() + '$ '
            encodedData = data.encode()
            connectionSocket.send(encodedData)
        else:
            confirmation = 'yes'
            connectionSocket.send(confirmation.encode())
            file = path_head_tail[1]
            connectionSocket.send(file.encode())

            with open(decodedCommand[4:], 'rb') as file:
                while True:
                    packet = file.read(4096)
                    connectionSocket.send(packet)
                    if not packet:
                        break
                    
                file.close()

            data = os.getcwd() + '$ '
            encodedData = data.encode()
            connectionSocket.send(encodedData)
    else:
        data = f'{decodedCommand}: command not found\n' + os.getcwd() + '$ '
        encodedData = data.encode()
        connectionSocket.send(encodedData)

    connectionSocket.close()
