"""
This module is responsible for counting messages from a given text file,
following whatsapp's conversation format, to count group activity
"""


class Regex(object):
    """
    Contains all regexes
    """
    def __init__(self):
        self.date =\
            "^[0-9]{2}/[0-9]{2}/[0-9]{4}, [0-9]{1,2}:[0-9]{1,2} (A|P){1}M"


class GroupHandler(object):
    """
    This class will read the group file and create a list of users and measure
    their activity data
    """
    def __init__(self):
