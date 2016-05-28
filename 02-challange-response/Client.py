#!/usr/bin/python3
# -*- coding: utf-8 -*-

import re
import Global
import socket


def get_string(name, regex):
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


def get_int(name):
    value = None
    while not value:
        value = input("Enter %s : " % name)
        try:
            value = int(value)
        except:
            value = None
            print("Invalid %s, please retry !" % name)
    return value


def get_message(sock):
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
    host = get_string("host", Global.REGEX_HOST)
    port = get_int("port")
    user = get_string("user", Global.REGEX_USER)
    print("Connect to %s@%s:%d" % (user, host, port))

    sock = socket.create_connection((host, port))

    if sock:
        print("Connected to server.")
    else:
        return

    sock.send(Global.get_message(1, user).encode(encoding="UTF-8"))

    message = get_message(sock)
    if len(message.get_raw_data()) == 0:
        print("Server has disconnected.")
    elif message.is_valid():
        print("Message received: ",message.get_content())

        if message.get_code() == 2:
            print("chap = '%s'" % message.get_content())

            code = get_string("chap", Global.REGEX_CHALLENGE)
            sock.send(Global.get_message(4, code).encode(encoding="UTF-8"))

            message = get_message(sock)
            if len(message.get_raw_data()) == 0:
                print("Server has disconnected.")
            elif message.is_valid():
                if message.get_code() == 5:
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
