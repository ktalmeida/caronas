# -*- coding: utf-8 -*-
"""
This class is responsible for counting group activity,
using a reguler expression handler
"""

import operator
from user import User
from regex_handler import Regex


class GroupHandler(object):
    """
    This class will read the group file and create a list of users and measure
    their activity data
    """
    def __init__(self, filename, regex):
        self.filename = filename
        self.regex = regex
        self.users = {}
        self.total_messages = 0
        self.total_file_lines = 0
        self.total_file_lines = 0
        self.total_messages = 0
        self.total_actions = 0

    def parse_file(self):
        lines = open(self.filename).readlines()
        self.users = {}
        temp_user = None
        already_added_users = None
        print "\rLendo o arquivo... Aguarde"
        for line in lines:
            self.total_file_lines += 1
            if self.regex.has_date(line):
                # Can be a message or an user action
                if self.regex.has_message(line):
                    # is an user message
                    temp_user = self.regex.get_user_by_message(line)
                    temp_user.number_of_messages = 1
                    self.total_messages += 1
                else:
                    # is an action
                    self.total_actions += 1
                    temp_user, curr_action = \
                        self.regex.get_user_by_action(line)
            else:
                # Is a message from the last user who sent a message
                self.total_messages += 1
            already_added_users = self.users.keys()
            if temp_user is not None:
                if temp_user.id not in already_added_users:
                    self.users[temp_user.id] = temp_user
                curr_user = self.users[temp_user.id]
                curr_user.last_message_date = temp_user.last_message_date
                if temp_user.number_of_messages > 0:
                    curr_user.number_of_messages += 1
                else:
                    curr_user.actions[curr_action] += 1
        self.users = sorted(self.users.values(), key=operator.attrgetter(
            'number_of_messages'), reverse=True)
        self.show_results()

    def show_results(self):
        """Print results in terminal"""
        print "------------------"
        print "----RESULTADOS-----"
        print "------------------"
        print "Linhas do arquivo: %i" % self.total_file_lines
        print "Total de mensagens: %i, Total de ações %i" \
            % (self.total_messages, self.total_actions)

    def __str__(self):
        users_string = ""
        for user in self.users:
            users_string += str(user)
        return users_string
