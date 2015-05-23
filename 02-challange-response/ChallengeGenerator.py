#!/usr/bin/python3
#-*- coding: utf-8 -*-

import string
from random import choice
import os
import datetime
import Global

DEFALUT_NUMBER = Global.DEFALUT_KEY_NUMBER


# TODO: It might be interesting to keep the trace of all key/value pair to avoid generating an existing key/value pair

def generateKeyword(alphabet, lenght):
    return "".join(choice(alphabet) for _ in range(lenght))

def generateChallenge(username, entries=DEFALUT_NUMBER, output_folder="users", expiration_date=None):

    if expiration_date is None:
        expiration_date = datetime.datetime.now() + datetime.timedelta(days=Global.EXPIRATION_DAYS)
    alphabet = string.ascii_letters


    keys = [generateKeyword(alphabet, Global.KEY_LENGHT) for k in range(entries)]
    challenges = [generateKeyword(alphabet, Global.CHALLENGE_LENGHT) for k in range(entries)]

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    with open(output_folder+"/" + username + ".txt", encoding="UTF-8", mode="w") as file:
        file.write(expiration_date.strftime("%c") + "\n")

        file.write("\n")

        for (key, challenge) in zip(keys, challenges):
            file.write(key + Global.USER_FILE_DELIMITER + challenge + "\n")

def validateRegexp(regexp):
    import re
    def inner(user):
        if not re.match(regexp, user):
            raise argparse.ArgumentTypeError("Invalid format")
        return user
    return inner

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("user", help="username", type=validateRegexp(Global.REGEX_USER))
    parser.add_argument("-n", "--number", help="number of challenge", type=int, default=DEFALUT_NUMBER)
    args = parser.parse_args()

    generateChallenge(args.user, args.number)
