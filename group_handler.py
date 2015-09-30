# -*- coding: utf-8 -*-
"""
This class is responsible for counting group activity,
using a reguler expression handler
"""

import operator
from user import User


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
        self.total_gone = 0

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
                line_type = "message"
                if self.regex.has_message(line):
                    # is an user message
                    temp_user = self.regex.get_user_by_message(line)
                    self.total_messages += 1
                else:
                    # is an action
                    temp_user, curr_action, affected_user = \
                        self.regex.get_user_by_action(line)
                    if curr_action not in ("left", "removed", "alter"):
                        self.total_actions += 1
                    else:
                        self.total_gone += 1
                    line_type = "action"
                    self.total_file_lines
            else:
                # Is a message from the last user who sent a message
                self.total_messages += 1
            already_added_users = self.users.keys()
            if temp_user is not None:
                if temp_user.id not in already_added_users:
                    self.users[temp_user.id] = temp_user
                curr_user = self.users[temp_user.id]
                curr_user.last_message_date = temp_user.last_message_date
                if line_type != "action":
                    curr_user.number_of_messages += 1
                else:
                    curr_user.actions[curr_action] += 1
                if curr_user.has_left():
                    del self.users[curr_user.id]
                if curr_user.has_removed() and affected_user is not None and\
                        affected_user in self.users.keys():
                    del self.users[affected_user]

        self.users = sorted(self.users.values(), key=operator.attrgetter(
            'number_of_messages'), reverse=True)

    def show_results(self):
        """Print results in terminal"""
        print "------------------"
        print "----RESULTADOS-----"
        print "------------------"
        print "Linhas do arquivo: %i" % self.total_file_lines
        print "Total de mensagens: %i, Total de ações %i" \
            % (self.total_messages, self.total_actions)
        print "Total de membros que saíram: %i" % self.total_gone
        print "Total de membros atualmente: %i" % len(self.users)

    def show_users(self):
        string = "["
        for user in self.users:
            string += str(user)
        string = "]"

    def __str__(self):
        users_string = ""
        for user in self.users:
            users_string += str(user)
        return users_string
