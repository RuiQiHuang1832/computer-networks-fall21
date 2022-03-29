import socket


class joinChannel:
    def joiningChannel(self, username):
        newSocket = socket.socket()
        hostOfServer = socket.gethostname()
        ip = socket.gethostbyname(hostOfServer)
        intPort = 8080

        hostOfServer = input('Enter the channel you would like to join: ')
        name = username
        print("----------------------- Channel " + hostOfServer + " ------------------------\n")
        print("All the data in this channel is encrypted\n")
        newSocket.connect((ip, intPort))

        newSocket.send(name.encode())
        recvSocketName = newSocket.recv(1024)
        recvSocketName = recvSocketName.decode()

        print(recvSocketName, ' just joined\n')
        print("Currently: " + recvSocketName + ", " + name + " are on this channel\n")
        print(recvSocketName + " is the admin of this channel")
        print("General Chat Guidelines: \n" +
              "1. Type #bye to exit from this channel. (only for non-admins users)\n" +
              "2. Use #<username> to send a private message to that user.\n")

        while True:
            message = (newSocket.recv(1024)).decode()
            if message == "#exit":
                exit(0)
            print(recvSocketName, ">", message)
            message = input("Me(" + name + ")" + "> ")
            newSocket.send(message.encode())
