"""
This module is responsible for counting messages from a given text file,
following whatsapp's conversation format, to count group activity
"""

import re  #  for regex matching

class Regex(object):
    """
    Contains all regexes
    """
    def __init__(self):
        self.date =\
            "^([0-9]{2}/[0-9]{2}/[0-9]{4}, [0-9]{1,2}:[0-9]{1,2} (A|P){1}M)"
            self.user_name = "(-\s(.*?)\:)"
        self.user_name_action = "(- ‪\+[0-9]{2}\s[0-9]{2}\s[0-9]{5}-[0-9]{4}(?!.\:))"

    def verify_match(self, line, regex_string):
        """
        Verifies a given regexp in line
        """
        parser = re.compile(regex_string)
        match = parser.search(line)
        if match is not None:
            return True
        return False
    def has_date(self, line):
        """
        Returns true if current line has a date
        """
        return self.verify_match(line, self.date)

    def has_message(self, line):
        """
        Returns true if current line has an user id, like this:
        26/03/2015, 10:19 PM - Kayan Almeida: Fala Galera, boa noite...
        """
        return self.verify_match(line, self.user_name)

    def has_action(self, line):
        """
        Returns true if line is a group action, like the following:
        07/04/2014, 3:06 PM - ‪+55 21 91234-1234‬ criou o grupo
        “Caronas freguesia fundão”
        26/03/2015, 10:20 PM - ‪+55 21 91234-1234 saiu
        12/08/2015, 3:02 PM - ‪+55 21 91234-91234 adicionou ‪+55 21 91234-2222
        """
        return self.verify_match(line, self.user_name_action)

    def get_user_by_message(line):


class GroupHandler(object):
    """
    This class will read the group file and create a list of users and measure
    their activity data
    """
    def __init__(self, filename, regex):
        self.group_file = open(filename)
        self.regex = regex
        self.users = []

    def parse_file(self):
        lines = self.group_file.readlines()
        temp_user = None
        for line in lines:
            if self.regex.has_date(line):
                # Can be a message or an user action
                if self.regex.has_message(line):
                    # is an user message
                    temp_user = self.regex.get_user_by_message(line)
                else:
                    # is an action
            else:
                # Is a message from the last user who sent a message

class User(object):
    """
    This class represents a group user
    """
    def __init__(self):
        self.id = ""
        self.last_message_date = ""
        self.number_of_messages = 0
        self.actions = {"add": 0, "remove": 0}

    def __init__(self, id, last_message_date, number_of_messages):
        self.id = id
        self.last_message_date = last_message_date
        self.number_of_messages = number_of_messages
