#! /usr/bin/env python

# Modified from irccat.py

# Original author
# Joel Rosdahl <joel@rosdahl.net>

import sys
import argparse
import itertools

import irc.client
import irc.logging

class ConnectionCallbacks(object):

    def __init__(self, target, message):
        self.state = "Connecting"
        self.target = target
        self.message = message 

    def on_connect(self, connection, event):
        self.state = "Connected"
        connection.privmsg(self.target, self.message)
        connection.quit("")

    def on_disconnect(self, connection, event):
        self.state = "Disconnected"

def send_message(args):

    client = irc.client.IRC()
    try:
        c = client.server().connect(args["server"], args["port"], args["nickname"])
    except irc.client.ServerConnectionError:
        print(sys.exc_info()[1])
        return False

    cc = ConnectionCallbacks(args["target"], args["message"])
    c.add_global_handler("welcome", cc.on_connect)
    c.add_global_handler("disconnect", cc.on_disconnect)

    while cc.state != "Disconnected":
        client.process_once(0.2)

