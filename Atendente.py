class Atendente():
    """
    This class represents a call center operator
    """

    def __init__(self, id, state):
        self.id = id  # Operator id
        self.state = state  # Operator state
        self.call = None  # Call that the operator is working
