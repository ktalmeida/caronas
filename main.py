# -*- coding: utf-8 -*-
"""
Main function, wrapping everything
"""
import os.path
import sys
import json

from group_handler import GroupHandler
from regex_handler import Regex

if __name__ == '__main__':
    file_name = 'group_chat.txt'
    if not os.path.isfile(file_name):
        print "Erro: Não consigo achar o arquivo: %s =(" % file_name
        sys.exit()
    group = GroupHandler(file_name, Regex())
    group.parse_file()
    for user in group.users:
        print "user = %s " % user.id
        print "last_activity = %s" % user.last_message_date
        print "messages = %i" % user.number_of_messages
        print "actions = " + json.dumps(user.actions)
        print "XXXXXXXXX"
