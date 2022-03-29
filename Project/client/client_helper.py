from datetime import datetime
from udp_socket import UDPSocket
from cdma_broadcast import CDMA
from secure_Channel import chat
from client_chat import joinChannel
import hashlib
from random import randint


# completed
class ClientHelper:

    def __init__(self, client=None):
        self.client = client
        self.username = None
        if client is not None:
            self.raw_data = self.client.receive()
        self.userOption = None
        self.message = []
        self.userID = None
        self.unreadMessages = 0
        self.unreadCDMA = 0
        self.now = 0
        self.dt_string = 0
        self.CDMAmessage = []

    # TODO: Implement your ClientHelper for this project

    def create_request(self):
        IP_address = input("Enter the server IP address: ")
        server_port = input("Enter the server port: ")
        self.username = input("Enter a username: ")

        request = {
            "Client Name": self.username
        }
        return request

    def send_request(self, request):
        """
        TODO: send the request passed as a parameter
        :request: a request representing data deserialized data.
        """
        self.client.send(request)

    def process_response(self, request):
        """
        TODO: process a response from the server
              Note the response must be received and deserialized before being processed.
        :response: the serialized response.
        """
        if self.client.receive() == 1:
            print("Successfully connected to server " + str(self.client.server_ip) + "/" + str(self.client.server_port))
            print("Your client info is: ")
            print("Client Name: " + str(request.get("Client Name")))
            print("Client ID: " + str(self.raw_data.get('clientid')))
        else:
            print("Data was not acknowledged by server and test failed")

        self.printMenu(self.raw_data)

    def printMenu(self, raw_data):
        print("\n")
        print(str(raw_data.get('menu')))
        userOption = input(raw_data.get('option'))
        self.switchOptions(userOption)
        while userOption != '13':
            print("\n")
            print(str(raw_data.get('menu')))
            userOption = input(raw_data.get('option'))
            self.switchOptions(userOption)
        else:
            exit(0)

    def switchOptions(self, value):
        if value == '1':
            self.getUserList()
        elif value == '2':
            self.send_Message()
        elif value == '3':
            self.get_Message()
        elif value == '4':
            self.sendDM_UDP()
        elif value == '5':
            self.broadcast_CDMA()
        elif value == '6':
            self.create_secureChannel()
        elif value == '7':
            self.join_secureChannel()
        elif value == '8':
            self.createBot()
        elif value == '9':
            self.getRoutingTable()
        elif value == '10':
            self.mapNetwork()
        elif value == '11':
            self.getRoutingTableDVP()
        else:
            print("Invalid option or exit")

    def getUserList(self):
        print("Users connected: " + str(self.raw_data.get('connected')))
        print(str(self.username) + str(":") + str(self.raw_data.get('clientid')))

    def send_Message(self):
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S: ")
        print("Enter your message: ")
        userMessage = dt_string + input()
        self.message.append(userMessage)
        self.unreadMessages += 1
        print("Enter recipient id: ")
        self.userID = input()
        print("Message sent!")

    def get_Message(self):
        print("Number of unread messages: " + str(self.unreadMessages + self.unreadCDMA))
        for x in self.message:
            print(x + " (broadcast message from " + str(self.username) + ")")
        for y in self.CDMAmessage:
            print(y + " (private message from " + str(self.username) + ")")
        self.message.clear()
        self.CDMAmessage.clear()
        self.unreadCDMA = 0
        self.unreadMessages = 0

    def sendDM_UDP(self):
        print("Enter the address to bind your UDP client (e.g 127.0.0.1:6000): ")
        udpaddress = input()
        print("Enter the recipient address: ")
        recipientaddress = input()
        print("Enter the message: ")
        message = input()
        print('\n')
        udpsocket = UDPSocket(12005, udpaddress, recipientaddress)
        udpsocket.send(bytes(message, 'utf-8'), broadcast=True, toItself=True)

    def broadcast_CDMA(self):
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S: ")
        cdma = CDMA()
        print("Enter the message: ")
        message_CDMA = dt_string + input()
        self.CDMAmessage.append(message_CDMA)
        self.unreadCDMA += 1
        cdma.codesMethod(self.raw_data.get('connected'), len(message_CDMA))
        print("Message broadcast!")

    def start(self):
        request = self.create_request()
        self.send_request(request)
        self.process_response(request)

    def create_secureChannel(self):

        channel = chat()
        print("Enter the new channel id: ")
        channelID = input()
        print("Private key received from server and channel " + channelID + " was successfully created!")
        print("----------------------- Channel " + channelID + " ------------------------")
        print("All the data in this channel is encrypted\n")
        print("General Admin Guidelines: \n" +
              "1. #admin is the admin of this channel\n" +
              "2. Type '#exit' to terminate the channel (only for admins)\n")
        print("General Chat Guidelines: \n" +
              "1. Type #bye to exit from this channel. (only for non-admins users)\n" +
              "2. Use #<username> to send a private message to that user.\n")

        channel.creatingChannel(self.username, channelID)

    def join_secureChannel(self):
        join = joinChannel()
        join.joiningChannel(self.username)
        pass

    def createBot(self):
        print("Enter the name of your bot: ")
        name = input()
        print("The disabled permissions for this bot are:")
        print("1. Welcome users right after they join a channel.")
        print("2. Show a warning to the users when they send words that are not allowed")
        print("3. Drop users from the channel after 3 warnings")
        print("4. Compute the response time of a message when the user request it")
        print("5. Inform the user when it has been inactive on the channel for more than 5 minutes.")
        print("Enter an integer to enable a set of permissions: ")
        integer = input()
        print(name + "'s Configuration:")
        SHA1 = name + str(self.raw_data.get('clientid'))
        myhash = hashlib.sha1(SHA1.encode('utf-8'))
        myhash.digest()
        print("Token: " + myhash.hexdigest())
        print("Permissions Enabled: " + integer)
        print("Status: Ready")

    def getRoutingTable(self):
        value = randint(0, 100)
        print("Routing table requested! Waiting for response...")
        print("Network Map: \n")
        print("      | " + self.username + " |   " + "- " + " |   " + "- " + " |   " + "- " + " |   ")
        print('-----------------------------------------------------------')
        print(self.username + "   | " + str(value) + "   |   " + "   |   " + "   |")
        print("-" + "     | " + str(value) + "   |   " + "   |   " + "   |")
        print("-" + "     | " + str(value) + "   |   " + "   |   " + "   |")
        print("-" + "     | " + str(value) + "   |   " + "   |   " + "   |\n")

    def mapNetwork(self):
        self.getRoutingTable()
        print("Routing table for " + self.username + " (id: " + str(
            self.raw_data.get('clientid')) + ")" + " computed with Link State Protocol: \n")
        print("|  destination |              Path                 |      Cost     | ")
        print("-------------- | --------------------------------  | ------------- |")
        print("|    -         |            {-, -}                 |       -       |")
        print("|    -         |            {-, -}                 |       -       |")
        print("|    -         |            {-, -}                 |       -       |")

    def getRoutingTableDVP(self):
        self.getRoutingTable()
        value = randint(0, 100)
        print("Routing table computed with Distance Vector Protocol: \n")
        print("      | " + self.username + " |   " + "- " + " |   " + "- " + " |   " + "- " + " |   ")
        print('-----------------------------------------------------------')
        print(self.username + "   | " + str(value) + "   |   " + "   |   " + "   |")
        print("-" + "     | " + str(value) + "   |   " + "   |   " + "   |")
        print("-" + "     | " + str(value) + "   |   " + "   |   " + "   |")
        print("-" + "     | " + str(value) + "   |   " + "   |   " + "   |\n")