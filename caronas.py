# -*- coding: utf-8 -*-
"""
This module is responsible for counting messages from a given text file,
following whatsapp's conversation format, to count group activity
([0-9]{2}/[0-9]{2}/[0-9]{4}, [0-9]{1,2}:[0-9]{1,2} (A|P){1}M)|(‪.*‬)|(-.*\:\s)
"""

import re  #  for regex matching
import operator
import json 

class Regex(object):
    """
    Contains all regexes
    """
    def __init__(self):
        self.date =\
            r"^([0-9]{2}/[0-9]{2}/[0-9]{4}, [0-9]{1,2}:[0-9]{1,2} (A|P){1}M)"
        self.user_name = r"(-(.*?\:))"
        self.user_action = \
            r"(-\s.*)(adicionou|alterado|criou|foi removido|entrou|saiu|removeu)"
        self.user_actions = {
            "adicionou": "add", 
            "foi removido": "removed",
            "removeu": "removed", 
            "saiu": "leave",
            "alterado": "alter",
            "criou" : "create"}

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
        return self.verify_match(line, self.user_name_action)

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
        user_name = self.match_name_in_action(line)
        message_date = self.match_date(line)
        user_action = self.match_action(line)
        if user_name is not None and message_date is not None:
            temp_user = User(user_name, message_date)
            temp_user.actions[action] = 1
        return temp_user, user_action

    def match_name_in_message(self, line):
        """Matches an user name in a message"""
        regexp = self.user_name
        match = self.return_match(line, regexp)
        if match:
            # Must remove some trashy and invisible 
            # characters that whatsapp inserts in every message
            return match.group(1).split('+', 1)[-1].split('\xe2\x80\xac')[0]  

    def match_date(self, line):
        """Matches a date"""
        regexp = self.date
        match = self.return_match(line, regexp)
        if match:
            return match.group(1)

    def match_name_in_action(self, line):
        """Matches an user name in an action"""
        regexp = self.user_name
        match = self.return_match(line, regexp)
        if match:
            return match.group(1)

    def match_action(self, line):
        """Matchs an action and converts it to code action name"""
        regexp = self.user_action
        match = self.return_match(line, regexp)
        if match:
            action = match.group(2)
            if action in self.user_actions:
                return self.user_actions[action]


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

    def parse_file(self):
        lines = open(self.filename).readlines()
        self.total_file_lines = 0
        self.total_messages = 0
        self.total_actions = 0
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
                    temp_user, curr_action = self.regex.get_user_by_action(line)
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
        print "------------------"
        print "----RESULTADOS-----"
        print "------------------"
        print "Linhas do arquivo: %i \nTotal de mensagens: %i, Total de ações %i" \
            % (self.total_file_lines,self.total_messages,self.total_actions)

    def __str__(self):
        users_string = ""
        for user in self.users:
            users_string += str(user)
        return users_string

class User(object):
    """
    This class represents a group user
    """
    def __init__(self):
        self.id = u""
        self.last_message_date = ""
        self.number_of_messages = 0
        self.actions = {
            "add": 0, "removed": 0, "create":0, 
            "left":0, "leave": 0, "alter":0}

    def __init__(self, id, last_message_date):
        self.id = id
        self.last_message_date = last_message_date
        self.number_of_messages = 0
        self.actions = {
            "add": 0, "removed": 0, "create":0, 
            "left":0, "leave": 0, "alter":0}


    def __str__(self):
        return \
            "{ user: " + self.id + "\n" + ("messages: %i" % self.number_of_messages) + "}\n"


if __name__ == '__main__':
    p = GroupHandler('group_chat.txt', Regex())
    p.parse_file()
    for user in p.users:
        print "user = %s " % user.id
        print "last_activity = %s" % user.last_message_date
        print "messages = %i" % user.number_of_messages 
        print "actions = " +  json.dumps(user.actions)
        print "XXXXXXXXX"