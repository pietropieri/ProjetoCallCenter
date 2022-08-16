import cmd
import os
from Atendente import Atendente


class BasicCallCenter(cmd.Cmd):
    """"
    This call simulate a CallCenter, it received CMD commands
    that represent a call center functionalities and then send
    message that represent the call center answers
    """
    def __init__(self):
        cmd.Cmd.__init__(self)
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

    def do_call(self, id):
        """
        This method create a call in the system
        :param id: Call id
        :return:
        """
        print(f"Call {id} received")
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
                print(f"Call {self.calls_availables[0]} ringing for operator {self.operators[i].id}")
                self.operators[i].call = self.calls_availables[0]
                self.operators[i].state = "ringing"
                self.calls_availables.remove(self.operators[i].call)
                return
        print(f"Call {id} waiting in queue")

    def do_answer(self, operator):
        """
        This method is responsible to answer a call
        :param operator: Operator id
        :return:
        """
        for i in range(len(self.operators)):
            if self.operators[i].id == operator:
                print(f"Call {self.operators[i].call} answered by operator {operator}")
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
                    print(f"Call {self.operators[i].call} missed")
                    break
                self.operators[i].call = None
                self.operators[i].state = "available"
                print(f"Call {id} finished and operator {self.operators[i].id} available")
                break
        if not call_ring:
            self.calls_availables.remove(id)
            print(f"Call {id} missed")
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
                print(f"Call {self.operators[i].call} rejected by operator {operator}")
                print(f"Call {self.operators[i].call} ringing for operator {operator}")


if __name__ == '__main__':
    """"
    Here we run the BasicCallCenter
    """
    BasicCallCenter().cmdloop()
