class ClientHelper:

    def __init__(self, client):
        self.client = client
        self.student_name = 'Rui Qi Huang'  # TODO: your name
        self.student_id = 917292550  # TODO: your student id
        self.github_username = 'RuiQiHuang1832'  # TODO: your github username

    def create_request(self, name, id, github_username):
        """
        TODO: create request with a Python dictionary to save the parameters given in this function
              the keys of the dictionary should be 'student_name', 'github_username', and
              'sid'.
        :return: the request created
        """

        request = {
            "student_name": name,
            "github_username": github_username,
            "sid": id

        }
        return request

    def send_request(self, request):
        """
        TODO: send the request passed as a parameter
        :request: a request representing data deserialized data.
        """
        self.client.send(request)

    def process_response(self):
        """
        TODO: process a response from the server
              Note the response must be received and deserialized before being processed.
        :response: the serialized response.
        """
        raw_data = self.client.receive()
        if self.client.receive() == 1:
            print(raw_data, end=" ")
            print("has successfully connected to " + str(self.client.server_ip) + "/" + str(self.client.server_port))
            print("Data acknowledged by server and you passed the test")
        else:
            print("Data was not acknowledged by server and test failed")

    def start(self):
        """
        TODO: create a request with your student info using the self.request(....) method
              send the request to the server, and then process the response sent from the server.
        """
        request = self.create_request(self.student_name, self.student_id, self.github_username)
        self.send_request(request)
        self.process_response()
