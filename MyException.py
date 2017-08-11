# -*- coding: utf-8 -*-
"""
    my Exception error define here
"""


# SQL connect Exception Process
class SQLconnError(Exception):
    def __init__(self, arg):
        self.arg = arg


# WebServer Exception Process
class WebServerError(Exception):
    def __init__(self, arg):
        self.arg = arg
