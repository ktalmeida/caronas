"""
Python class that represets an User of a whatsapp group
"""

import json


class User(object):
    """
    This class represents a group user
    """
    def __init__(self, id="", last_message_date=""):
        self.id = unicode(id)
        self.last_message_date = last_message_date
        self.number_of_messages = 0
        self.actions = {
            "add": 0, "removed": 0, "create": 0, "remove": 0,
            "left": 0, "alter": 0}

    def has_left(self):
        """
        Returns true if the user was removed, changed number of letf group
        """
        for action in self.actions:
            if action in ("left", "alter", "removed",) and \
                    self.actions[action] > 0:
                return True
        return False

    def has_removed(self):
        return self.actions["remove"] > 0

    def __str__(self):
        return json.dumps(
            self.__dict__, indent=2, ensure_ascii=False).encode('utf-8')
