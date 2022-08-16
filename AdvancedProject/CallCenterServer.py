import time
from twisted.internet import reactor
from twisted.internet.protocol import Protocol
from twisted.internet.protocol import ServerFactory as ServFactory
from twisted.internet.endpoints import TCP4ServerEndpoint
import json
from Atendente import Atendente


class Server(Protocol):
    """
    This class represent a Call Center Server and is responsible
    to receive a Json file that represent the functionalities of a
    call center
    """

    def __init__(self):
        self.operators = []  # Operators lists
        self.calls_availables = []  # Calls available list
        self.calls_attended = []  # Calls available list
        self.create_operators("A")
        self.create_operators("B")

    def create_operators(self, id):
        """
        This method create a new operator and put this operator
        in the operator list
        :param id: Operator id
        :return:
        """
        self.operators.append(Atendente(id, "available"))

    def connectionMade(self):
        """"
        This method create a connection with the client
        """
        print("New connection")
        self.transport.write("Hello from server".encode("utf-8"))

    def dataReceived(self, data):
        """
        This method receive the Json data
        :param data: Json data
        :return:
        """
        self.decode_json(data)

    def send_message(self, data):
        """
        This method send a Json data to the Client
        :param data: Json data
        :return:
        """
        self.transport.write(bytes(data, "utf-8"))

    def make_json(self, response):
        """
        This method create the Json data that will be sent
        to the client
        :param response: Dict
        :return: json_dict: Json data
        """
        json_dict = json.dumps(response)
        return json_dict

    def decode_json(self, data):
        """
        This method is responsible for interpreting the Json data
        received by the client and then send the command to the system
        :param data: Json data
        :return:
        """
        command = json.loads(data.decode("utf-8"))
        if command.get("command") == "call":
            self.do_call(command.get("id"))
        elif command.get("command") == "answer":
            self.do_answer(command.get("id"))
        elif command.get("command") == "hangup":
            self.do_hangup(command.get("id"))
        else:
            self.do_reject(command.get("id"))

    def do_call(self, id):
        """
        This method create a call in the system
        :param id: Call id
        :return:
        """
        dict_json = {"response": f"Call {id} received"}
        self.send_message(self.make_json(dict_json))
        self.calls_availables.append(id)
        self.ring_call(id)

    def ring_call(self, id=None):
        """
        This method is responsible to ring a call to an operator
        and with the operator is busy, it sends a message which says
        the call is in the queue
        :param id: Call id
        :return:
        """
        for i in range(len(self.operators)):
            if self.operators[i].state == "available":
                dict_json = {"response": f"Call {self.calls_availables[0]} ringing for operator {self.operators[i].id}"}
                self.send_message(self.make_json(dict_json))
                self.operators[i].call = self.calls_availables[0]
                self.operators[i].state = "ringing"
                self.calls_availables.remove(self.operators[i].call)
                return
        dict_json = {"response": f"Call {id} waiting in queue"}
        self.send_message(self.make_json(dict_json))

    def do_answer(self, operator):
        """
        This method is responsible to answer a call
        :param operator: Operator id
        :return:
        """
        for i in range(len(self.operators)):
            if self.operators[i].id == operator:
                dict_json = {"response": f"Call {self.operators[i].call} answered by operator {operator}"}
                self.send_message(self.make_json(dict_json))
                self.operators[i].state = "busy"
                self.calls_attended.append(self.operators[i].call)

    def do_hangup(self, id):
        """
        This method is responsible to finish a call and set the
        operator status to available
        :param id: Call id
        :return:
        """
        call_ring = False
        for i in range(len(self.operators)):
            if self.operators[i].call == id:
                call_ring = True
                if self.operators[i].state == "busy":
                    self.calls_attended.remove(self.operators[i].call)
                else:
                    self.operators[i].state = "available"
                    dict_json = {"response": f"Call {self.operators[i].call} missed"}
                    self.send_message(self.make_json(dict_json))
                    break
                self.operators[i].call = None
                self.operators[i].state = "available"
                dict_json = {"response": f"Call {id} finished and operator {self.operators[i].id} available"}
                self.send_message(self.make_json(dict_json))
                break
        if not call_ring:
            self.calls_availables.remove(id)
            dict_json = {"response": f"Call {id} missed"}
            self.send_message(self.make_json(dict_json))
        if self.calls_availables:
            self.ring_call()
        return

    def do_reject(self, operator):
        """
        This method is responsible to reject a call
        :param operator: Operator id
        :return:
        """
        for i in range(len(self.operators)):
            if self.operators[i].id == operator:
                dict_json = {"response": f"Call {self.operators[i].call} rejected by operator {operator}"}
                self.send_message(self.make_json(dict_json))
                dict_json = {"response": f"Call {self.operators[i].call} ringing for operator {operator}"}
                self.send_message(self.make_json(dict_json))


class ServerFactory(ServFactory):

    def buildProtocol(self, addr):
        return Server()


if __name__ == '__main__':
    """
    Here we run the test in the TCP port 5678 
    """
    endpoint = TCP4ServerEndpoint(reactor, 5678)
    endpoint.listen(ServerFactory())
    reactor.run()
