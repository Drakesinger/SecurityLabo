#!/usr/bin/python3
# -*- coding: utf-8 -*-

import re
import Global
import socket

def getString(name, regex):
    value = None
    while(not value):
        value = input("Enter %s : " % name)
        if not re.match(regex, value):
            value = None
            print("Invalide %s, please retry !" % name)
    return value

def getInt(name):
    value = None
    while(not value):
        value = input("Enter %s : "  % name)
        try:
            value = int(value)
        except:
            value = None
            print("Invalid %s, please retry !" % name)
    return value

def main():
    print()
    print()
    print("Challenge client")
    print("================")
    print()
    host = getString("host", Global.REGEX_HOST)
    port = getInt("port")
    user = getString("user", Global.REGEX_USER)
    print("Connect to %s@%s:%d" % (user, host, port))

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    print("connected")
    s.send(Global.getMessage(1, user).encode(encoding="UTF-8"))
    print("sent")
    data = s.recv(Global.BUFFER_SIZE)
    print("received")
    message = data.decode(encoding="UTF-8")
    if message[0] == "2":
        print("chap = '%s'" % message[2:])
        code = getString("chap", Global.REGEX_CHALLENGE)

        print("before resend")
        s.send(Global.getMessage(4, code).encode(encoding="UTF-8"))
        print("after resend")
        data = s.recv(Global.BUFFER_SIZE)
        message = data.decode(encoding="UTF-8")
        print("received data:", message)
        if message[0] == "5":
            print("User ok!")
        else:
            print("Bad chap !")
    else:
        print("Error, user unknown !")


    s.close()

if __name__ == '__main__':
    main()
