# -*- coding: utf-8 -*-
"""
This class is responsible for parsing a line in whatsapp conversation history
"""

import re  # For regex matching
from user import User
import unicodedata


class Regex(object):
    """
    Contains all regexes
    """
    def __init__(self):
        self.date =\
            r"^([0-9]{2}/[0-9]{2}/[0-9]{4}, [0-9]{1,2}:[0-9]{1,2} (A|P){1}M)|^([0-9]{2}/[0-9]{2}/[0-9]{4}, [0-9]{1,2}:[0-9]{1,2})"
        self.user_name = r"(-(.*?)\:)"
        self.user_action = \
            r"-\s(.*)\s(adicionou|alterado|criou|foi removido|entrou|saiu|removeu)"
        self.affected_user = r"removeu\s‪\+(.*)‬"
        self.user_actions = {
            "adicionou": "add",
            "foi removido": "removed",
            "removeu": "remove",
            "saiu": "left",
            "alterado": "alter",
            "criou": "create"}

    def verify_match(self, line, regex_string):
        """
        Verifies a given regexp in line
        """
        parser = re.compile(regex_string)
        match = parser.search(line)
        if match:
            return True
        return False

    def return_match(self, line, regexp):
        """Returns a match, given a regexp"""
        parser = re.compile(regexp)
        match = parser.search(line)
        return match

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
        return self.verify_match(line, self.user_actions)

    def get_user_by_message(self, line):
        """
        Based on message pattern (date - user_name: message), retrieves
        user data
        """
        temp_user = None
        user_name = self.match_name_in_message(line)
        message_date = self.match_date(line)
        if user_name is not None and message_date is not None:
            temp_user = User(user_name, message_date)
        return temp_user

    def get_user_by_action(self, line):
        """
        Based on action patter (date - user action), retrieves user data
        """
        temp_user = None
        affected_user = None
        user_name = self.match_name_in_action(line)
        message_date = self.match_date(line)
        user_action = self.match_action(line)
        if user_action == "remove":
            affected_user = self.match_affected_user(line)
        if user_name is not None and message_date is not None:
            temp_user = User(user_name, message_date)
        return temp_user, user_action, affected_user

    def match_affected_user(self, line):
        """Gets affected user"""
        regexp = self.affected_user
        match = self.return_match(line, regexp)
        if match:
            return match.group(1)

    def match_name_in_message(self, line):
        """Matches an user name in a message"""
        regexp = self.user_name
        match = self.return_match(line, regexp)
        if match:
            # Must remove some trashy and invisible
            # characters that whatsapp inserts in every message
            return self.remove_special_characters(match.group(2))

    def match_date(self, line):
        """Matches a date"""
        regexp = self.date
        match = self.return_match(line, regexp)
        if match:
            return match.group()

    def match_name_in_action(self, line):
        """Matches an user name in an action"""
        regexp = self.user_action
        match = self.return_match(line, regexp)
        if match:
            return self.remove_special_characters(match.group(1))

    def match_action(self, line):
        """Matchs an action and converts it to code action name"""
        regexp = self.user_action
        match = self.return_match(line, regexp)
        if match:
            action = match.group(2)
            if action in self.user_actions.keys():
                return self.user_actions[action]

    def remove_special_characters(self, string):
        clean_string = string
        if '‬' in string:
            clean_string = string.replace('‬', "")
        if "+" in string:
            clean_string = string.replace("+", "")
        return self.remove_control_characters(
            clean_string.lstrip().rstrip().decode('utf-8'))

    def remove_control_characters(self, s):
        return "".join(ch for ch in s if unicodedata.category(ch)[0] != "C")
