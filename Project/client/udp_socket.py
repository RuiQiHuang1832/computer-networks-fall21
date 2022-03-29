import socket


class UDPSocket:

    def __init__(self, port, udpaddress, recipientaddress):
        self.port = port
        self.udpaddress = udpaddress
        self.recipientaddress = recipientaddress
        self.ipv4 = socket.AF_INET
        self.transmission_protocol = socket.SOCK_DGRAM
        self.udp_socket = socket.socket(self.ipv4, self.transmission_protocol)
        self.listen()


    def listen(self):
        try:
            self.bind()
            print(f'UDP client running and accepting other clients at udp address {self.udpaddress}')
        except ConnectionError as err:
            print("An error occurred: ", err.args[1])

    def bind(self):
        address = ('', self.port)
        self.udp_socket.bind(address)

    def send(self, message, to=None, broadcast=False, toItself=False):
        if broadcast:
            self.broadcast(message, toItself)
        else:
            self.udp_socket.sendto(message, to)

    def broadcast(self, message, toItself=False):
        socket_option = socket.SOL_SOCKET
        transmission_method = socket.SO_BROADCAST
        active = 1
        self.udp_socket.setsockopt(socket_option, transmission_method, active)
        address = ('<broadcast>', self.port)
        self.udp_socket.sendto(message, address)
        if toItself:
            self.print_response(is_broadcast=True)

    def print_response(self, is_broadcast=False, mem_alloc=4096):
            data, addr = self.udp_socket.recvfrom(mem_alloc)
            if is_broadcast:
                print("Message sent to udp address:" + str(self.recipientaddress))
            else:
                print(f'{data} from {addr}')


