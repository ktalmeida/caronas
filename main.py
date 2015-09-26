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
    # Searching in current directory for txt file
    files = [f for f in os.listdir('.') if os.path.isfile(f)]
    for f in files:
        if ".txt" in f:  # If file has a txt extension
            file_name = f
            break
    if not os.path.isfile(file_name):
        print "Erro: Não consigo achar um arquivo txt =(" % file_name
        sys.exit()
    group = GroupHandler(file_name, Regex())
    group.parse_file()
    for user in group.users:
        print "user = %s " % user.id
        print "last_activity = %s" % user.last_message_date
        print "messages = %i" % user.number_of_messages
        print "actions = " + json.dumps(user.actions)
        print "XXXXXXXXX"
