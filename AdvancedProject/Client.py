import time

from twisted.internet import reactor
from twisted.internet.protocol import Protocol
from twisted.internet.protocol import ClientFactory as CLFactory
from twisted.internet.endpoints import TCP4ClientEndpoint
import json


class Client(Protocol):
    """
    This class simulate a Client of a call center, it sends messages
    to the call center server and then the server answer to the client
    and these answers are printed for the client
    """

    def dataReceived(self, data):
        """
        This method receive the Json data
        :param data: Json data
        :return:
        """
        self.decode_json(data)
        self.message_input()

    def send_message(self, data):
        """
        This method send a Json data to the server
        :param data: Json data
        :return:
        """
        self.transport.write(bytes(data, "utf-8"))

    def message_input(self):
        """
        This method receive inputs from the user, these inputs
        are the messages that represents a call center instructions
        :return:
        """
        data = input(" ")
        json_data = self.json_message(data)
        self.send_message(json_data)

    def json_message(self, data):
        """
        This method create the Json file that will be sent to
        the server
        :param data: Input Messages
        :return: json_obj: Json File
        """
        array = data.split(" ")
        if array[0] == "answer":
            dict_json = {"command": array[0], "id": array[1]}
        elif array[0] == "call":
            dict_json = {"command": array[0], "id": array[1]}
        elif array[0] == "reject":
            dict_json = {"command": array[0], "id": array[1]}
        else:
            dict_json = {"command": array[0], "id": array[1]}
        json_obj = json.dumps(dict_json)
        return json_obj

    def decode_json(self, data):
        """
        This method decode the message that was sent by the
        server
        :param data: Server Message(Json)
        :return:
        """
        data = data.decode("utf-8")
        if "Hello" not in data:
            self.map_dict(data)

    def map_dict(self, data):
        """"
        This method transform the Json that was sent by the server
        in a dictionary and the print the response to the Client
        :param data: Server Message(Json)
        """
        while data.find("{") != -1:
            key1 = data.find("{")
            key2 = data.find("}")
            dict_json = data[key1:key2 + 1]
            dict_json = json.loads(dict_json)
            print(dict_json.get("response"))
            data = data.replace(data[key1:key2 + 1], "")


class ClientFactory(CLFactory):
    def buildProtocol(self, addr):
        return Client()


if __name__ == '__main__':
    """
    Here we run the Client.
    """
    endpoint = TCP4ClientEndpoint(reactor, 'localhost', 5678)
    endpoint.connect(ClientFactory())
    reactor.run()
