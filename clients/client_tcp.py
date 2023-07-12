from socket import *
import os

serverName = '192.168.1.27'
serverPort = 32007
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))

def send_commands():
    print(os.getcwd() + '$ ', end='')
    while True:
        command = input('')  # Enter the command

        if len(command) > 0:
            if command == 'quit':
                break
            elif command[:3] == 'scp':
                encodedCommand = command.encode("UTF-8")
                clientSocket.send(encodedCommand)
                confirmation = clientSocket.recv(2048)
                if confirmation.decode() == 'yes':
                    arquivo = clientSocket.recv(2048).decode()

                    with open(arquivo, 'wb') as file:
                        while True:
                            chunk = clientSocket.recv(2048)
                            if not chunk:
                                break
                            file.write(chunk)
                        file.close()

                    # Receive the final response
                    data = receive_complete_response(clientSocket)
                    print(data, end='')
                else:
                    print(confirmation.decode(), end='')

            else:
                encodedCommand = command.encode("UTF-8")
                clientSocket.send(encodedCommand)
                data = receive_complete_response(clientSocket)
                print(data, end='')
        else:
            print(os.getcwd() + '$ ', end='')

    clientSocket.close()

def receive_complete_response(socket):
    buffer_size = 4096  # Adjust the buffer size as needed
    response = b""
    while True:
        chunk = socket.recv(buffer_size)
        response += chunk
        if len(chunk) < buffer_size:
            break
    return response.decode()

send_commands()
