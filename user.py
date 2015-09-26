"""
Python class that represets an User of a whatsapp group
"""


class User(object):
    """
    This class represents a group user
    """
    def __init__(self):
        self.id = u""
        self.last_message_date = ""
        self.number_of_messages = 0
        self.actions = {
            "add": 0, "removed": 0, "create": 0,
            "left": 0, "leave": 0, "alter": 0}

    def __init__(self, id, last_message_date):
        self.id = id
        self.last_message_date = last_message_date
        self.number_of_messages = 0
        self.actions = {
            "add": 0, "removed": 0, "create": 0,
            "left": 0, "leave": 0, "alter": 0}

    def __str__(self):
        return \
            "{ user: " + self.id + "\n" +\
            ("messages: %i" % self.number_of_messages) + "}\n"
