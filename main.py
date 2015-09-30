# -*- coding: utf-8 -*-
"""
Main function, wrapping everything
"""
import os.path
import sys

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
    group.show_results()
    # print group.teste
    for user in group.users:
        print user
