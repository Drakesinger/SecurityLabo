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
    s.send(("1 " + user+"\r\n").encode(encoding="UTF-8"))
    print("sent")
    data = s.recv(1024)
    print("recieved")
    s.close()
    print("received data:", data.decode(encoding="UTF-8"))

if __name__ == '__main__':
    main()
