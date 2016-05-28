#!/usr/bin/python3
# -*- coding: utf-8 -*-

import re
import Global
import socket


def getString(name, regex):
    value = None
    while (not value):
        value = input("Enter %s : " % name)
        # We could validate the response here according to the
        # minimum requirements in the GLOBAL file
        # however, a challenge-response system
        # must send data to validate it, not validate it
        # locally.

        #if not re.match(regex, value):
        #    value = None
        #    print("Invalide %s, please retry !" % name)
    return value


def getInt(name):
    value = None
    while (not value):
        value = input("Enter %s : " % name)
        try:
            value = int(value)
        except:
            value = None
            print("Invalid %s, please retry !" % name)
    return value


def getMessage(sock):
    data = sock.recv(Global.BUFFER_SIZE)
    str = data.decode(encoding="UTF-8")
    message = Global.Message(str)
    print("received '%s'" % str.rstrip())
    return message


def main():
    print()
    print()
    print("Challenge client")
    print("================")
    print()
    host = "157.26.109.83" #getString("host", Global.REGEX_HOST)
    port = 7777 # getInt("port")
    user = getString("user", Global.REGEX_USER)
    print("Connect to %s@%s:%d" % (user, host, port))

    sock = socket.create_connection((host, port))

    if sock:
        print("Connected to server.")
    else:
        return

    sock.send(Global.getMessage(1, user).encode(encoding="UTF-8"))
    message = getMessage(sock)
    if len(message.getRaw()) == 0:
        print("Server has disconnected.")
    elif message.isValid():
        print("Message received: ",message.getContent())
        if message.getCode() == 2:
            print("chap = '%s'" % message.getContent())
            code = getString("chap", Global.REGEX_CHALLENGE)
            sock.send(Global.getMessage(4, code).encode(encoding="UTF-8"))
            message = getMessage(sock)
            if len(message.getRaw()) == 0:
                print("Server has disconnected.")
            elif message.isValid():
                if message.getCode() == 5:
                    print("User ok!")
                else:
                    print("Bad chap !")
            else:
                print("Error, user unknown !")
        else:
            print("Error, user unknown !")
    else:
        print("Response not valid !")

    sock.close()


if __name__ == '__main__':
    main()
