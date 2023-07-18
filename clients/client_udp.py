from socket import *
import sys
import time

serverName = sys.argv[1]
serverPort = 15005
clientSocket = socket(AF_INET, SOCK_DGRAM)

def send_commands():
    print('$ ', end='')
    while True:
        command = input('')  # digita o comando
        if len(command) > 0:
            if command == 'quit':
                break
            elif command[:3] == 'scp':
                clientSocket.sendto(command.encode("UTF-8"), (serverName, serverPort))

                file_size, _ = clientSocket.recvfrom(1024)
                file_size = int(file_size.decode())

                if file_size != 0:
                    clientSocket.sendto(b"ack", (serverName, serverPort))

                    arquivo, _ = clientSocket.recvfrom(1024)
                    clientSocket.sendto(b"ack", (serverName, serverPort))

                    with open(arquivo.decode(), 'wb') as file:
                        while file_size > 0:
                            if file_size > 1024:
                                partialData, _ = clientSocket.recvfrom(1024)
                                file.write(partialData)
                                file_size -= 1024
                                clientSocket.sendto(b"ack", (serverName, serverPort))
                            else:
                                partialData, _ = clientSocket.recvfrom(1024)
                                file.write(partialData)
                                file_size -= file_size
                                clientSocket.sendto(b"ack", (serverName, serverPort))

                    data, _ = clientSocket.recvfrom(1024)
                    print(data.decode(), end='')
                else:
                    print('no such file in the directory\n$ ', end='')
            else:
                clientSocket.sendto(command.encode(), (serverName, serverPort))

                # receive data, maybe create a function
                data, _ = clientSocket.recvfrom(1024)
                print(data.decode(), end='')
        else:
            # print waiting for command
            print('$ ', end='')

send_commands()
clientSocket.close()
