from socket import *

server = gethostbyname(gethostname())
serverPort = 12000
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((server, serverPort))

cont = True
while cont:
    try:
        serverMessage = clientSocket.recv(1024).decode()
        print('[SERVER]:', serverMessage)

        userResponse = input('> ')
        clientSocket.send(userResponse.encode())

        if userResponse == '0':
            print("Closing the connection...")
            cont = False
        else:
            while True:
                serverMessage = clientSocket.recv(1024).decode()
                print('[SERVER]:', serverMessage)
                if 'Enter' in serverMessage or 'Invalid' in serverMessage :
                    userResponse = input('> ')
                    clientSocket.send(userResponse.encode())
                    if userResponse.lower() == 'logout' or userResponse.lower() == 'quit' or userResponse == '0':
                        break
                if 'Goodbye' in serverMessage :

                    break
    except Exception as e:
        print(f"An error occurred: {e}")
        cont = False

clientSocket.close()
