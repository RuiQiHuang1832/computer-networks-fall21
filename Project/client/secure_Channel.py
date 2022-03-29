import socket
import client_helper


class chat:

    def creatingChannel(self, username, channelID):
        OKBLUE = '\033[94m'
        OKGREEN = '\033[92m'
        ENDC = '\033[0m'
        BOLD = '\033[1m'
        UNDERLINE = '\033[4m'
        createSocket = socket.socket()
        adminName = socket.gethostname()
        port = 8080
        theclient = client_helper.ClientHelper()

        createSocket.bind((adminName, port))
        name = username

        print(f"Waiting for other users to join....\n{OKGREEN}{BOLD}{UNDERLINE}(Please Create another terminal and "
              f"run client.py and "
              f"choose {ENDC}{BOLD}{UNDERLINE}{OKBLUE}Menu Option #7{ENDC}{BOLD}{UNDERLINE}{OKGREEN} to join the channel!){ENDC}\n")
        print("PLEASE VIEW DOCUMENTATION ATTACHED TO FOLDER IF NOT WORKING!!!!! ONLY RUN OPTION#6 IN TERMINAL")

        createSocket.listen(1)
        conn, add = createSocket.accept()
        client = (conn.recv(1024)).decode()
        conn.send(name.encode())

        while True:
            userMessage = input("Me(" + name + ")" + "> ")
            if userMessage == "#exit":
                print("Channel " + channelID + " closed by admin")
                createSocket.close()
                exit(0)
            conn.send(userMessage.encode())
            userMessage = conn.recv(1024)
            userMessage = userMessage.decode()
            print(client, '>', userMessage)
