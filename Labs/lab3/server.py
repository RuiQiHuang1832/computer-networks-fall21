########################################################################################################################
# Class: CSC645-01 Computer Networks SFSU
# Lab3: TCP Server Socket
# Goal: Learning Networking in Python with TCP sockets
# Student Name: Rui Qi Huang
# Student ID: 917292550
# Student Github Username: RuiQiHuang1832
# Program Running instructions: python3 server.py # compatible with python version 3
#
########################################################################################################################

# don't modify this imports.
import socket
import pickle
from threading import Thread


class Server(object):
    """
    The server class implements a server socket that can handle multiple client connections.
    It is really important to handle any exceptions that may occur because other clients
    are using the server too, and they may be unaware of the exceptions occurring. So, the
    server must not be stopped when a exception occurs. A proper message needs to be show in the
    server console.
    """
    MAX_NUM_CONN = 10  # keeps 10 clients in queue

    def __init__(self, host="127.0.0.1", port=12000):
        """
        Class constructor
        :param host: by default localhost. Note that '0.0.0.0' takes LAN ip address.
        :param port: by default 12000
        """
        self.host = host
        self.port = port
        self.serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # TODO: create the server socket
        # self.handlers = {}  # ignore this for this lab. It will be used in lab 4

    def _bind(self):
        """
        # TODO: bind host and port to this server socket
        :return: VOID
        """
        self.serversocket.bind((self.host, self.port))

    def _listen(self):
        """
        # TODO: puts the server in listening mode.
        # TODO: if successful, print the message "Server listening at ip/port"
        :return: VOID
        """
        self._bind()
        self.serversocket.listen(self.MAX_NUM_CONN)
        print("Listening at " + self.host + "/" + str(self.port))

    def _accept_clients(self):
        """
        #TODO: accept clients when they connect, and creates the client handler
               after accepting the client, creating the client handler, and
               send the client id to the client, you should call the
               process_request(....) method next because after the client id
               is sent, the client will send a request with the student info.
               Recall that the server must acknowledge that it received
               the student info after processing the data
        :return: VOID
        """

        clienthandler, addr = self.serversocket.accept()
        with clienthandler:
            client_id = addr[1]
            self._sendID(clienthandler, client_id)
            while True:
                raw_data = clienthandler.recv(1024)  # receives data from this client
                self._process_request(clienthandler, raw_data)
                if not raw_data:
                    break

    def _sendID(self, clienthandler, clientid):
        """
        TODO: sends the client id to the client
        :clienthandler: the handler created by the server for the client
        :clientid: an integer representing the client id assigned to the client
        """
        data = {'clientid': clientid}
        serialized_data = pickle.dumps(data)
        clienthandler.send(serialized_data)

    def _process_request(self, clienthandler, request):
        """
        TODO: process a request from the client and sends
              a response back acknowledging that the data was received
              here is where you retrieve the student info from your client
              and print it on the server side
        :clienthandler: the handler created by the server after accepting the client
        :request: the request from the client. It must be already deserialized.
        """
        data = pickle.loads(request)  # deserializes the data from the client
        student_name = data['student_name']
        github_username = data['github_username']
        sid = data['sid']
        log = "Connected: Student: " + student_name + ", Github Username: " + github_username + ", sid: " + str(sid)
        print(log)
        serialized_data = pickle.dumps(1)
        clienthandler.send(serialized_data)

    def run(self):
        """
        Already implemented for you
        Run the server.
        :return: VOID
        """
        self._listen()
        self._accept_clients()


# main execution
if __name__ == '__main__':
    server = Server()
    server.run()
